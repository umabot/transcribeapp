"""Test configuration and fixtures for transcribe_app tests."""

import os
import sys
from pathlib import Path

import pytest

# Add project root to path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)


@pytest.fixture
def sample_audio_path(tmp_path):
    """Create a mock audio file path for testing."""
    audio_file = tmp_path / "test_audio.wav"
    # Create a minimal valid file (just for path testing)
    audio_file.write_bytes(b'\x00' * 100)
    return str(audio_file)


@pytest.fixture
def output_path(tmp_path):
    """Create output path for testing."""
    return str(tmp_path / "output.md")


@pytest.fixture
def mock_aws_env(monkeypatch):
    """Set mock AWS environment variables."""
    monkeypatch.setenv('AWS_ACCESS_KEY_ID', 'test_key')
    monkeypatch.setenv('AWS_SECRET_ACCESS_KEY', 'test_secret')
    monkeypatch.setenv('AWS_REGION', 'us-east-1')
    monkeypatch.setenv('AWS_S3_BUCKET', 'test-bucket')


@pytest.fixture
def mock_gcp_env(monkeypatch, tmp_path):
    """Set mock GCP environment variables."""
    creds_file = tmp_path / "gcp_creds.json"
    creds_file.write_text('{"type": "service_account"}')
    monkeypatch.setenv('GOOGLE_APPLICATION_CREDENTIALS', str(creds_file))
    monkeypatch.setenv('GCP_STORAGE_BUCKET', 'test-gcp-bucket')


@pytest.fixture
def mock_azure_env(monkeypatch):
    """Set mock Azure environment variables."""
    monkeypatch.setenv('AZURE_SPEECH_KEY', 'test_azure_key')
    monkeypatch.setenv('AZURE_SPEECH_REGION', 'eastus')


@pytest.fixture
def standardized_transcript():
    """Return a sample standardized transcript format."""
    return {
        'transcript': 'Hello, how are you? I am fine, thank you.',
        'segments': [
            {
                'speaker': 'spk_0',
                'start': 0.0,
                'end': 1.5,
                'text': 'Hello, how are you?'
            },
            {
                'speaker': 'spk_1',
                'start': 1.8,
                'end': 3.2,
                'text': 'I am fine, thank you.'
            }
        ],
        'metadata': {
            'provider': 'Test Provider',
            'language': 'en-US',
            'duration': 3.2,
            'confidence': 0.95
        }
    }


@pytest.fixture
def aws_raw_transcript():
    """Return a sample AWS raw transcript format."""
    return {
        'results': {
            'transcripts': [
                {'transcript': 'Hello, how are you? I am fine, thank you.'}
            ],
            'items': [
                {
                    'start_time': '0.0',
                    'end_time': '0.5',
                    'alternatives': [{'content': 'Hello', 'confidence': '0.95'}],
                    'type': 'pronunciation'
                },
                {
                    'alternatives': [{'content': ','}],
                    'type': 'punctuation'
                },
                {
                    'start_time': '0.6',
                    'end_time': '0.8',
                    'alternatives': [{'content': 'how', 'confidence': '0.92'}],
                    'type': 'pronunciation'
                },
                {
                    'start_time': '0.9',
                    'end_time': '1.0',
                    'alternatives': [{'content': 'are', 'confidence': '0.98'}],
                    'type': 'pronunciation'
                },
                {
                    'start_time': '1.1',
                    'end_time': '1.5',
                    'alternatives': [{'content': 'you', 'confidence': '0.99'}],
                    'type': 'pronunciation'
                }
            ],
            'speaker_labels': {
                'segments': [
                    {
                        'speaker_label': 'spk_0',
                        'start_time': '0.0',
                        'end_time': '1.5'
                    }
                ]
            }
        }
    }
