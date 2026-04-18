"""AWS Transcribe provider implementation."""

import json
import os
import time
import uuid
from pathlib import Path
from typing import Dict, List, Optional

import boto3
import requests
from botocore.exceptions import ClientError

from src.transcribe.base import BaseTranscriber
from src.errors import (
    ValidationError,
    AuthenticationError,
    NetworkError,
    wrap_provider_exception,
)
from src.validation.language import validate_aws_language


class AWSTranscriber(BaseTranscriber):
    """
    AWS Transcribe provider implementation.
    
    Handles audio transcription via AWS Transcribe service with S3 storage
    for audio files. Supports speaker diarization and automatic language
    detection.
    
    Required environment variables:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_REGION
    - AWS_S3_BUCKET
    """
    
    PROVIDER_NAME = "AWS Transcribe"
    SUPPORTED_FORMATS = {'amr', 'flac', 'wav', 'ogg', 'mp3', 'mp4', 'webm', 'm4a'}
    
    def __init__(self, region_name: Optional[str] = None):
        """
        Initialize AWS Transcriber.
        
        Args:
            region_name: AWS region (defaults to AWS_REGION env var)
        """
        self.region_name = region_name or os.getenv('AWS_REGION')
        self.bucket_name = os.getenv('AWS_S3_BUCKET', 'transcribeapp')
        
        # Initialize AWS clients
        try:
            if self.region_name:
                self.transcribe_client = boto3.client('transcribe', region_name=self.region_name)
                self.s3_client = boto3.client('s3', region_name=self.region_name)
            else:
                self.transcribe_client = boto3.client('transcribe')
                self.s3_client = boto3.client('s3')
        except Exception as e:
            raise wrap_provider_exception(e, 'aws')
        
        print(f"🔧 Initialized AWSTranscriber:")
        print(f"   Region: {self.region_name or 'default'}")
        print(f"   Bucket: {self.bucket_name}")
    
    def validate_language(self, language_code: Optional[str]) -> Optional[str]:
        """
        Validate language code for AWS Transcribe.
        
        AWS requires BCP-47 format (e.g., en-US, fr-FR).
        
        Args:
            language_code: BCP-47 code or None for auto-detect
            
        Returns:
            Validated code or None
            
        Raises:
            ValidationError: If invalid format or unsupported language
        """
        return validate_aws_language(language_code)
    
    def _upload_to_s3(self, file_path: str) -> str:
        """
        Upload file to S3 and return S3 URI.
        
        Args:
            file_path: Local path to audio file
            
        Returns:
            S3 URI for the uploaded file
            
        Raises:
            ValidationError: For file/bucket issues
            AuthenticationError: For permission issues
        """
        file_name = Path(file_path).name
        s3_key = f"uploads/{file_name}"
        s3_uri = f"s3://{self.bucket_name}/{s3_key}"
        
        try:
            print(f"Uploading file to S3: {self.bucket_name}/{s3_key}")
            self.s3_client.upload_file(file_path, self.bucket_name, s3_key)
            print(f"✓ Upload complete. S3 URI: {s3_uri}")
            return s3_uri
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            if error_code == 'NoSuchBucket':
                raise ValidationError(f"S3 bucket '{self.bucket_name}' does not exist")
            elif error_code in ('AccessDenied', 'InvalidAccessKeyId', 'SignatureDoesNotMatch'):
                raise AuthenticationError(
                    "Access denied to S3 bucket",
                    details="Check your AWS credentials and bucket permissions"
                )
            elif error_code == 'InvalidBucketName':
                raise ValidationError(f"Invalid S3 bucket name: '{self.bucket_name}'")
            else:
                raise ValidationError(
                    f"Failed to upload to S3: {e.response.get('Error', {}).get('Message', str(e))}"
                )
        except FileNotFoundError:
            raise ValidationError(f"Input file not found: {file_path}")
        except Exception as e:
            raise wrap_provider_exception(e, 'aws')
    
    def _cleanup_s3(self, s3_key: str) -> None:
        """Clean up uploaded S3 file."""
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
            print(f"🗑️  Cleaned up S3 file: {s3_key}")
        except Exception as e:
            print(f"⚠️  Warning: Could not delete S3 file: {e}")
    
    def _cleanup_job(self, job_name: str) -> None:
        """Clean up transcription job."""
        try:
            self.transcribe_client.delete_transcription_job(TranscriptionJobName=job_name)
            print(f"🗑️  Cleaned up transcription job: {job_name}")
        except Exception as e:
            print(f"⚠️  Warning: Could not delete transcription job: {e}")
    
    def _convert_to_standard_format(
        self, 
        aws_response: dict,
        detected_language: Optional[str] = None,
        enable_diarization: bool = True
    ) -> dict:
        """
        Convert AWS Transcribe response to standardized format.
        
        Args:
            aws_response: Raw AWS Transcribe JSON response
            detected_language: Language code (detected or specified)
            enable_diarization: Whether diarization was enabled
            
        Returns:
            Standardized transcript dictionary
        """
        results = aws_response.get('results', {})
        
        # Extract full transcript
        transcripts = results.get('transcripts', [])
        full_transcript = transcripts[0]['transcript'] if transcripts else ""
        
        # Calculate duration from items
        duration = 0.0
        items = results.get('items', [])
        for item in reversed(items):
            if 'end_time' in item:
                duration = float(item['end_time'])
                break
        
        # Extract segments with speaker labels
        segments: List[Dict] = []
        
        if enable_diarization and 'speaker_labels' in results:
            speaker_segments = results['speaker_labels'].get('segments', [])
            
            for segment in speaker_segments:
                speaker = segment.get('speaker_label', 'unknown')
                start_time = float(segment.get('start_time', 0))
                end_time = float(segment.get('end_time', 0))
                
                # Find items within this segment
                segment_text_parts = []
                for item in items:
                    if 'start_time' not in item:
                        continue
                    item_start = float(item['start_time'])
                    if start_time <= item_start <= end_time:
                        if 'alternatives' in item and item['alternatives']:
                            content = item['alternatives'][0]['content']
                            # Handle punctuation
                            if item.get('type') == 'punctuation' and segment_text_parts:
                                segment_text_parts[-1] += content
                            else:
                                segment_text_parts.append(content)
                
                segment_text = ' '.join(segment_text_parts)
                if segment_text.strip():
                    segments.append({
                        'speaker': speaker,
                        'start': start_time,
                        'end': end_time,
                        'text': segment_text.strip()
                    })
        
        # Calculate average confidence
        confidences = []
        for item in items:
            if 'alternatives' in item and item['alternatives']:
                conf = item['alternatives'][0].get('confidence')
                if conf:
                    confidences.append(float(conf))
        avg_confidence = sum(confidences) / len(confidences) if confidences else None
        
        return {
            'transcript': full_transcript,
            'segments': segments,
            'metadata': {
                'provider': self.PROVIDER_NAME,
                'language': detected_language or 'auto-detected',
                'duration': duration,
                'confidence': avg_confidence,
                'job_name': aws_response.get('jobName'),
            },
            # Keep raw response for LocalStorage compatibility
            'raw_response': aws_response
        }
    
    def transcribe(
        self,
        file_path: str,
        language_code: Optional[str] = None,
        enable_diarization: bool = True,
        max_speakers: int = 2
    ) -> dict:
        """
        Transcribe an audio file using AWS Transcribe.
        
        Args:
            file_path: Path to the audio file
            language_code: BCP-47 language code or None for auto-detect
            enable_diarization: Enable speaker diarization
            max_speakers: Maximum number of speakers (2-10)
            
        Returns:
            Standardized transcript dictionary
            
        Raises:
            ValidationError: For input validation failures
            AuthenticationError: For credential issues
            NetworkError: For API communication failures
        """
        # Validate inputs
        self.validate_parameters(max_speakers, enable_diarization)
        file_format = self.validate_file(file_path)
        validated_language = self.validate_language(language_code)
        
        job_name = f"transcription-{uuid.uuid4()}"
        s3_key: Optional[str] = None
        detected_language = validated_language
        
        try:
            # Upload to S3
            s3_uri = self._upload_to_s3(file_path)
            s3_key = s3_uri.split(f"{self.bucket_name}/")[1]
            
            print(f"Starting transcription job: {job_name}")
            
            # Prepare transcription parameters
            transcription_params = {
                'TranscriptionJobName': job_name,
                'Media': {'MediaFileUri': s3_uri},
                'MediaFormat': file_format,
                'Settings': {
                    'ShowSpeakerLabels': enable_diarization,
                    'MaxSpeakerLabels': max_speakers
                }
            }
            
            if validated_language:
                transcription_params['LanguageCode'] = validated_language
            else:
                transcription_params['IdentifyLanguage'] = True
            
            # Start transcription job
            self.transcribe_client.start_transcription_job(**transcription_params)
            
            # Poll for completion
            while True:
                status = self.transcribe_client.get_transcription_job(
                    TranscriptionJobName=job_name
                )
                job_status = status['TranscriptionJob']['TranscriptionJobStatus']
                print(f"Transcription status: {job_status}")
                
                if job_status in ['COMPLETED', 'FAILED']:
                    break
                time.sleep(5)
            
            if job_status == 'COMPLETED':
                transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
                print(f"Downloading transcript from: {transcript_uri}")
                
                # Get detected language
                if not validated_language:
                    detected_language = status['TranscriptionJob'].get('LanguageCode', 'unknown')
                    print(f"Identified language: {detected_language}")
                
                # Download transcript
                try:
                    response = requests.get(transcript_uri, timeout=30)
                    response.raise_for_status()
                    transcript_data = response.json()
                except requests.Timeout:
                    raise NetworkError(
                        "Timeout while downloading transcript",
                        details="Please try again"
                    )
                except requests.RequestException as e:
                    raise NetworkError(
                        "Failed to download transcript",
                        details=str(e)
                    )
                except json.JSONDecodeError as e:
                    raise ValidationError(
                        "Failed to parse transcript JSON",
                        details=str(e)
                    )
                
                # Cleanup job
                self._cleanup_job(job_name)
                
                # Convert to standard format
                return self._convert_to_standard_format(
                    transcript_data,
                    detected_language=detected_language,
                    enable_diarization=enable_diarization
                )
            else:
                failure_reason = status['TranscriptionJob'].get('FailureReason', 'Unknown reason')
                raise ValidationError(f"Transcription failed: {failure_reason}")
                
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            error_message = e.response.get('Error', {}).get('Message', str(e))
            
            if error_code in ('AccessDeniedException', 'InvalidAccessKeyId', 'SignatureDoesNotMatch'):
                raise AuthenticationError(
                    "AWS authentication failed",
                    details=error_message
                )
            elif error_code == 'LimitExceededException':
                raise NetworkError(
                    "AWS service limit exceeded",
                    details="Please try again later"
                )
            elif error_code == 'InternalFailureException':
                raise NetworkError(
                    "AWS internal error",
                    details="Please try again later"
                )
            elif error_code == 'ConflictException':
                raise ValidationError(
                    "A transcription job with this name already exists",
                    details="Please try again"
                )
            elif error_code == 'BadRequestException':
                raise ValidationError(
                    f"Invalid request: {error_message}"
                )
            else:
                raise ValidationError(f"AWS Transcribe error ({error_code}): {error_message}")
        
        except (ValidationError, AuthenticationError, NetworkError):
            # Re-raise our custom exceptions
            raise
        
        except Exception as e:
            raise wrap_provider_exception(e, 'aws')
        
        finally:
            # Cleanup S3 file
            if s3_key:
                self._cleanup_s3(s3_key)
