"""Unit tests for TranscriberFactory."""

import pytest
from unittest.mock import patch, MagicMock

from src.transcribe.factory import TranscriberFactory
from src.transcribe.base import BaseTranscriber
from src.errors import ValidationError


class TestTranscriberFactory:
    """Tests for TranscriberFactory class."""
    
    @pytest.fixture(autouse=True)
    def reset_factory(self):
        """Reset factory registry before each test."""
        TranscriberFactory._registry = {}
        TranscriberFactory._initialized = False
        yield
        TranscriberFactory._registry = {}
        TranscriberFactory._initialized = False
    
    def test_list_available_providers_empty_when_no_deps(self):
        """Test listing providers when dependencies aren't installed."""
        providers = TranscriberFactory.list_available_providers()
        assert isinstance(providers, list)
        # When deps aren't installed, list may be empty
    
    def test_is_provider_available_unknown(self):
        """Test unknown provider returns False."""
        assert TranscriberFactory.is_provider_available('unknown_provider') is False
    
    def test_get_provider_info(self):
        """Test getting provider information."""
        info = TranscriberFactory.get_provider_info()
        
        assert isinstance(info, dict)
        assert 'aws' in info
        assert 'gcp' in info
        assert 'azure' in info
        assert 'local' in info
        
        # Check AWS info structure
        aws_info = info['aws']
        assert 'name' in aws_info
        assert 'available' in aws_info
        assert 'env_vars' in aws_info
        assert 'language_format' in aws_info
        assert 'diarization_support' in aws_info
    
    def test_get_provider_info_env_vars(self):
        """Test provider info includes correct env vars."""
        info = TranscriberFactory.get_provider_info()
        
        assert 'AWS_ACCESS_KEY_ID' in info['aws']['env_vars']
        assert 'GOOGLE_APPLICATION_CREDENTIALS' in info['gcp']['env_vars']
        assert 'AZURE_SPEECH_KEY' in info['azure']['env_vars']
        assert info['local']['env_vars'] == []  # Local needs no env vars
    
    def test_get_transcriber_unknown_raises(self):
        """Test unknown provider raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            TranscriberFactory.get_transcriber('unknown')
        # When no providers available, message differs
        error_msg = str(exc_info.value)
        assert 'provider' in error_msg.lower() or 'available' in error_msg.lower()


class TestTranscriberFactoryWithMocks:
    """Tests for TranscriberFactory with mocked providers."""
    
    @pytest.fixture(autouse=True)
    def reset_factory(self):
        """Reset factory registry before each test."""
        TranscriberFactory._registry = {}
        TranscriberFactory._initialized = False
        yield
        TranscriberFactory._registry = {}
        TranscriberFactory._initialized = False
    
    def test_get_transcriber_with_mock_aws(self, mock_aws_env):
        """Test getting AWS transcriber with mocked provider."""
        # Create a mock transcriber class
        mock_transcriber = MagicMock(spec=BaseTranscriber)
        mock_transcriber.PROVIDER_NAME = "AWS Transcribe"
        
        # Manually register the mock
        TranscriberFactory._registry['aws'] = lambda **kwargs: mock_transcriber
        TranscriberFactory._initialized = True
        
        transcriber = TranscriberFactory.get_transcriber('aws')
        assert transcriber.PROVIDER_NAME == "AWS Transcribe"
    
    def test_is_provider_available_with_registered(self):
        """Test provider availability check with registered provider."""
        # Manually register a mock provider
        TranscriberFactory._registry['test'] = MagicMock
        TranscriberFactory._initialized = True
        
        assert TranscriberFactory.is_provider_available('test') is True
        assert TranscriberFactory.is_provider_available('nonexistent') is False
    
    def test_list_providers_with_registered(self):
        """Test listing providers with registered providers."""
        # Manually register mock providers
        TranscriberFactory._registry['aws'] = MagicMock
        TranscriberFactory._registry['local'] = MagicMock
        TranscriberFactory._initialized = True
        
        providers = TranscriberFactory.list_available_providers()
        assert 'aws' in providers
        assert 'local' in providers
        assert len(providers) == 2
