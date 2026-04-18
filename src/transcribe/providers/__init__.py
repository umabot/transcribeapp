"""Transcription provider implementations."""

# Lazy imports to avoid dependency errors
# Providers are imported by the factory when needed

__all__ = [
    'AWSTranscriber',
    'GCPTranscriber',
    'AzureTranscriber',
    'LocalTranscriber',
]


def __getattr__(name):
    """Lazy import providers to avoid import errors when dependencies missing."""
    if name == 'AWSTranscriber':
        from src.transcribe.providers.aws import AWSTranscriber
        return AWSTranscriber
    elif name == 'GCPTranscriber':
        from src.transcribe.providers.gcp import GCPTranscriber
        return GCPTranscriber
    elif name == 'AzureTranscriber':
        from src.transcribe.providers.azure import AzureTranscriber
        return AzureTranscriber
    elif name == 'LocalTranscriber':
        from src.transcribe.providers.local import LocalTranscriber
        return LocalTranscriber
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
