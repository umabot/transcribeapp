"""Azure AI Speech provider implementation."""

import os
import time
from pathlib import Path
from typing import Dict, List, Optional

from src.transcribe.base import BaseTranscriber
from src.errors import (
    ValidationError,
    AuthenticationError,
    NetworkError,
    wrap_provider_exception,
)
from src.validation.language import validate_azure_language

# Lazy import for optional dependency
speechsdk = None


def _ensure_azure_imports():
    """Lazily import Azure Speech SDK."""
    global speechsdk
    if speechsdk is None:
        try:
            import azure.cognitiveservices.speech as _speechsdk
            speechsdk = _speechsdk
        except ImportError:
            raise ValidationError(
                "Azure Speech SDK not installed. "
                "Install with: pip install azure-cognitiveservices-speech"
            )


class AzureTranscriber(BaseTranscriber):
    """
    Azure AI Speech provider implementation.
    
    Handles audio transcription via Azure Cognitive Services Speech SDK.
    Uses continuous recognition for longer audio files and supports
    speaker diarization via ConversationTranscriber.
    
    Required environment variables:
    - AZURE_SPEECH_KEY: Azure Speech service subscription key
    - AZURE_SPEECH_REGION: Azure region (e.g., eastus, westeurope)
    """
    
    PROVIDER_NAME = "Azure AI Speech"
    SUPPORTED_FORMATS = {'wav', 'mp3', 'ogg', 'flac', 'webm', 'm4a', 'mp4'}
    
    def __init__(
        self, 
        speech_key: Optional[str] = None,
        speech_region: Optional[str] = None
    ):
        """
        Initialize Azure Transcriber.
        
        Args:
            speech_key: Azure Speech key (defaults to AZURE_SPEECH_KEY env var)
            speech_region: Azure region (defaults to AZURE_SPEECH_REGION env var)
        """
        _ensure_azure_imports()
        
        self.speech_key = speech_key or os.getenv('AZURE_SPEECH_KEY')
        self.speech_region = speech_region or os.getenv('AZURE_SPEECH_REGION')
        
        if not self.speech_key:
            raise AuthenticationError(
                "AZURE_SPEECH_KEY environment variable is required"
            )
        
        if not self.speech_region:
            raise ValidationError(
                "AZURE_SPEECH_REGION environment variable is required"
            )
        
        try:
            self.speech_config = speechsdk.SpeechConfig(
                subscription=self.speech_key,
                region=self.speech_region
            )
            # Enable detailed output
            self.speech_config.request_word_level_timestamps()
            self.speech_config.output_format = speechsdk.OutputFormat.Detailed
        except Exception as e:
            raise wrap_provider_exception(e, 'azure')
        
        print(f"🔧 Initialized AzureTranscriber:")
        print(f"   Region: {self.speech_region}")
    
    def validate_language(self, language_code: Optional[str]) -> Optional[str]:
        """
        Validate language code for Azure AI Speech.
        
        Azure requires BCP-47 format (e.g., en-US, fr-FR).
        
        Args:
            language_code: BCP-47 code or None for auto-detect
            
        Returns:
            Validated code or None
            
        Raises:
            ValidationError: If invalid format or unsupported language
        """
        return validate_azure_language(language_code)
    
    def _transcribe_simple(
        self,
        file_path: str,
        language_code: Optional[str]
    ) -> List[Dict]:
        """
        Simple transcription without diarization.
        
        Uses continuous recognition to handle longer audio files.
        
        Returns:
            List of result dictionaries
        """
        if language_code:
            self.speech_config.speech_recognition_language = language_code
        
        audio_config = speechsdk.AudioConfig(filename=file_path)
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config,
            audio_config=audio_config
        )
        
        results = []
        done = False
        
        def on_recognized(evt):
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                results.append({
                    'text': evt.result.text,
                    'offset': evt.result.offset / 10_000_000,  # Convert to seconds
                    'duration': evt.result.duration / 10_000_000,
                })
        
        def on_session_stopped(evt):
            nonlocal done
            done = True
        
        def on_canceled(evt):
            nonlocal done
            done = True
            if evt.result.reason == speechsdk.CancellationReason.Error:
                error_details = evt.result.error_details
                if 'unauthorized' in error_details.lower() or 'invalid subscription' in error_details.lower():
                    raise AuthenticationError(
                        "Azure authentication failed",
                        details=error_details
                    )
                raise NetworkError(
                    "Azure transcription canceled",
                    details=error_details
                )
        
        recognizer.recognized.connect(on_recognized)
        recognizer.session_stopped.connect(on_session_stopped)
        recognizer.canceled.connect(on_canceled)
        
        print("Starting continuous recognition...")
        recognizer.start_continuous_recognition()
        
        # Wait for completion
        timeout = 3600  # 1 hour
        start_time = time.time()
        while not done:
            time.sleep(0.5)
            if time.time() - start_time > timeout:
                recognizer.stop_continuous_recognition()
                raise NetworkError("Azure transcription timed out")
        
        recognizer.stop_continuous_recognition()
        print("✓ Recognition complete")
        
        return results
    
    def _transcribe_with_diarization(
        self,
        file_path: str,
        language_code: Optional[str],
        max_speakers: int
    ) -> List[Dict]:
        """
        Transcription with speaker diarization using ConversationTranscriber.
        
        Returns:
            List of result dictionaries with speaker info
        """
        if language_code:
            self.speech_config.speech_recognition_language = language_code
        
        audio_config = speechsdk.AudioConfig(filename=file_path)
        
        # Use ConversationTranscriber for diarization
        transcriber = speechsdk.transcription.ConversationTranscriber(
            speech_config=self.speech_config,
            audio_config=audio_config
        )
        
        results = []
        done = False
        
        def on_transcribed(evt):
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                results.append({
                    'text': evt.result.text,
                    'speaker': evt.result.speaker_id or 'Unknown',
                    'offset': evt.result.offset / 10_000_000,
                    'duration': evt.result.duration / 10_000_000,
                })
        
        def on_session_stopped(evt):
            nonlocal done
            done = True
        
        def on_canceled(evt):
            nonlocal done
            done = True
            if evt.result.reason == speechsdk.CancellationReason.Error:
                error_details = evt.result.error_details
                if 'unauthorized' in error_details.lower():
                    raise AuthenticationError(
                        "Azure authentication failed",
                        details=error_details
                    )
        
        transcriber.transcribed.connect(on_transcribed)
        transcriber.session_stopped.connect(on_session_stopped)
        transcriber.canceled.connect(on_canceled)
        
        print("Starting conversation transcription with diarization...")
        transcriber.start_transcribing_async().get()
        
        # Wait for completion
        timeout = 3600
        start_time = time.time()
        while not done:
            time.sleep(0.5)
            if time.time() - start_time > timeout:
                transcriber.stop_transcribing_async().get()
                raise NetworkError("Azure transcription timed out")
        
        transcriber.stop_transcribing_async().get()
        print("✓ Conversation transcription complete")
        
        return results
    
    def _convert_to_standard_format(
        self,
        results: List[Dict],
        language_code: Optional[str],
        enable_diarization: bool
    ) -> dict:
        """
        Convert Azure results to standardized format.
        """
        segments: List[Dict] = []
        full_transcript_parts = []
        duration = 0.0
        
        for result in results:
            text = result.get('text', '')
            if not text:
                continue
            
            full_transcript_parts.append(text)
            
            start = result.get('offset', 0)
            end = start + result.get('duration', 0)
            
            if end > duration:
                duration = end
            
            speaker = result.get('speaker', 'spk_0')
            if not speaker or speaker == 'Unknown':
                speaker = 'spk_0'
            elif not speaker.startswith('spk_'):
                # Normalize speaker format
                speaker = f"spk_{speaker}"
            
            segments.append({
                'speaker': speaker,
                'start': start,
                'end': end,
                'text': text
            })
        
        return {
            'transcript': ' '.join(full_transcript_parts),
            'segments': segments,
            'metadata': {
                'provider': self.PROVIDER_NAME,
                'language': language_code or 'auto-detected',
                'duration': duration,
                'confidence': None,  # Azure doesn't provide overall confidence
                'region': self.speech_region,
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
        Transcribe an audio file using Azure AI Speech.
        
        Args:
            file_path: Path to the audio file
            language_code: BCP-47 language code or None for auto-detect
            enable_diarization: Enable speaker diarization
            max_speakers: Maximum number of speakers
            
        Returns:
            Standardized transcript dictionary
        """
        self.validate_parameters(max_speakers, enable_diarization)
        self.validate_file(file_path)
        validated_language = self.validate_language(language_code)
        
        try:
            if enable_diarization:
                results = self._transcribe_with_diarization(
                    file_path,
                    validated_language,
                    max_speakers
                )
            else:
                results = self._transcribe_simple(file_path, validated_language)
            
            return self._convert_to_standard_format(
                results,
                validated_language,
                enable_diarization
            )
            
        except (ValidationError, AuthenticationError, NetworkError):
            raise
        except Exception as e:
            raise wrap_provider_exception(e, 'azure')
