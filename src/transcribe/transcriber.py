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

    def transcribe_file(self, input_file: str) -> str:
        job_name = f"transcription-{uuid.uuid4()}"
        file_format = Path(input_file).suffix[1:]  # Remove the dot from extension
        
        try:
            # First upload the file to S3
            s3_uri = self.upload_to_s3(input_file)
            
            print(f"Starting transcription job: {job_name}")
            # Start transcription job
            response = self.transcribe_client.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={'MediaFileUri': s3_uri},
                MediaFormat=file_format,
                LanguageCode='en-US'
            )
            
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
        finally:
            # Cleanup: Delete the audio file from S3
            try:
                self.s3_client.delete_object(
                    Bucket=self.bucket_name,
                    Key=f"uploads/{Path(input_file).name}"
                )
                print("Cleaned up temporary S3 file")
            except Exception as e:
                print(f"Warning: Could not delete temporary S3 file: {e}")