"""Unit tests for GCP transcriber authentication behavior."""

from types import SimpleNamespace

from src.transcribe.providers.gcp import GCPTranscriber


class _FakeSpeechClient:
    """Minimal fake Speech client."""


class _FakeBucket:
    """Minimal fake Storage bucket."""


class _FakeStorageClient:
    """Minimal fake Storage client."""

    def bucket(self, name):
        return _FakeBucket()


class _FakeSpeechModule:
    SpeechClient = _FakeSpeechClient


class _FakeStorageModule:
    Client = _FakeStorageClient


def test_init_allows_adc_without_google_application_credentials(monkeypatch):
    """GCP transcriber should allow ADC-based auth without a local key file."""
    monkeypatch.delenv('GOOGLE_APPLICATION_CREDENTIALS', raising=False)
    monkeypatch.setenv('GCP_STORAGE_BUCKET', 'test-gcp-bucket')

    monkeypatch.setattr(
        'src.transcribe.providers.gcp._ensure_gcp_imports',
        lambda: None,
    )
    monkeypatch.setattr(
        'src.transcribe.providers.gcp.speech_v1',
        _FakeSpeechModule,
        raising=False,
    )
    monkeypatch.setattr(
        'src.transcribe.providers.gcp.storage',
        _FakeStorageModule,
        raising=False,
    )

    transcriber = GCPTranscriber()

    assert transcriber.bucket_name == 'test-gcp-bucket'
    assert isinstance(transcriber.speech_client, _FakeSpeechClient)
    assert isinstance(transcriber.storage_client, _FakeStorageClient)
