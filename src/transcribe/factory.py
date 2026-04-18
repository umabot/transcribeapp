"""Factory for creating transcriber instances."""

from typing import Dict, Type

from src.transcribe.base import BaseTranscriber
from src.errors import ValidationError


class TranscriberFactory:
    """
    Factory for creating transcriber instances based on provider name.
    
    Implements the Factory Pattern to instantiate the appropriate
    transcriber class based on user selection.
    """
    
    # Registry of available providers
    # Populated lazily to avoid import errors when dependencies aren't installed
    _registry: Dict[str, Type[BaseTranscriber]] = {}
    _initialized: bool = False
    
    @classmethod
    def _initialize_registry(cls) -> None:
        """Initialize the provider registry with available transcribers."""
        if cls._initialized:
            return
        
        # AWS - always available (core dependency)
        try:
            from src.transcribe.providers.aws import AWSTranscriber
            cls._registry['aws'] = AWSTranscriber
        except ImportError:
            pass
        
        # GCP - optional
        try:
            from src.transcribe.providers.gcp import GCPTranscriber
            cls._registry['gcp'] = GCPTranscriber
        except ImportError:
            pass
        
        # Azure - optional
        try:
            from src.transcribe.providers.azure import AzureTranscriber
            cls._registry['azure'] = AzureTranscriber
        except ImportError:
            pass
        
        # Local Whisper - optional
        try:
            from src.transcribe.providers.local import LocalTranscriber
            cls._registry['local'] = LocalTranscriber
        except ImportError:
            pass
        
        cls._initialized = True
    
    @classmethod
    def get_transcriber(cls, provider_name: str, **kwargs) -> BaseTranscriber:
        """
        Get a transcriber instance for the specified provider.
        
        Args:
            provider_name: Name of the provider ('aws', 'gcp', 'azure', 'local')
            **kwargs: Additional arguments passed to the transcriber constructor
            
        Returns:
            Instance of the requested transcriber
            
        Raises:
            ValidationError: If provider is unknown or unavailable
        """
        cls._initialize_registry()
        
        provider_lower = provider_name.lower()
        
        if provider_lower not in cls._registry:
            available = cls.list_available_providers()
            if available:
                available_str = ', '.join(available)
                raise ValidationError(
                    f"Unknown provider: '{provider_name}'. "
                    f"Available providers: {available_str}"
                )
            else:
                raise ValidationError(
                    f"No transcription providers available. "
                    f"Please install required dependencies."
                )
        
        transcriber_class = cls._registry[provider_lower]
        return transcriber_class(**kwargs)
    
    @classmethod
    def list_available_providers(cls) -> list:
        """
        List all available provider names.
        
        Returns:
            List of provider name strings
        """
        cls._initialize_registry()
        return list(cls._registry.keys())
    
    @classmethod
    def is_provider_available(cls, provider_name: str) -> bool:
        """
        Check if a provider is available.
        
        Args:
            provider_name: Provider name to check
            
        Returns:
            True if provider is available
        """
        cls._initialize_registry()
        return provider_name.lower() in cls._registry
    
    @classmethod
    def get_provider_info(cls) -> Dict[str, dict]:
        """
        Get information about all providers including availability and env vars.
        
        Returns:
            Dictionary with provider info
        """
        return {
            'aws': {
                'name': 'AWS Transcribe',
                'available': cls.is_provider_available('aws'),
                'env_vars': [
                    'AWS_ACCESS_KEY_ID',
                    'AWS_SECRET_ACCESS_KEY',
                    'AWS_REGION',
                    'AWS_S3_BUCKET'
                ],
                'language_format': 'BCP-47 (e.g., en-US, fr-FR)',
                'diarization_support': True,
                'max_speakers': 10,
            },
            'gcp': {
                'name': 'Google Cloud Speech-to-Text',
                'available': cls.is_provider_available('gcp'),
                'env_vars': [
                    'GOOGLE_APPLICATION_CREDENTIALS',
                    'GCP_STORAGE_BUCKET'
                ],
                'language_format': 'BCP-47 (e.g., en-US, fr-FR)',
                'diarization_support': True,
                'max_speakers': 10,
            },
            'azure': {
                'name': 'Azure AI Speech',
                'available': cls.is_provider_available('azure'),
                'env_vars': [
                    'AZURE_SPEECH_KEY',
                    'AZURE_SPEECH_REGION'
                ],
                'language_format': 'BCP-47 (e.g., en-US, fr-FR)',
                'diarization_support': True,
                'max_speakers': 10,
            },
            'local': {
                'name': 'Local Whisper',
                'available': cls.is_provider_available('local'),
                'env_vars': [],  # No cloud credentials needed
                'language_format': 'ISO-639-1 (e.g., en, fr, es)',
                'diarization_support': 'Limited (requires pyannote-audio)',
                'max_speakers': 10,
                'hardware_requirements': 'Apple Silicon recommended (M1/M2/M3/M4)',
            },
        }
