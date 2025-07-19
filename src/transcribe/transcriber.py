import boto3
import time
from botocore.exceptions import ClientError
import uuid
import json
import requests
from pathlib import Path
import os

class AWSTranscriber:
    # AWS Transcribe supported formats
    SUPPORTED_FORMATS = {'amr', 'flac', 'wav', 'ogg', 'mp3', 'mp4', 'webm', 'm4a'}
    
    def __init__(self):
        self.transcribe_client = boto3.client('transcribe')
        self.s3_client = boto3.client('s3')
        self.bucket_name = os.getenv('AWS_S3_BUCKET', 'transcribeapp')
    
    def _validate_file_format(self, file_path: str) -> str:
        """Validate file format and return the format string for AWS"""
        file_extension = Path(file_path).suffix[1:].lower()  # Remove dot and lowercase
        
        if not file_extension:
            raise ValueError("File has no extension")
            
        if file_extension not in self.SUPPORTED_FORMATS:
            supported_list = ', '.join(sorted(self.SUPPORTED_FORMATS))
            raise ValueError(
                f"Unsupported file format: '{file_extension}'. "
                f"AWS Transcribe supports: {supported_list}"
            )
        
        return file_extension
    
    def _validate_parameters(self, max_speakers: int):
        """Validate input parameters"""
        if max_speakers < 1 or max_speakers > 10:
            raise ValueError("max_speakers must be between 1 and 10")

    def upload_to_s3(self, file_path: str) -> str:
        """Upload file to S3 and return S3 URI"""
        file_name = Path(file_path).name
        s3_key = f"uploads/{file_name}"
        
        try:
            print(f"Uploading file to S3: {self.bucket_name}/{s3_key}")
            self.s3_client.upload_file(file_path, self.bucket_name, s3_key)
            return f"s3://{self.bucket_name}/{s3_key}"
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            if error_code == 'NoSuchBucket':
                raise ValueError(f"S3 bucket '{self.bucket_name}' does not exist")
            elif error_code == 'AccessDenied':
                raise ValueError("Access denied to S3 bucket. Check your AWS credentials and permissions")
            elif error_code == 'InvalidBucketName':
                raise ValueError(f"Invalid S3 bucket name: '{self.bucket_name}'")
            else:
                raise ValueError(f"Failed to upload to S3: {e.response.get('Error', {}).get('Message', str(e))}")
        except FileNotFoundError:
            raise ValueError(f"Input file not found: {file_path}")
        except Exception as e:
            raise ValueError(f"Unexpected error during S3 upload: {e}")

    def transcribe_file(self, input_file: str, language_code: str = None, enable_diarization: bool = True, max_speakers: int = 2) -> str:
        # Validate inputs
        self._validate_parameters(max_speakers)
        file_format = self._validate_file_format(input_file)
        
        job_name = f"transcription-{uuid.uuid4()}"
        
        try:
            # First upload the file to S3
            s3_uri = self.upload_to_s3(input_file)
            
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
            
            # If language_code is provided, use it. Otherwise, enable automatic language identification
            if language_code:
                transcription_params['LanguageCode'] = language_code
            else:
                transcription_params['IdentifyLanguage'] = True
                # Optionally, you can specify the language options to limit the detection
                # transcription_params['LanguageOptions'] = ['en-US', 'es-ES', 'fr-FR']
            
            # Start transcription job
            response = self.transcribe_client.start_transcription_job(**transcription_params)
            
            # Wait for completion
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
                # Get the transcript URL
                transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
                print(f"Downloading transcript from: {transcript_uri}")
                
                # Get the identified language if automatic detection was used
                if not language_code:
                    identified_language = status['TranscriptionJob'].get('LanguageCode', 'unknown')
                    print(f"Identified language: {identified_language}")
                
                # Download and parse the JSON
                try:
                    response = requests.get(transcript_uri)
                    response.raise_for_status()
                    transcript_data = response.json()
                    return transcript_data
                except requests.RequestException as e:
                    raise ValueError(f"Failed to download transcript: {e}")
                except json.JSONDecodeError as e:
                    raise ValueError(f"Failed to parse transcript JSON: {e}")
            else:
                failure_reason = status['TranscriptionJob'].get('FailureReason', 'Unknown reason')
                raise ValueError(f"Transcription failed: {failure_reason}")
                
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            error_message = e.response.get('Error', {}).get('Message', str(e))
            
            if error_code == 'BadRequestException':
                if 'mediaFormat' in error_message:
                    raise ValueError("Invalid media format. Please check that your file is in a supported format")
                elif 'validation error' in error_message.lower():
                    raise ValueError(f"Invalid request parameters: {error_message}")
                else:
                    raise ValueError(f"Bad request: {error_message}")
            elif error_code == 'AccessDeniedException':
                raise ValueError("Access denied. Check your AWS credentials and transcription permissions")
            elif error_code == 'LimitExceededException':
                raise ValueError("AWS service limit exceeded. Please try again later")
            elif error_code == 'InternalFailureException':
                raise ValueError("AWS internal error. Please try again later")
            elif error_code == 'ConflictException':
                raise ValueError("A transcription job with this name already exists. Please try again")
            else:
                raise ValueError(f"AWS Transcribe error ({error_code}): {error_message}")