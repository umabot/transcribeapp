"""Unit tests for language validation utilities."""

import pytest

from src.validation.language import (
    validate_bcp47,
    validate_iso639,
    validate_aws_language,
    validate_gcp_language,
    validate_azure_language,
    validate_whisper_language,
)
from src.errors import ValidationError


class TestBCP47Validation:
    """Tests for BCP-47 language code validation."""
    
    def test_valid_bcp47_codes(self):
        """Test that valid BCP-47 codes pass validation."""
        valid_codes = ['en-US', 'fr-FR', 'es-ES', 'de-DE', 'ja-JP', 'zh-CN']
        for code in valid_codes:
            result = validate_bcp47(code)
            assert result == code
    
    def test_bcp47_normalization(self):
        """Test that codes are normalized to correct case."""
        assert validate_bcp47('EN-us') == 'en-US'
        assert validate_bcp47('FR-fr') == 'fr-FR'
        assert validate_bcp47('es-es') == 'es-ES'
    
    def test_invalid_bcp47_format(self):
        """Test that invalid formats raise ValidationError."""
        invalid_codes = ['en', 'english', 'en_US', 'en-USA', '']
        for code in invalid_codes:
            with pytest.raises(ValidationError):
                validate_bcp47(code)
    
    def test_empty_code_raises_error(self):
        """Test that empty string raises ValidationError."""
        with pytest.raises(ValidationError):
            validate_bcp47('')


class TestISO639Validation:
    """Tests for ISO-639-1 language code validation."""
    
    def test_valid_iso639_codes(self):
        """Test that valid ISO-639-1 codes pass validation."""
        valid_codes = ['en', 'fr', 'es', 'de', 'ja', 'zh']
        for code in valid_codes:
            result = validate_iso639(code)
            assert result == code.lower()
    
    def test_iso639_normalization(self):
        """Test that codes are normalized to lowercase."""
        assert validate_iso639('EN') == 'en'
        assert validate_iso639('Fr') == 'fr'
    
    def test_invalid_iso639_format(self):
        """Test that invalid formats raise ValidationError."""
        invalid_codes = ['eng', 'en-US', 'english', '1', '']
        for code in invalid_codes:
            with pytest.raises(ValidationError):
                validate_iso639(code)


class TestAWSLanguageValidation:
    """Tests for AWS Transcribe language validation."""
    
    def test_valid_aws_languages(self):
        """Test that valid AWS language codes pass."""
        valid_codes = ['en-US', 'fr-FR', 'es-ES', 'ja-JP']
        for code in valid_codes:
            result = validate_aws_language(code)
            assert result == code
    
    def test_none_returns_none(self):
        """Test that None (auto-detect) is allowed."""
        assert validate_aws_language(None) is None
    
    def test_unsupported_aws_language(self):
        """Test that unsupported language raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            validate_aws_language('xx-XX')
        assert 'not supported by AWS' in str(exc_info.value)


class TestGCPLanguageValidation:
    """Tests for GCP Speech-to-Text language validation."""
    
    def test_valid_gcp_languages(self):
        """Test that valid GCP language codes pass."""
        valid_codes = ['en-US', 'en-GB', 'fr-FR']
        for code in valid_codes:
            result = validate_gcp_language(code)
            assert result == code
    
    def test_none_returns_none(self):
        """Test that None (auto-detect) is allowed."""
        assert validate_gcp_language(None) is None


class TestAzureLanguageValidation:
    """Tests for Azure Speech language validation."""
    
    def test_valid_azure_languages(self):
        """Test that valid Azure language codes pass."""
        valid_codes = ['en-US', 'de-DE', 'it-IT']
        for code in valid_codes:
            result = validate_azure_language(code)
            assert result == code
    
    def test_none_returns_none(self):
        """Test that None (auto-detect) is allowed."""
        assert validate_azure_language(None) is None


class TestWhisperLanguageValidation:
    """Tests for local Whisper language validation."""
    
    def test_valid_whisper_languages(self):
        """Test that valid Whisper language codes pass."""
        valid_codes = ['en', 'fr', 'es', 'de', 'ja', 'zh']
        for code in valid_codes:
            result = validate_whisper_language(code)
            assert result == code
    
    def test_none_returns_none(self):
        """Test that None (auto-detect) is allowed."""
        assert validate_whisper_language(None) is None
    
    def test_bcp47_rejected_for_whisper(self):
        """Test that BCP-47 codes are rejected for Whisper."""
        with pytest.raises(ValidationError) as exc_info:
            validate_whisper_language('en-US')
        assert 'ISO-639-1' in str(exc_info.value)
