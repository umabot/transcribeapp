"""Local Whisper transcription provider implementation."""

import os
import platform
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

from src.transcribe.base import BaseTranscriber
from src.errors import (
    ValidationError,
    HardwareError,
    wrap_provider_exception,
)
from src.validation.language import validate_whisper_language

# Lazy imports for optional dependencies
whisper = None
torch = None


def _ensure_whisper_imports():
    """Lazily import Whisper and torch libraries."""
    global whisper, torch
    if whisper is None:
        try:
            # Try faster-whisper first (recommended)
            import faster_whisper as _whisper
            whisper = _whisper
            whisper._is_faster = True
        except ImportError:
            try:
                # Fall back to openai-whisper
                import whisper as _whisper
                whisper = _whisper
                whisper._is_faster = False
            except ImportError:
                raise ValidationError(
                    "Whisper not installed. "
                    "Install with: pip install faster-whisper (recommended) "
                    "or pip install openai-whisper"
                )
    
    if torch is None:
        try:
            import torch as _torch
            torch = _torch
        except ImportError:
            raise ValidationError(
                "PyTorch not installed. "
                "Install with: pip install torch"
            )


def _get_system_ram_gb() -> float:
    """Get system RAM in GB."""
    try:
        if platform.system() == 'Darwin':
            # macOS
            result = subprocess.run(
                ['sysctl', '-n', 'hw.memsize'],
                capture_output=True,
                text=True
            )
            return int(result.stdout.strip()) / (1024 ** 3)
        elif platform.system() == 'Linux':
            with open('/proc/meminfo') as f:
                for line in f:
                    if line.startswith('MemTotal:'):
                        return int(line.split()[1]) / (1024 ** 2)
        return 16  # Default assumption
    except Exception:
        return 16


def _is_apple_silicon() -> bool:
    """Check if running on Apple Silicon."""
    if platform.system() != 'Darwin':
        return False
    return platform.machine() == 'arm64'


def _get_optimal_device() -> str:
    """
    Determine the optimal compute device.
    
    Returns:
        Device string: 'mps' for Apple Silicon, 'cuda' for NVIDIA, 'cpu' otherwise
    """
    _ensure_whisper_imports()
    
    # Check for Apple Silicon MPS
    if _is_apple_silicon() and hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
        return 'mps'
    
    # Check for CUDA
    if torch.cuda.is_available():
        return 'cuda'
    
    return 'cpu'


