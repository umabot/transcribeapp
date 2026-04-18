"""Base transcriber interface for all providers."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from src.errors import ValidationError


class BaseTranscriber(ABC):
    """
    Abstract base class for all transcription providers.
    
    Implements the Strategy Pattern to allow interchangeable providers
    (AWS, GCP, Azure, Local Whisper) while maintaining a consistent interface.
    """
    
    # Subclasses should define their supported audio formats
    SUPPORTED_FORMATS: set = set()
    
    # Provider name for identification
    PROVIDER_NAME: str = "base"
    
    def validate_file(self, file_path: str) -> str:
        """
        Validate that the file exists and has a supported format.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            The file extension (lowercase, without dot)
            
        Raises:
            ValidationError: If file doesn't exist or format is unsupported
        """
        path = Path(file_path)
        
        if not path.exists():
            raise ValidationError(f"File not found: {file_path}")
        
        if not path.is_file():
            raise ValidationError(f"Path is not a file: {file_path}")
        
        extension = path.suffix[1:].lower() if path.suffix else ""
        
        if not extension:
            raise ValidationError("File has no extension")
        
        if extension not in self.SUPPORTED_FORMATS:
            supported_list = ', '.join(sorted(self.SUPPORTED_FORMATS))
            raise ValidationError(
                f"Unsupported file format: '{extension}'. "
                f"{self.PROVIDER_NAME} supports: {supported_list}"
            )
        
        return extension
    
    @abstractmethod
    def validate_language(self, language_code: Optional[str]) -> Optional[str]:
        """
        Validate the language code for this provider.
        
        Each provider has different requirements:
        - AWS/GCP/Azure: BCP-47 format (e.g., en-US, fr-FR)
        - Local Whisper: ISO-639-1 format (e.g., en, fr)
        
        Args:
            language_code: The language code to validate, or None for auto-detect
            
        Returns:
            The validated language code, or None if auto-detect
            
        Raises:
            ValidationError: If the language code is invalid for this provider
        """
        pass
    
    @abstractmethod
    def transcribe(
        self, 
        file_path: str, 
        language_code: Optional[str] = None,
        enable_diarization: bool = True,
        max_speakers: int = 2
    ) -> dict:
        """
        Transcribe an audio file.
        
        Args:
            file_path: Path to the audio file
            language_code: Language code (provider-specific format) or None for auto-detect
            enable_diarization: Whether to enable speaker diarization
            max_speakers: Maximum number of speakers to identify
            
        Returns:
            Standardized transcript dictionary with structure:
            {
                "transcript": str,  # Full transcript text
                "segments": [       # Speaker-labeled segments (if diarization enabled)
                    {
                        "speaker": str,      # Speaker label (e.g., "spk_0")
                        "start": float,      # Start time in seconds
                        "end": float,        # End time in seconds
                        "text": str          # Segment text
                    }
                ],
                "metadata": {
                    "provider": str,         # Provider name
                    "language": str,         # Detected or specified language
                    "duration": float,       # Audio duration in seconds
                    "confidence": float,     # Average confidence score (if available)
                    ...                      # Provider-specific metadata
                }
            }
            
        Raises:
            ValidationError: If input validation fails
            AuthenticationError: If credentials are invalid
            NetworkError: If API call fails
        """
        pass
    
    def validate_parameters(self, max_speakers: int, enable_diarization: bool) -> None:
        """
        Validate transcription parameters.
        
        Args:
            max_speakers: Maximum number of speakers
            enable_diarization: Whether diarization is enabled
            
        Raises:
            ValidationError: If parameters are invalid
        """
        if enable_diarization:
            if max_speakers < 2 or max_speakers > 10:
                raise ValidationError(
                    "max_speakers must be between 2 and 10 when diarization is enabled"
                )
        else:
            if max_speakers != 1:
                raise ValidationError(
                    "max_speakers should be 1 when diarization is disabled"
                )
