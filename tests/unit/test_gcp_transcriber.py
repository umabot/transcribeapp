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


class _FakeAudioEncoding:
    """Minimal enum-like audio encoding container."""

    FLAC = 'FLAC'
    LINEAR16 = 'LINEAR16'
    MP3 = 'MP3'
    OGG_OPUS = 'OGG_OPUS'
    WEBM_OPUS = 'WEBM_OPUS'
    ENCODING_UNSPECIFIED = 'ENCODING_UNSPECIFIED'


class _FakeRecognitionConfig:
    """Minimal recognition config object."""

    AudioEncoding = _FakeAudioEncoding

    def __init__(self, **kwargs):
        self.diarization_config = None
        for key, value in kwargs.items():
            setattr(self, key, value)


class _FakeSpeechModule:
    SpeechClient = _FakeSpeechClient
    RecognitionConfig = _FakeRecognitionConfig
    RecognitionAudio = staticmethod(lambda **kwargs: SimpleNamespace(**kwargs))
    SpeakerDiarizationConfig = staticmethod(
        lambda **kwargs: SimpleNamespace(**kwargs)
    )


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


def test_transcribe_always_uses_gcs_long_running_path(monkeypatch, tmp_path):
    """GCP should use the GCS-backed long-running API even for small files."""
    monkeypatch.delenv('GOOGLE_APPLICATION_CREDENTIALS', raising=False)
    monkeypatch.setenv('GCP_STORAGE_BUCKET', 'test-gcp-bucket')

    calls = {'upload': 0, 'long_running': 0, 'sync': 0, 'delete': 0}

    class FakeBlob:
        def upload_from_filename(self, file_path):
            calls['upload'] += 1

        def delete(self):
            calls['delete'] += 1

    class FakeBucket:
        def blob(self, name):
            return FakeBlob()

    class FakeStorageClient:
        def bucket(self, name):
            return FakeBucket()

    class FakeSpeechClient:
        def long_running_recognize(self, config, audio):
            calls['long_running'] += 1
            assert hasattr(audio, 'uri')
            return SimpleNamespace(result=lambda timeout: SimpleNamespace(results=[]))

        def recognize(self, config, audio):
            calls['sync'] += 1
            raise AssertionError('sync recognize should not be used for GCP')

    monkeypatch.setattr(
        'src.transcribe.providers.gcp._ensure_gcp_imports',
        lambda: None,
    )
    monkeypatch.setattr(
        'src.transcribe.providers.gcp.speech_v1',
        SimpleNamespace(
            SpeechClient=lambda: FakeSpeechClient(),
            RecognitionConfig=_FakeRecognitionConfig,
            RecognitionAudio=lambda **kwargs: SimpleNamespace(**kwargs),
            SpeakerDiarizationConfig=lambda **kwargs: SimpleNamespace(**kwargs),
        ),
        raising=False,
    )
    monkeypatch.setattr(
        'src.transcribe.providers.gcp.storage',
        SimpleNamespace(Client=lambda: FakeStorageClient()),
        raising=False,
    )

    audio_file = tmp_path / 'short.mp3'
    audio_file.write_bytes(b'not-a-real-mp3-but-good-enough-for-branch-testing')

    transcriber = GCPTranscriber()
    monkeypatch.setattr(
        transcriber,
        '_convert_to_standard_format',
        lambda response, detected_language, enable_diarization: {
            'transcript': 'ok',
            'segments': [],
            'metadata': {'provider': transcriber.PROVIDER_NAME},
        },
    )

    result = transcriber.transcribe(str(audio_file), language_code='en-US')

    assert result['transcript'] == 'ok'
    assert calls['upload'] == 1
    assert calls['long_running'] == 1
    assert calls['sync'] == 0
    assert calls['delete'] == 1