class LocalTranscriber(BaseTranscriber):
    """
    Local Whisper transcription provider.
    
    Uses OpenAI's Whisper model (or faster-whisper) for local transcription.
    Optimized for Apple Silicon with MPS (Metal Performance Shaders) support.
    
    Model sizes and requirements:
    - tiny: ~1GB RAM, fastest, lowest accuracy
    - base: ~1GB RAM, fast, good accuracy (default)
    - small: ~2GB RAM, good balance
    - medium: ~5GB RAM, high accuracy
    - large: ~10GB RAM, highest accuracy
    - large-v3: ~10GB RAM, latest and best
    
    No cloud credentials required - runs entirely locally.
    """
    
    PROVIDER_NAME = "Local Whisper"
    SUPPORTED_FORMATS = {'wav', 'mp3', 'flac', 'ogg', 'm4a', 'webm', 'mp4'}
    
    # Model RAM requirements in GB
    MODEL_RAM_REQUIREMENTS = {
        'tiny': 1,
        'tiny.en': 1,
        'base': 1,
        'base.en': 1,
        'small': 2,
        'small.en': 2,
        'medium': 5,
        'medium.en': 5,
        'large': 10,
        'large-v1': 10,
        'large-v2': 10,
        'large-v3': 10,
    }
    
    def __init__(
        self,
        model_name: str = "base",
        device: Optional[str] = None,
        compute_type: str = "auto"
    ):
        """
        Initialize Local Whisper Transcriber.
        
        Args:
            model_name: Whisper model size (tiny, base, small, medium, large, large-v3)
            device: Compute device ('mps', 'cuda', 'cpu') or None for auto-detect
            compute_type: Compute type for faster-whisper ('auto', 'float16', 'int8', etc.)
        """
        _ensure_whisper_imports()
        
        self.model_name = model_name
        self.compute_type = compute_type
        self.device = device or _get_optimal_device()
        self.actual_device = self.device
        self.actual_compute_type = compute_type
        self.model = None  # Lazy load
        self._is_faster_whisper = getattr(whisper, '_is_faster', False)
        
        # Check hardware requirements
        self._check_hardware_requirements()
        
        print(f"🔧 Initialized LocalTranscriber:")
        print(f"   Model: {self.model_name}")
        print(f"   Device: {self.device}")
        print(f"   Engine: {'faster-whisper' if self._is_faster_whisper else 'openai-whisper'}")
        
        if _is_apple_silicon():
            print(f"   Apple Silicon: ✓ (Hardware acceleration enabled)")
    
    def _get_effective_compute_type(self, device: str) -> str:
        """Return a compute type supported by the actual runtime device."""
        if not self._is_faster_whisper:
            return self.compute_type
        
        if self.compute_type != 'auto':
            return self.compute_type
        
        if device == 'cuda':
            return 'float16'
        
        return 'int8'
    
    def _check_hardware_requirements(self) -> None:
        """
        Check if system meets hardware requirements for the selected model.
        
        Raises:
            HardwareError: If requirements not met
        """
        required_ram = self.MODEL_RAM_REQUIREMENTS.get(self.model_name, 10)
        available_ram = _get_system_ram_gb()
        
        if available_ram < required_ram:
            raise HardwareError(
                f"Insufficient RAM for model '{self.model_name}'",
                details=f"Required: {required_ram}GB, Available: {available_ram:.1f}GB. "
                        f"Try a smaller model (tiny, base, small)."
            )
        
        if self.device == 'mps' and not _is_apple_silicon():
            raise HardwareError(
                "MPS device requested but not running on Apple Silicon"
            )
        
        if self.device == 'cuda':
            if not torch.cuda.is_available():
                raise HardwareError(
                    "CUDA device requested but CUDA is not available",
                    details="Install CUDA toolkit or use device='cpu'"
                )
    
    def _load_model(self):
        """Lazy load the Whisper model."""
        if self.model is not None:
            return
        
        print(f"Loading Whisper model '{self.model_name}'...")
        
        try:
            if self._is_faster_whisper:
                # faster-whisper uses different device names
                device = self.device
                if device == 'mps':
                    # faster-whisper doesn't support MPS directly, use CPU
                    device = 'cpu'
                    print("   Note: faster-whisper using CPU (MPS not supported)")
                
                compute_type = self._get_effective_compute_type(device)
                self.actual_device = device
                self.actual_compute_type = compute_type
                
                try:
                    self.model = whisper.WhisperModel(
                        self.model_name,
                        device=device,
                        compute_type=compute_type
                    )
                except Exception as model_error:
                    if device == 'cpu' and compute_type != 'float32':
                        error_msg = str(model_error).lower()
                        if 'float16' in error_msg or 'compute type' in error_msg:
                            print("   Note: retrying with float32 for CPU compatibility")
                            compute_type = 'float32'
                            self.actual_compute_type = compute_type
                            self.model = whisper.WhisperModel(
                                self.model_name,
                                device=device,
                                compute_type=compute_type
                            )
                        else:
                            raise
                    else:
                        raise
            else:
                # openai-whisper
                self.actual_device = self.device
                self.actual_compute_type = 'float32' if self.device in {'cpu', 'mps'} else 'float16'
                self.model = whisper.load_model(self.model_name, device=self.device)
            
            print(f"✓ Model loaded")
        except Exception as e:
            raise wrap_provider_exception(e, 'local')
    
    def validate_language(self, language_code: Optional[str]) -> Optional[str]:
        """
        Validate language code for Whisper.
        
        Whisper uses ISO-639-1 format (2-letter codes like 'en', 'fr').
        
        Args:
            language_code: ISO-639-1 code or None for auto-detect
            
        Returns:
            Validated code or None
            
        Raises:
            ValidationError: If invalid format or unsupported language
        """
        return validate_whisper_language(language_code)
    
    def _transcribe_faster_whisper(
        self,
        file_path: str,
        language_code: Optional[str],
        enable_diarization: bool
    ) -> dict:
        """
        Transcribe using faster-whisper.
        
        Returns:
            Raw transcription result
        """
        transcribe_options = {
            'beam_size': 5,
            'word_timestamps': True,
        }
        
        if language_code:
            transcribe_options['language'] = language_code
        
        segments, info = self.model.transcribe(file_path, **transcribe_options)
        
        # Convert generator to list
        segments_list = list(segments)
        
        return {
            'segments': segments_list,
            'info': info,
        }
    
    def _transcribe_openai_whisper(
        self,
        file_path: str,
        language_code: Optional[str],
        enable_diarization: bool
    ) -> dict:
        """
        Transcribe using openai-whisper.
        
        Returns:
            Raw transcription result
        """
        transcribe_options = {
            'word_timestamps': True,
            'verbose': False,
        }
        
        if language_code:
            transcribe_options['language'] = language_code
        
        result = self.model.transcribe(file_path, **transcribe_options)
        
        return result
    
    def _convert_to_standard_format(
        self,
        result: dict,
        enable_diarization: bool
    ) -> dict:
        """
        Convert Whisper result to standardized format.
        
        Note: Native Whisper doesn't support speaker diarization.
        Speaker labels will be 'spk_0' for all segments.
        """
        segments: List[Dict] = []
        full_transcript_parts = []
        duration = 0.0
        
        if self._is_faster_whisper:
            # faster-whisper format
            raw_segments = result.get('segments', [])
            info = result.get('info', {})
            detected_language = getattr(info, 'language', None)
            
            for seg in raw_segments:
                text = seg.text.strip()
                if not text:
                    continue
                
                full_transcript_parts.append(text)
                
                start = seg.start
                end = seg.end
                
                if end > duration:
                    duration = end
                
                segments.append({
                    'speaker': 'spk_0',  # Whisper doesn't do diarization natively
                    'start': start,
                    'end': end,
                    'text': text
                })
        else:
            # openai-whisper format
            detected_language = result.get('language')
            
            for seg in result.get('segments', []):
                text = seg.get('text', '').strip()
                if not text:
                    continue
                
                full_transcript_parts.append(text)
                
                start = seg.get('start', 0)
                end = seg.get('end', 0)
                
                if end > duration:
                    duration = end
                
                segments.append({
                    'speaker': 'spk_0',
                    'start': start,
                    'end': end,
                    'text': text
                })
        
        # Add diarization notice if requested but not available
        diarization_note = None
        if enable_diarization:
            diarization_note = (
                "Note: Native Whisper does not support speaker diarization. "
                "All segments are labeled 'spk_0'. For diarization, install "
                "pyannote-audio and configure it separately."
            )
        
        return {
            'transcript': ' '.join(full_transcript_parts),
            'segments': segments,
            'metadata': {
                'provider': self.PROVIDER_NAME,
                'language': detected_language or 'auto-detected',
                'duration': duration,
                'confidence': None,  # Whisper doesn't provide confidence scores
                'model': self.model_name,
                'device': self.actual_device,
                'compute_type': self.actual_compute_type,
                'engine': 'faster-whisper' if self._is_faster_whisper else 'openai-whisper',
                'diarization_note': diarization_note,
            }
        }
    
    def transcribe(
        self,
        file_path: str,
        language_code: Optional[str] = None,
        enable_diarization: bool = True,
        max_speakers: int = 2
    ) -> dict:
        """
        Transcribe an audio file using local Whisper.
        
        Args:
            file_path: Path to the audio file
            language_code: ISO-639-1 language code or None for auto-detect
            enable_diarization: Enable speaker diarization (limited support)
            max_speakers: Maximum number of speakers (not used by native Whisper)
            
        Returns:
            Standardized transcript dictionary
            
        Note:
            Native Whisper does not support speaker diarization. If diarization
            is requested, a note will be included in the metadata. For true
            diarization, consider integrating pyannote-audio.
        """
        # For local, we relax the diarization parameter check since
        # Whisper handles it differently
        if enable_diarization:
            # Just validate file, don't enforce speaker count
            pass
        else:
            self.validate_parameters(max_speakers, enable_diarization)
        
        self.validate_file(file_path)
        validated_language = self.validate_language(language_code)
        
        try:
            # Lazy load model
            self._load_model()
            
            print(f"Transcribing: {Path(file_path).name}")
            
            if self._is_faster_whisper:
                result = self._transcribe_faster_whisper(
                    file_path,
                    validated_language,
                    enable_diarization
                )
            else:
                result = self._transcribe_openai_whisper(
                    file_path,
                    validated_language,
                    enable_diarization
                )
            
            print("✓ Transcription complete")
            
            return self._convert_to_standard_format(result, enable_diarization)
            
        except (ValidationError, HardwareError):
            raise
        except Exception as e:
            raise wrap_provider_exception(e, 'local')
