"""Google Cloud Speech-to-Text provider implementation."""

import os
import uuid
from pathlib import Path
from typing import Dict, List, Optional

from src.transcribe.base import BaseTranscriber
from src.errors import (
    ValidationError,
    AuthenticationError,
    NetworkError,
    wrap_provider_exception,
)
from src.validation.language import validate_gcp_language

# Lazy imports for optional dependencies
speech_v1 = None
storage = None


def _ensure_gcp_imports():
    """Lazily import GCP libraries."""
    global speech_v1, storage
    if speech_v1 is None:
        try:
            from google.cloud import speech_v1 as _speech
            from google.cloud import storage as _storage
            speech_v1 = _speech
            storage = _storage
        except ImportError:
            raise ValidationError(
                "GCP dependencies not installed. "
                "Install with: pip install google-cloud-speech google-cloud-storage"
            )


class GCPTranscriber(BaseTranscriber):
    """
    Google Cloud Speech-to-Text provider implementation.
    
    Handles audio transcription via GCP Speech-to-Text API with Cloud Storage
    for audio files (required for long audio > 60 seconds).
    
    Required environment variables:
    - GCP_STORAGE_BUCKET: Cloud Storage bucket name for audio uploads
    
    Authentication options:
    - Recommended: Application Default Credentials via
      `gcloud auth application-default login`
    - Optional: GOOGLE_APPLICATION_CREDENTIALS pointing to a valid Google
      credential configuration file
    """
    
    PROVIDER_NAME = "GCP Speech-to-Text"
    SUPPORTED_FORMATS = {'flac', 'wav', 'mp3', 'ogg', 'webm'}
    
    # GCP encoding mapping
    ENCODING_MAP = {
        'flac': 'FLAC',
        'wav': 'LINEAR16',
        'mp3': 'MP3',
        'ogg': 'OGG_OPUS',
        'webm': 'WEBM_OPUS',
    }
    
    def __init__(self, bucket_name: Optional[str] = None):
        """
        Initialize GCP Transcriber.
        
        Args:
            bucket_name: GCS bucket name (defaults to GCP_STORAGE_BUCKET env var)
        """
        _ensure_gcp_imports()
        
        self.bucket_name = bucket_name or os.getenv('GCP_STORAGE_BUCKET')
        
        if not self.bucket_name:
            raise ValidationError(
                "GCP_STORAGE_BUCKET environment variable is required"
            )
        
        # Optional explicit credential configuration. If unset, the Google
        # client libraries use the standard Application Default Credentials chain.
        creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if creds_path and not Path(creds_path).exists():
            raise AuthenticationError(
                f"Credential file not found: {creds_path}",
                details=(
                    "Unset GOOGLE_APPLICATION_CREDENTIALS to use Application "
                    "Default Credentials, or point it to a valid Google "
                    "credential configuration file."
                )
            )
        
        try:
            self.speech_client = speech_v1.SpeechClient()
            self.storage_client = storage.Client()
            self.bucket = self.storage_client.bucket(self.bucket_name)
        except Exception as e:
            error_text = str(e).lower()
            if (
                'default credentials' in error_text
                or 'could not automatically determine credentials' in error_text
                or 'credential' in error_text
                or 'reauth' in error_text
            ):
                raise AuthenticationError(
                    "Google Cloud authentication failed",
                    details=(
                        "Authenticate locally with 'gcloud auth application-default "
                        "login', or use 'gcloud auth application-default login "
                        "--impersonate-service-account <service-account-email>' "
                        "for keyless service account access."
                    )
                )
            raise wrap_provider_exception(e, 'gcp')
        
        print(f"🔧 Initialized GCPTranscriber:")
        print(f"   Bucket: {self.bucket_name}")
        if creds_path:
            print(f"   Auth: GOOGLE_APPLICATION_CREDENTIALS")
        else:
            print(f"   Auth: Application Default Credentials (ADC)")
    
    def validate_language(self, language_code: Optional[str]) -> Optional[str]:
        """
        Validate language code for GCP Speech-to-Text.
        
        GCP requires BCP-47 format (e.g., en-US, fr-FR).
        
        Args:
            language_code: BCP-47 code or None for auto-detect
            
        Returns:
            Validated code or None
            
        Raises:
            ValidationError: If invalid format or unsupported language
        """
        return validate_gcp_language(language_code)
    
    def _upload_to_gcs(self, file_path: str) -> str:
        """
        Upload file to Google Cloud Storage.
        
        Args:
            file_path: Local path to audio file
            
        Returns:
            GCS URI for the uploaded file
        """
        file_name = Path(file_path).name
        blob_name = f"uploads/{uuid.uuid4()}_{file_name}"
        
        try:
            print(f"Uploading file to GCS: gs://{self.bucket_name}/{blob_name}")
            blob = self.bucket.blob(blob_name)
            blob.upload_from_filename(file_path)
            gcs_uri = f"gs://{self.bucket_name}/{blob_name}"
            print(f"✓ Upload complete. GCS URI: {gcs_uri}")
            return gcs_uri
        except Exception as e:
            if 'credentials' in str(e).lower() or 'permission' in str(e).lower():
                raise AuthenticationError(
                    "Access denied to GCS bucket",
                    details=str(e)
                )
            raise wrap_provider_exception(e, 'gcp')
    
    def _cleanup_gcs(self, gcs_uri: str) -> None:
        """Clean up uploaded GCS file."""
        try:
            blob_name = gcs_uri.replace(f"gs://{self.bucket_name}/", "")
            blob = self.bucket.blob(blob_name)
            blob.delete()
            print(f"🗑️  Cleaned up GCS file: {blob_name}")
        except Exception as e:
            print(f"⚠️  Warning: Could not delete GCS file: {e}")
    
    def _get_audio_config(self, file_path: str, language_code: Optional[str]) -> tuple:
        """
        Create GCP audio and recognition config objects.
        
        Returns:
            Tuple of (RecognitionConfig, use_gcs: bool)
        """
        extension = Path(file_path).suffix[1:].lower()
        encoding = self.ENCODING_MAP.get(extension, 'ENCODING_UNSPECIFIED')
        
        # Build recognition config
        config_params = {
            'encoding': getattr(speech_v1.RecognitionConfig.AudioEncoding, encoding),
            'enable_automatic_punctuation': True,
            'enable_word_time_offsets': True,
        }
        
        if language_code:
            config_params['language_code'] = language_code
        else:
            # GCP requires at least one language for auto-detection
            config_params['language_code'] = 'en-US'
            config_params['alternative_language_codes'] = ['es-ES', 'fr-FR', 'de-DE', 'it-IT']
        
        # Check file size - GCS required for > 60 seconds
        file_size_mb = Path(file_path).stat().st_size / (1024 * 1024)
        use_gcs = file_size_mb > 10  # Use GCS for larger files
        
        return speech_v1.RecognitionConfig(**config_params), use_gcs
    
    def _convert_to_standard_format(
        self,
        response,
        detected_language: Optional[str],
        enable_diarization: bool
    ) -> dict:
        """
        Convert GCP response to standardized format.
        
        Args:
            response: GCP LongRunningRecognize response
            detected_language: Language code
            enable_diarization: Whether diarization was enabled
            
        Returns:
            Standardized transcript dictionary
        """
        segments: List[Dict] = []
        full_transcript_parts = []
        duration = 0.0
        confidences = []
        
        for result in response.results:
            if not result.alternatives:
                continue
            
            alternative = result.alternatives[0]
            full_transcript_parts.append(alternative.transcript)
            
            if alternative.confidence:
                confidences.append(alternative.confidence)
            
            # Extract word-level timing
            for word_info in alternative.words:
                end_time = word_info.end_time.total_seconds()
                if end_time > duration:
                    duration = end_time
                
                if enable_diarization and hasattr(word_info, 'speaker_tag'):
                    speaker = f"spk_{word_info.speaker_tag}"
                else:
                    speaker = "spk_0"
                
                # Group words into segments (simplified)
                if segments and segments[-1]['speaker'] == speaker:
                    segments[-1]['text'] += ' ' + word_info.word
                    segments[-1]['end'] = end_time
                else:
                    segments.append({
                        'speaker': speaker,
                        'start': word_info.start_time.total_seconds(),
                        'end': end_time,
                        'text': word_info.word
                    })
        
        avg_confidence = sum(confidences) / len(confidences) if confidences else None
        
        return {
            'transcript': ' '.join(full_transcript_parts),
            'segments': segments,
            'metadata': {
                'provider': self.PROVIDER_NAME,
                'language': detected_language or 'auto-detected',
                'duration': duration,
                'confidence': avg_confidence,
            }
        }
    
    def transcribe(
        self,
        file_path: str,
        language_code: Optional[str] = None,
        enable_diarization: bool = True,
        max_speakers: int = 2
    ) -> dict:
        """
        Transcribe an audio file using GCP Speech-to-Text.
        
        Args:
            file_path: Path to the audio file
            language_code: BCP-47 language code or None for auto-detect
            enable_diarization: Enable speaker diarization
            max_speakers: Maximum number of speakers (2-10)
            
        Returns:
            Standardized transcript dictionary
        """
        self.validate_parameters(max_speakers, enable_diarization)
        self.validate_file(file_path)
        validated_language = self.validate_language(language_code)
        
        gcs_uri: Optional[str] = None
        
        try:
            config, use_gcs = self._get_audio_config(file_path, validated_language)
            
            # Enable diarization if requested
            if enable_diarization:
                diarization_config = speech_v1.SpeakerDiarizationConfig(
                    enable_speaker_diarization=True,
                    min_speaker_count=2,
                    max_speaker_count=max_speakers,
                )
                config.diarization_config = diarization_config
            
            if use_gcs:
                # Upload to GCS for long audio
                gcs_uri = self._upload_to_gcs(file_path)
                audio = speech_v1.RecognitionAudio(uri=gcs_uri)
                
                print("Starting long-running transcription...")
                operation = self.speech_client.long_running_recognize(
                    config=config,
                    audio=audio
                )
                
                print("Waiting for transcription to complete...")
                response = operation.result(timeout=3600)  # 1 hour timeout
            else:
                # Use inline audio for short files
                with open(file_path, 'rb') as audio_file:
                    content = audio_file.read()
                
                audio = speech_v1.RecognitionAudio(content=content)
                
                print("Starting transcription...")
                response = self.speech_client.recognize(config=config, audio=audio)
            
            print("✓ Transcription complete")
            
            return self._convert_to_standard_format(
                response,
                detected_language=validated_language,
                enable_diarization=enable_diarization
            )
            
        except Exception as e:
            if 'credentials' in str(e).lower() or 'permission' in str(e).lower():
                raise AuthenticationError(
                    "GCP authentication failed",
                    details=str(e)
                )
            elif 'timeout' in str(e).lower() or 'deadline' in str(e).lower():
                raise NetworkError(
                    "GCP request timed out",
                    details=str(e)
                )
            raise wrap_provider_exception(e, 'gcp')
        
        finally:
            if gcs_uri:
                self._cleanup_gcs(gcs_uri)
