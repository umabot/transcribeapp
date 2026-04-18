"""Integration tests for AWS Transcriber with mocked AWS services."""

import pytest
from unittest.mock import Mock, patch, MagicMock

from src.transcribe.providers.aws import AWSTranscriber
from src.errors import ValidationError, AuthenticationError, NetworkError


class TestAWSTranscriberIntegration:
    """Integration tests for AWSTranscriber with mocked AWS."""
    
    @pytest.fixture
    def mock_boto3(self):
        """Create mock boto3 clients."""
        with patch('src.transcribe.providers.aws.boto3') as mock:
            # Setup mock clients
            mock_s3 = MagicMock()
            mock_transcribe = MagicMock()
            
            mock.client.side_effect = lambda service, **kwargs: {
                's3': mock_s3,
                'transcribe': mock_transcribe
            }[service]
            
            yield {
                'boto3': mock,
                's3': mock_s3,
                'transcribe': mock_transcribe
            }
    
    def test_transcriber_initialization(self, mock_aws_env, mock_boto3):
        """Test AWSTranscriber initializes correctly."""
        transcriber = AWSTranscriber()
        
        assert transcriber.PROVIDER_NAME == "AWS Transcribe"
        assert transcriber.region_name == 'us-east-1'
        assert transcriber.bucket_name == 'test-bucket'
    
    def test_validate_language_valid(self, mock_aws_env, mock_boto3):
        """Test language validation with valid code."""
        transcriber = AWSTranscriber()
        
        result = transcriber.validate_language('en-US')
        assert result == 'en-US'
    
    def test_validate_language_none(self, mock_aws_env, mock_boto3):
        """Test language validation with None (auto-detect)."""
        transcriber = AWSTranscriber()
        
        result = transcriber.validate_language(None)
        assert result is None
    
    def test_validate_language_invalid_format(self, mock_aws_env, mock_boto3):
        """Test language validation with invalid format."""
        transcriber = AWSTranscriber()
        
        with pytest.raises(ValidationError) as exc_info:
            transcriber.validate_language('en')  # ISO-639-1 not allowed
        assert 'BCP-47' in str(exc_info.value)
    
    def test_upload_to_s3_success(self, mock_aws_env, mock_boto3, tmp_path):
        """Test successful S3 upload."""
        transcriber = AWSTranscriber()
        
        audio_file = tmp_path / "test.wav"
        audio_file.write_bytes(b'\x00' * 100)
        
        s3_uri = transcriber._upload_to_s3(str(audio_file))
        
        assert s3_uri.startswith('s3://test-bucket/')
        mock_boto3['s3'].upload_file.assert_called_once()
    
    def test_upload_to_s3_bucket_not_found(self, mock_aws_env, mock_boto3, tmp_path):
        """Test S3 upload failure when bucket doesn't exist."""
        from botocore.exceptions import ClientError
        
        mock_boto3['s3'].upload_file.side_effect = ClientError(
            {'Error': {'Code': 'NoSuchBucket', 'Message': 'Bucket not found'}},
            'upload_file'
        )
        
        transcriber = AWSTranscriber()
        
        audio_file = tmp_path / "test.wav"
        audio_file.write_bytes(b'\x00' * 100)
        
        with pytest.raises(ValidationError) as exc_info:
            transcriber._upload_to_s3(str(audio_file))
        assert 'does not exist' in str(exc_info.value)
    
    def test_upload_to_s3_access_denied(self, mock_aws_env, mock_boto3, tmp_path):
        """Test S3 upload failure on access denied."""
        from botocore.exceptions import ClientError
        
        mock_boto3['s3'].upload_file.side_effect = ClientError(
            {'Error': {'Code': 'AccessDenied', 'Message': 'Access Denied'}},
            'upload_file'
        )
        
        transcriber = AWSTranscriber()
        
        audio_file = tmp_path / "test.wav"
        audio_file.write_bytes(b'\x00' * 100)
        
        with pytest.raises(AuthenticationError):
            transcriber._upload_to_s3(str(audio_file))
    
    def test_convert_to_standard_format(self, mock_aws_env, mock_boto3):
        """Test AWS response conversion to standard format."""
        transcriber = AWSTranscriber()
        
        aws_response = {
            'results': {
                'transcripts': [{'transcript': 'Hello world'}],
                'items': [
                    {
                        'start_time': '0.0',
                        'end_time': '0.5',
                        'alternatives': [{'content': 'Hello', 'confidence': '0.95'}],
                        'type': 'pronunciation'
                    },
                    {
                        'start_time': '0.6',
                        'end_time': '1.0',
                        'alternatives': [{'content': 'world', 'confidence': '0.98'}],
                        'type': 'pronunciation'
                    }
                ],
                'speaker_labels': {
                    'segments': [
                        {'speaker_label': 'spk_0', 'start_time': '0.0', 'end_time': '1.0'}
                    ]
                }
            }
        }
        
        result = transcriber._convert_to_standard_format(
            aws_response,
            detected_language='en-US',
            enable_diarization=True
        )
        
        assert 'transcript' in result
        assert 'segments' in result
        assert 'metadata' in result
        assert result['metadata']['provider'] == 'AWS Transcribe'
        assert result['metadata']['language'] == 'en-US'


class TestAWSTranscriberTranscribe:
    """Tests for full transcription flow with mocked AWS."""
    
    @pytest.fixture
    def mock_full_aws(self, mock_aws_env):
        """Create fully mocked AWS setup for transcription."""
        with patch('src.transcribe.providers.aws.boto3') as mock_boto3, \
             patch('src.transcribe.providers.aws.requests') as mock_requests:
            
            mock_s3 = MagicMock()
            mock_transcribe = MagicMock()
            
            mock_boto3.client.side_effect = lambda service, **kwargs: {
                's3': mock_s3,
                'transcribe': mock_transcribe
            }[service]
            
            # Setup transcription job response
            mock_transcribe.get_transcription_job.return_value = {
                'TranscriptionJob': {
                    'TranscriptionJobStatus': 'COMPLETED',
                    'LanguageCode': 'en-US',
                    'Transcript': {
                        'TranscriptFileUri': 'https://s3.amazonaws.com/transcript.json'
                    }
                }
            }
            
            # Setup transcript download
            mock_response = MagicMock()
            mock_response.json.return_value = {
                'results': {
                    'transcripts': [{'transcript': 'Test transcript'}],
                    'items': [],
                    'speaker_labels': {'segments': []}
                }
            }
            mock_requests.get.return_value = mock_response
            
            yield {
                'boto3': mock_boto3,
                's3': mock_s3,
                'transcribe': mock_transcribe,
                'requests': mock_requests
            }
    
    def test_transcribe_success(self, mock_full_aws, tmp_path):
        """Test successful transcription flow."""
        audio_file = tmp_path / "test.wav"
        audio_file.write_bytes(b'\x00' * 100)
        
        transcriber = AWSTranscriber()
        result = transcriber.transcribe(
            file_path=str(audio_file),
            language_code='en-US',
            enable_diarization=True,
            max_speakers=2
        )
        
        assert 'transcript' in result
        assert 'segments' in result
        assert 'metadata' in result
        
        # Verify AWS calls
        mock_full_aws['s3'].upload_file.assert_called_once()
        mock_full_aws['transcribe'].start_transcription_job.assert_called_once()
