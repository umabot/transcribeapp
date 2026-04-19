"""Unit tests for ErrorHandler and custom exceptions."""

import pytest
import sys
from io import StringIO
from pathlib import Path

from src.errors import (
    ErrorHandler,
    TranscriptionError,
    ValidationError,
    AuthenticationError,
    NetworkError,
    HardwareError,
    wrap_provider_exception,
)


class TestCustomExceptions:
    """Tests for custom exception classes."""
    
    def test_validation_error_exit_code(self):
        """Test ValidationError has exit code 1."""
        err = ValidationError("Test error")
        assert err.exit_code == 1
    
    def test_authentication_error_exit_code(self):
        """Test AuthenticationError has exit code 2."""
        err = AuthenticationError("Test error")
        assert err.exit_code == 2
    
    def test_network_error_exit_code(self):
        """Test NetworkError has exit code 3."""
        err = NetworkError("Test error")
        assert err.exit_code == 3
    
    def test_hardware_error_exit_code(self):
        """Test HardwareError has exit code 4."""
        err = HardwareError("Test error")
        assert err.exit_code == 4
    
    def test_base_error_exit_code(self):
        """Test TranscriptionError has exit code 99."""
        err = TranscriptionError("Test error")
        assert err.exit_code == 99
    
    def test_error_with_details(self):
        """Test exception stores details."""
        err = ValidationError("Main message", details="Extra details")
        assert err.message == "Main message"
        assert err.details == "Extra details"


class TestErrorHandler:
    """Tests for ErrorHandler class."""
    
    def test_get_exit_code_validation(self):
        """Test exit code mapping for ValidationError."""
        handler = ErrorHandler()
        err = ValidationError("Test")
        assert handler.get_exit_code(err) == 1
    
    def test_get_exit_code_auth(self):
        """Test exit code mapping for AuthenticationError."""
        handler = ErrorHandler()
        err = AuthenticationError("Test")
        assert handler.get_exit_code(err) == 2
    
    def test_get_exit_code_network(self):
        """Test exit code mapping for NetworkError."""
        handler = ErrorHandler()
        err = NetworkError("Test")
        assert handler.get_exit_code(err) == 3
    
    def test_get_exit_code_hardware(self):
        """Test exit code mapping for HardwareError."""
        handler = ErrorHandler()
        err = HardwareError("Test")
        assert handler.get_exit_code(err) == 4
    
    def test_get_exit_code_unknown(self):
        """Test exit code mapping for unknown exception."""
        handler = ErrorHandler()
        err = RuntimeError("Test")
        assert handler.get_exit_code(err) == 99
    
    def test_format_error_message(self):
        """Test error message formatting."""
        handler = ErrorHandler()
        err = ValidationError("Invalid format")
        message = handler.format_error_message(err)
        assert "❌" in message
        assert "Invalid format" in message
    
    def test_format_error_message_with_details(self):
        """Test error message includes details."""
        handler = ErrorHandler()
        err = ValidationError("Invalid format", details="Use .mp3")
        message = handler.format_error_message(err)
        assert "Use .mp3" in message
    
    def test_write_error_file(self, tmp_path):
        """Test error logging to file."""
        error_file = tmp_path / "errors.log"
        handler = ErrorHandler(error_file=str(error_file))
        
        err = ValidationError("Test error")
        result = handler.write_error_file(err)
        
        assert result is True
        assert error_file.exists()
        content = error_file.read_text()
        assert "ValidationError" in content
        assert "Test error" in content
    
    def test_write_error_file_no_path(self):
        """Test write_error_file returns False when no path set."""
        handler = ErrorHandler()
        err = ValidationError("Test")
        assert handler.write_error_file(err) is False
    
    def test_handle_without_exit(self, capsys):
        """Test handle method without exiting."""
        handler = ErrorHandler()
        err = ValidationError("Test error")
        
        exit_code = handler.handle(err, write_log=False, exit_on_error=False)
        
        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Test error" in captured.err


class TestWrapProviderException:
    """Tests for wrap_provider_exception utility."""
    
    def test_wrap_auth_exception(self):
        """Test wrapping authentication-related exceptions."""
        original = Exception("Invalid credentials")
        wrapped = wrap_provider_exception(original, 'aws')
        
        assert isinstance(wrapped, AuthenticationError)
        assert 'AWS' in wrapped.message
    
    def test_wrap_network_exception(self):
        """Test wrapping network-related exceptions."""
        original = Exception("Connection timeout")
        wrapped = wrap_provider_exception(original, 'gcp')
        
        assert isinstance(wrapped, NetworkError)
        assert 'GCP' in wrapped.message
    
    def test_wrap_hardware_exception(self):
        """Test wrapping hardware-related exceptions."""
        original = Exception("Out of memory error")
        wrapped = wrap_provider_exception(original, 'local')
        
        assert isinstance(wrapped, HardwareError)
    
    def test_wrap_validation_exception(self):
        """Test wrapping validation-related exceptions."""
        original = Exception("Invalid format")
        wrapped = wrap_provider_exception(original, 'azure')
        
        assert isinstance(wrapped, ValidationError)
    
    def test_wrap_unknown_exception(self):
        """Test wrapping unknown exceptions."""
        original = Exception("Something weird happened")
        wrapped = wrap_provider_exception(original, 'aws')
        
        assert isinstance(wrapped, TranscriptionError)

    def test_wrap_gcp_sync_input_too_long_as_validation_error(self):
        """GCP input-limit errors should not be misclassified as hardware errors."""
        original = Exception(
            "400 Sync input too long. For audio longer than 1 min use "
            "LongRunningRecognize with a 'uri' parameter."
        )
        wrapped = wrap_provider_exception(original, 'gcp')

        assert isinstance(wrapped, ValidationError)
