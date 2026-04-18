"""Unit tests for LocalStorage."""

import pytest
from pathlib import Path

from src.storage.local import LocalStorage


class TestLocalStorageStandardFormat:
    """Tests for LocalStorage with standardized format."""
    
    def test_save_markdown_creates_file(self, tmp_path, standardized_transcript):
        """Test that save_markdown creates output file."""
        input_file = tmp_path / "test.wav"
        input_file.write_bytes(b'\x00' * 1000)
        output_file = tmp_path / "output.md"
        
        LocalStorage.save_markdown(
            transcript_data=standardized_transcript,
            output_file=str(output_file),
            input_file=str(input_file)
        )
        
        assert output_file.exists()
    
    def test_save_markdown_content(self, tmp_path, standardized_transcript):
        """Test markdown content structure."""
        input_file = tmp_path / "test.wav"
        input_file.write_bytes(b'\x00' * 1000)
        output_file = tmp_path / "output.md"
        
        LocalStorage.save_markdown(
            transcript_data=standardized_transcript,
            output_file=str(output_file),
            input_file=str(input_file),
            language='en-US',
            speakers=2,
            diarization=True
        )
        
        content = output_file.read_text()
        
        # Check sections exist
        assert '# Transcription' in content
        assert '## Metadata' in content
        assert '## System Information' in content
        assert '## Processing Information' in content
        assert '## Content' in content
        
        # Check metadata
        assert 'test.wav' in content
        assert 'en-US' in content
    
    def test_save_markdown_with_diarization(self, tmp_path, standardized_transcript):
        """Test diarization formatting in output."""
        input_file = tmp_path / "test.wav"
        input_file.write_bytes(b'\x00' * 1000)
        output_file = tmp_path / "output.md"
        
        LocalStorage.save_markdown(
            transcript_data=standardized_transcript,
            output_file=str(output_file),
            input_file=str(input_file),
            diarization=True
        )
        
        content = output_file.read_text()
        assert '**spk_0**' in content
        assert '**spk_1**' in content
    
    def test_save_markdown_without_diarization(self, tmp_path, standardized_transcript):
        """Test plain transcript without diarization."""
        input_file = tmp_path / "test.wav"
        input_file.write_bytes(b'\x00' * 1000)
        output_file = tmp_path / "output.md"
        
        LocalStorage.save_markdown(
            transcript_data=standardized_transcript,
            output_file=str(output_file),
            input_file=str(input_file),
            diarization=False
        )
        
        content = output_file.read_text()
        # Plain transcript should be used
        assert 'Hello, how are you?' in content
    
    def test_save_markdown_creates_parent_dirs(self, tmp_path, standardized_transcript):
        """Test that parent directories are created."""
        input_file = tmp_path / "test.wav"
        input_file.write_bytes(b'\x00' * 1000)
        output_file = tmp_path / "subdir" / "nested" / "output.md"
        
        LocalStorage.save_markdown(
            transcript_data=standardized_transcript,
            output_file=str(output_file),
            input_file=str(input_file)
        )
        
        assert output_file.exists()


class TestLocalStorageAWSFormat:
    """Tests for LocalStorage with AWS raw format (backward compatibility)."""
    
    def test_save_markdown_aws_format(self, tmp_path, aws_raw_transcript):
        """Test that AWS raw format is processed correctly."""
        input_file = tmp_path / "test.wav"
        input_file.write_bytes(b'\x00' * 1000)
        output_file = tmp_path / "output.md"
        
        LocalStorage.save_markdown(
            transcript_data=aws_raw_transcript,
            output_file=str(output_file),
            input_file=str(input_file),
            diarization=True
        )
        
        content = output_file.read_text()
        assert '**spk_0**' in content
        assert 'Hello' in content


class TestLocalStorageHelpers:
    """Tests for LocalStorage helper methods."""
    
    def test_is_standardized_format_true(self, standardized_transcript):
        """Test detection of standardized format."""
        assert LocalStorage._is_standardized_format(standardized_transcript) is True
    
    def test_is_standardized_format_false(self, aws_raw_transcript):
        """Test detection rejects AWS format."""
        assert LocalStorage._is_standardized_format(aws_raw_transcript) is False
    
    def test_is_standardized_format_empty(self):
        """Test detection rejects empty dict."""
        assert LocalStorage._is_standardized_format({}) is False
