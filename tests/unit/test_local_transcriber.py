"""Unit tests for LocalTranscriber."""

from types import SimpleNamespace

import src.transcribe.providers.local as local_module


class _MockWhisperModel:
    """Test double for faster-whisper model initialization."""

    def __init__(self, model_name, device, compute_type):
        self.model_name = model_name
        self.device = device
        self.compute_type = compute_type


class _MockMPSBackend:
    @staticmethod
    def is_available():
        return True


class _MockCudaBackend:
    @staticmethod
    def is_available():
        return False


class TestLocalTranscriberComputeType:
    """Tests for device and compute type selection."""

    def test_load_model_uses_cpu_safe_compute_type_for_apple_silicon_fallback(self, monkeypatch):
        """Test faster-whisper falls back from MPS to CPU with a CPU-safe compute type."""
        dummy_torch = SimpleNamespace(
            backends=SimpleNamespace(mps=_MockMPSBackend()),
            cuda=_MockCudaBackend(),
        )
        dummy_whisper = SimpleNamespace(
            _is_faster=True,
            WhisperModel=_MockWhisperModel,
        )

        monkeypatch.setattr(local_module, "torch", dummy_torch)
        monkeypatch.setattr(local_module, "whisper", dummy_whisper)
        monkeypatch.setattr(local_module, "_ensure_whisper_imports", lambda: None)
        monkeypatch.setattr(local_module, "_is_apple_silicon", lambda: True)
        monkeypatch.setattr(local_module, "_get_system_ram_gb", lambda: 32)

        transcriber = local_module.LocalTranscriber(model_name="base")
        transcriber._load_model()

        assert transcriber.model.device == "cpu"
        assert transcriber.model.compute_type in {"int8", "float32"}

    def test_load_model_uses_cpu_safe_compute_type_for_cpu_device(self, monkeypatch):
        """Test faster-whisper uses a CPU-safe compute type on CPU-only systems."""
        dummy_torch = SimpleNamespace(
            backends=SimpleNamespace(mps=_MockMPSBackend()),
            cuda=_MockCudaBackend(),
        )
        dummy_whisper = SimpleNamespace(
            _is_faster=True,
            WhisperModel=_MockWhisperModel,
        )

        monkeypatch.setattr(local_module, "torch", dummy_torch)
        monkeypatch.setattr(local_module, "whisper", dummy_whisper)
        monkeypatch.setattr(local_module, "_ensure_whisper_imports", lambda: None)
        monkeypatch.setattr(local_module, "_is_apple_silicon", lambda: False)
        monkeypatch.setattr(local_module, "_get_system_ram_gb", lambda: 32)

        transcriber = local_module.LocalTranscriber(model_name="base", device="cpu")
        transcriber._load_model()

        assert transcriber.model.device == "cpu"
        assert transcriber.model.compute_type in {"int8", "float32"}
