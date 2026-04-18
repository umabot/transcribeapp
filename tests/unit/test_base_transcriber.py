"""Unit tests for BaseTranscriber abstract class."""

import pytest
from pathlib import Path

from src.transcribe.base import BaseTranscriber
from src.errors import ValidationError


class ConcreteTranscriber(BaseTranscriber):
    """Concrete implementation for testing BaseTranscriber."""
    
    PROVIDER_NAME = "Test Provider"
    SUPPORTED_FORMATS = {'wav', 'mp3', 'flac'}
    
    def validate_language(self, language_code):
        return language_code
    
    def transcribe(self, file_path, language_code=None, enable_diarization=True, max_speakers=2):
        return {
            'transcript': 'Test transcript',
            'segments': [],
            'metadata': {'provider': self.PROVIDER_NAME}
        }


class TestBaseTranscriberValidation:
    """Tests for BaseTranscriber validation methods."""
    
    def test_validate_file_exists(self, tmp_path):
        """Test validation passes for existing file."""
        transcriber = ConcreteTranscriber()
        
        audio_file = tmp_path / "test.wav"
        audio_file.write_bytes(b'\x00' * 100)
        
        result = transcriber.validate_file(str(audio_file))
        assert result == 'wav'
    
    def test_validate_file_not_found(self):
        """Test validation fails for non-existent file."""
        transcriber = ConcreteTranscriber()
        
        with pytest.raises(ValidationError) as exc_info:
            transcriber.validate_file('/nonexistent/path/audio.wav')
        assert 'not found' in str(exc_info.value).lower()
    
    def test_validate_file_is_directory(self, tmp_path):
        """Test validation fails for directory path."""
        transcriber = ConcreteTranscriber()
        
        with pytest.raises(ValidationError) as exc_info:
            transcriber.validate_file(str(tmp_path))
        assert 'not a file' in str(exc_info.value).lower()
    
    def test_validate_file_no_extension(self, tmp_path):
        """Test validation fails for file without extension."""
        transcriber = ConcreteTranscriber()
        
        audio_file = tmp_path / "testfile"
        audio_file.write_bytes(b'\x00' * 100)
        
        with pytest.raises(ValidationError) as exc_info:
            transcriber.validate_file(str(audio_file))
        assert 'no extension' in str(exc_info.value).lower()
    
    def test_validate_file_unsupported_format(self, tmp_path):
        """Test validation fails for unsupported format."""
        transcriber = ConcreteTranscriber()
        
        audio_file = tmp_path / "test.xyz"
        audio_file.write_bytes(b'\x00' * 100)
        
        with pytest.raises(ValidationError) as exc_info:
            transcriber.validate_file(str(audio_file))
        assert 'unsupported' in str(exc_info.value).lower()
    
    def test_validate_file_supported_formats_in_error(self, tmp_path):
        """Test error message includes supported formats."""
        transcriber = ConcreteTranscriber()
        
        audio_file = tmp_path / "test.xyz"
        audio_file.write_bytes(b'\x00' * 100)
        
        with pytest.raises(ValidationError) as exc_info:
            transcriber.validate_file(str(audio_file))
        
        error_msg = str(exc_info.value).lower()
        assert 'wav' in error_msg or 'mp3' in error_msg


class TestBaseTranscriberParameters:
    """Tests for BaseTranscriber parameter validation."""
    
    def test_validate_parameters_valid_diarization(self):
        """Test valid parameters with diarization."""
        transcriber = ConcreteTranscriber()
        
        # Should not raise
        transcriber.validate_parameters(max_speakers=2, enable_diarization=True)
        transcriber.validate_parameters(max_speakers=5, enable_diarization=True)
        transcriber.validate_parameters(max_speakers=10, enable_diarization=True)
    
    def test_validate_parameters_valid_no_diarization(self):
        """Test valid parameters without diarization."""
        transcriber = ConcreteTranscriber()
        
        # Should not raise
        transcriber.validate_parameters(max_speakers=1, enable_diarization=False)
    
    def test_validate_parameters_invalid_speakers_with_diarization(self):
        """Test invalid speaker count with diarization."""
        transcriber = ConcreteTranscriber()
        
        with pytest.raises(ValidationError):
            transcriber.validate_parameters(max_speakers=1, enable_diarization=True)
        
        with pytest.raises(ValidationError):
            transcriber.validate_parameters(max_speakers=11, enable_diarization=True)
    
    def test_validate_parameters_invalid_speakers_without_diarization(self):
        """Test invalid speaker count without diarization."""
        transcriber = ConcreteTranscriber()
        
        with pytest.raises(ValidationError):
            transcriber.validate_parameters(max_speakers=2, enable_diarization=False)
