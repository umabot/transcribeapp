import boto3
import time
from botocore.exceptions import ClientError
import uuid
import json
import requests
from pathlib import Path
import os

class AWSTranscriber:
    def __init__(self):
        self.transcribe_client = boto3.client('transcribe')
        self.s3_client = boto3.client('s3')
        self.bucket_name = os.getenv('AWS_S3_BUCKET', 'transcribeapp')
        
    def upload_to_s3(self, file_path: str) -> str:
        """Upload file to S3 and return S3 URI"""
        file_name = Path(file_path).name
        s3_key = f"uploads/{file_name}"
        
        try:
            print(f"Uploading file to S3: {self.bucket_name}/{s3_key}")
            self.s3_client.upload_file(file_path, self.bucket_name, s3_key)
            return f"s3://{self.bucket_name}/{s3_key}"
        except ClientError as e:
            print(f"Error uploading to S3: {e}")
            raise

    def transcribe_file(self, input_file: str, language_code: str = None) -> str:
        job_name = f"transcription-{uuid.uuid4()}"
        file_format = Path(input_file).suffix[1:]  # Remove the dot from extension
        
        try:
            # First upload the file to S3
            s3_uri = self.upload_to_s3(input_file)
            
            print(f"Starting transcription job: {job_name}")
            # Prepare transcription parameters
            transcription_params = {
                'TranscriptionJobName': job_name,
                'Media': {'MediaFileUri': s3_uri},
                'MediaFormat': file_format,
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
                response = requests.get(transcript_uri)
                transcript_data = response.json()
                
                # Extract the actual transcript text
                transcript_text = transcript_data['results']['transcripts'][0]['transcript']
                return transcript_text
            else:
                raise Exception(f"Transcription failed with status: {job_status}")
                
        except ClientError as e:
            print(f"AWS Error: {e}")
            raise