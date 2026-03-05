"""
Voice Command Module - Voice commands using Vosk

Civil Technology: 100% local, open source, no API, no credits.
Vosk is completely free and works offline.
"""

import json
import logging
import wave
import io
from typing import Optional, Dict
from pathlib import Path

logger = logging.getLogger(__name__)


class VoiceCommandProcessor:
    """Voice command processor using Vosk (offline, local, free)"""
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize voice processor with Vosk
        
        Args:
            model_path: Path to Vosk model. If None, tries to locate/download automatically
        """
        self.model = None
        self.recognizer = None
        self.model_path = model_path
        self._initialized = False
        
        # Try to initialize Vosk
        try:
            self._initialize_vosk()
        except Exception as e:
            logger.warning(f"Vosk not available: {e}. Voice commands will be disabled.")
            logger.info("To enable voice commands, install Vosk: pip install vosk")
            logger.info("And download a language model from: https://alphacephei.com/vosk/models")
    
    def _initialize_vosk(self):
        """Initialize Vosk if available"""
        try:
            import vosk
            
            # Search for model if path not specified
            if not self.model_path:
                self.model_path = self._find_or_download_model()
            
            if not self.model_path or not Path(self.model_path).exists():
                raise FileNotFoundError(
                    f"Vosk model not found at: {self.model_path}\n"
                    "Download a language model from: https://alphacephei.com/vosk/models\n"
                    "Recommended model: vosk-model-small-es-0.22 (50MB) for Spanish"
                )
            
            # Load model
            logger.info(f"Loading Vosk model from: {self.model_path}")
            self.model = vosk.Model(self.model_path)
            self.recognizer = vosk.KaldiRecognizer(self.model, 16000)  # 16kHz sample rate
            self.recognizer.SetWords(True)  # Include words in result
            
            self._initialized = True
            logger.info("✅ Vosk initialized successfully - Voice commands enabled")
            
        except ImportError:
            raise ImportError(
                "Vosk is not installed. Install with: pip install vosk\n"
                "Vosk is 100% local, open source and free."
            )
    
    def _find_or_download_model(self) -> Optional[str]:
        """Search for Vosk model or suggest downloading it"""
        # Search in common locations
        possible_paths = [
            Path.home() / "vosk-models" / "vosk-model-small-es-0.22",
            Path.home() / "vosk-models" / "vosk-model-es-0.22",
            Path(__file__).parent.parent / "models" / "vosk-model-small-es-0.22",
            Path(__file__).parent.parent / "models" / "vosk-model-es-0.22",
        ]
        
        for path in possible_paths:
            if path.exists() and (path / "am" / "final.mdl").exists():
                return str(path)
        
        # If not found, suggest download
        logger.info(
            "Vosk model not found. To enable voice commands:\n"
            "1. Download a language model from: https://alphacephei.com/vosk/models\n"
            "2. Recommended: vosk-model-small-es-0.22 (50MB) for Spanish\n"
            "3. Extract to: ~/vosk-models/vosk-model-small-es-0.22\n"
            "   Or to: agent/models/vosk-model-small-es-0.22"
        )
        return None
    
    def is_available(self) -> bool:
        """Check if voice processor is available"""
        return self._initialized and self.recognizer is not None
    
    def process_audio(self, audio_data: bytes, sample_rate: int = 16000) -> Dict:
        """
        Process audio and return recognized text
        
        Args:
            audio_data: Audio data in WAV/PCM format
            sample_rate: Sample rate (default: 16000 Hz)
        
        Returns:
            Dict with 'text' (recognized text), 'confidence' (confidence), 'words' (words)
        """
        if not self.is_available():
            return {
                'text': '',
                'confidence': 0.0,
                'error': 'Voice recognition not available. Install Vosk and download a language model.',
                'words': []
            }
        
        try:
            # Ensure recognizer has correct frequency
            if self.recognizer.AcceptWaveform(audio_data):
                result = json.loads(self.recognizer.Result())
                text = result.get('text', '').strip()
                confidence = result.get('confidence', 0.0) if 'confidence' in result else 0.0
                
                return {
                    'text': text,
                    'confidence': confidence,
                    'words': result.get('result', []),
                    'error': None
                }
            else:
                # Partial result
                partial = json.loads(self.recognizer.PartialResult())
                return {
                    'text': partial.get('partial', '').strip(),
                    'confidence': 0.0,
                    'words': [],
                    'partial': True,
                    'error': None
                }
        
        except Exception as e:
            logger.error(f"Error processing audio: {e}")
            return {
                'text': '',
                'confidence': 0.0,
                'error': str(e),
                'words': []
            }
    
    def process_wav_file(self, wav_file_path: str) -> Dict:
        """
        Process a WAV file
        
        Args:
            wav_file_path: Path to WAV file
        
        Returns:
            Dict with recognition result
        """
        if not self.is_available():
            return {
                'text': '',
                'confidence': 0.0,
                'error': 'Voice recognition not available',
                'words': []
            }
        
        try:
            with wave.open(wav_file_path, 'rb') as wf:
                sample_rate = wf.getframerate()
                
                # Ensure recognizer has correct frequency
                if sample_rate != 16000:
                    logger.warning(f"Sample rate {sample_rate} != 16000, may affect accuracy")
                
                audio_data = wf.readframes(wf.getnframes())
                return self.process_audio(audio_data, sample_rate)
        
        except Exception as e:
            logger.error(f"Error processing WAV file: {e}")
            return {
                'text': '',
                'confidence': 0.0,
                'error': str(e),
                'words': []
            }
    
    def process_wav_bytes(self, wav_bytes: bytes) -> Dict:
        """
        Process WAV data from bytes
        
        Args:
            wav_bytes: WAV file bytes
        
        Returns:
            Dict with recognition result
        """
        if not self.is_available():
            return {
                'text': '',
                'confidence': 0.0,
                'error': 'Voice recognition not available',
                'words': []
            }
        
        try:
            wav_io = io.BytesIO(wav_bytes)
            with wave.open(wav_io, 'rb') as wf:
                sample_rate = wf.getframerate()
                audio_data = wf.readframes(wf.getnframes())
                return self.process_audio(audio_data, sample_rate)
        
        except Exception as e:
            logger.error(f"Error processing WAV bytes: {e}")
            return {
                'text': '',
                'confidence': 0.0,
                'error': str(e),
                'words': []
            }


# Singleton for voice processor
_voice_processor: Optional[VoiceCommandProcessor] = None


def get_voice_processor(model_path: Optional[str] = None) -> VoiceCommandProcessor:
    """
    Get singleton instance of voice processor
    
    Args:
        model_path: Path to Vosk model (only used on first call)
    
    Returns:
        VoiceCommandProcessor instance
    """
    global _voice_processor
    
    if _voice_processor is None:
        _voice_processor = VoiceCommandProcessor(model_path=model_path)
    
    return _voice_processor

