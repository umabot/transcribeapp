"""Centralized error handling for multi-cloud transcription CLI."""

import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional, Type


class TranscriptionError(Exception):
    """Base exception for all transcription errors."""
    exit_code = 99
    
    def __init__(self, message: str, details: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.details = details


class ValidationError(TranscriptionError):
    """
    Raised for validation failures.
    
    Examples:
    - Unsupported file format
    - Invalid language code
    - Invalid parameter values
    """
    exit_code = 1


class AuthenticationError(TranscriptionError):
    """
    Raised for authentication/authorization failures.
    
    Examples:
    - Invalid API keys
    - Missing credentials
    - Insufficient permissions
    """
    exit_code = 2


class NetworkError(TranscriptionError):
    """
    Raised for network and API communication failures.
    
    Examples:
    - Connection timeout
    - API rate limiting
    - Service unavailable
    """
    exit_code = 3


class HardwareError(TranscriptionError):
    """
    Raised for local hardware requirement failures.
    
    Examples:
    - Insufficient RAM for model
    - No Apple Neural Engine found
    - GPU not available
    """
    exit_code = 4


class ErrorHandler:
    """
    Centralized error handler for mapping exceptions to user-friendly
    messages and standardized exit codes.
    """
    
    # Map exception types to exit codes
    EXIT_CODES = {
        ValidationError: 1,
        AuthenticationError: 2,
        NetworkError: 3,
        HardwareError: 4,
        Exception: 99,  # Catch-all for unexpected errors
    }
    
    # Map common external exceptions to our custom types
    EXCEPTION_MAPPING = {
        FileNotFoundError: (ValidationError, "File not found"),
        PermissionError: (ValidationError, "Permission denied"),
        ConnectionError: (NetworkError, "Connection failed"),
        TimeoutError: (NetworkError, "Request timed out"),
    }
    
    def __init__(self, error_file: Optional[str] = None):
        """
        Initialize error handler.
        
        Args:
            error_file: Optional path to write detailed error logs
        """
        self.error_file = Path(error_file) if error_file else None
    
    def get_exit_code(self, exception: Exception) -> int:
        """
        Get the appropriate exit code for an exception.
        
        Args:
            exception: The exception to map
            
        Returns:
            Exit code (1-99)
        """
        for exc_type, code in self.EXIT_CODES.items():
            if isinstance(exception, exc_type):
                return code
        return 99
    
    def format_error_message(self, exception: Exception) -> str:
        """
        Format exception into user-friendly message.
        
        Args:
            exception: The exception to format
            
        Returns:
            Formatted error message
        """
        if isinstance(exception, TranscriptionError):
            message = f"❌ {exception.message}"
            if exception.details:
                message += f"\n   Details: {exception.details}"
            return message
        
        # Map known external exceptions
        exc_type = type(exception)
        if exc_type in self.EXCEPTION_MAPPING:
            custom_type, prefix = self.EXCEPTION_MAPPING[exc_type]
            return f"❌ {prefix}: {str(exception)}"
        
        # Unknown exception
        return f"❌ Unexpected error: {str(exception)}"
    
    def log_error(self, exception: Exception) -> str:
        """
        Create detailed error log entry.
        
        Args:
            exception: The exception to log
            
        Returns:
            Formatted log entry
        """
        timestamp = datetime.now().isoformat()
        exc_type = type(exception).__name__
        
        log_entry = f"""
================================================================================
ERROR LOG - {timestamp}
================================================================================
Exception Type: {exc_type}
Exit Code: {self.get_exit_code(exception)}
Message: {str(exception)}

Stack Trace:
{traceback.format_exc()}
================================================================================
"""
        return log_entry
    
    def write_error_file(self, exception: Exception) -> bool:
        """
        Write detailed error information to error file.
        
        Args:
            exception: The exception to log
            
        Returns:
            True if successfully written, False otherwise
        """
        if not self.error_file:
            return False
        
        try:
            self.error_file.parent.mkdir(parents=True, exist_ok=True)
            
            log_entry = self.log_error(exception)
            
            # Append to existing file
            with open(self.error_file, 'a') as f:
                f.write(log_entry)
            
            return True
        except Exception:
            # Don't raise on logging failures
            return False
    
    def handle(
        self, 
        exception: Exception, 
        write_log: bool = True,
        exit_on_error: bool = True
    ) -> int:
        """
        Handle an exception: print message, log to file, and optionally exit.
        
        Args:
            exception: The exception to handle
            write_log: Whether to write to error file
            exit_on_error: Whether to exit the process
            
        Returns:
            Exit code
        """
        # Print user-friendly message to stderr
        message = self.format_error_message(exception)
        print(message, file=sys.stderr)
        
        # Write detailed log if configured
        if write_log and self.error_file:
            if self.write_error_file(exception):
                print(f"   Error details logged to: {self.error_file}", file=sys.stderr)
        
        exit_code = self.get_exit_code(exception)
        
        if exit_on_error:
            sys.exit(exit_code)
        
        return exit_code


def wrap_provider_exception(
    exception: Exception, 
    provider: str
) -> TranscriptionError:
    """
    Wrap provider-specific exceptions into our custom exception types.
    
    Args:
        exception: The original exception
        provider: Provider name (aws, gcp, azure, local)
        
    Returns:
        Appropriate TranscriptionError subclass
    """
    exc_str = str(exception).lower()
    
    # Authentication patterns
    auth_patterns = [
        'credential', 'authentication', 'unauthorized', 'access denied',
        'invalid key', 'api key', 'permission', 'forbidden', '403', '401'
    ]
    if any(pattern in exc_str for pattern in auth_patterns):
        return AuthenticationError(
            f"{provider.upper()} authentication failed",
            details=str(exception)
        )
    
    # Network patterns
    network_patterns = [
        'timeout', 'connection', 'network', 'unreachable', 'refused',
        'reset', 'ssl', 'dns', '503', '502', '504'
    ]
    if any(pattern in exc_str for pattern in network_patterns):
        return NetworkError(
            f"{provider.upper()} connection failed",
            details=str(exception)
        )
    
    # Validation patterns
    validation_patterns = [
        '400', 'bad request', 'badrequest', 'invalid', 'unsupported',
        'format', 'not found', 'missing', 'input too long', 'too long'
    ]
    if any(pattern in exc_str for pattern in validation_patterns):
        return ValidationError(
            f"Validation error in {provider}",
            details=str(exception)
        )

    # Hardware patterns (mainly for local)
    hardware_patterns = [
        'out of memory', 'insufficient memory', 'cuda', 'gpu', 'mps',
        'metal', 'neural engine'
    ]
    if any(pattern in exc_str for pattern in hardware_patterns):
        return HardwareError(
            f"Hardware requirement not met for {provider}",
            details=str(exception)
        )
    
    # Default to unexpected error
    return TranscriptionError(
        f"Unexpected error in {provider}: {str(exception)}"
    )
