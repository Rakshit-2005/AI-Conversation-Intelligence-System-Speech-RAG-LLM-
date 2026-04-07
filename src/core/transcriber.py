"""
Core transcription module using OpenAI Whisper
Handles audio-to-text conversion
"""

import logging
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any
import whisper
from config import settings

logger = logging.getLogger(__name__)


class AudioTranscriber:
    """Transcribes audio files to text using Whisper"""

    def __init__(self, model_size: str = "base"):
        """
        Initialize transcriber with specified Whisper model
        
        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
        """
        self.model_size = model_size
        self.model = None
        self._load_model()

    def _load_model(self):
        """Load Whisper model"""
        try:
            logger.info(f"Loading Whisper model: {self.model_size}")
            self.model = whisper.load_model(self.model_size)
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            raise

    def transcribe(
        self,
        audio_path: Path,
        language: Optional[str] = None,
        task: str = "transcribe",
    ) -> Dict[str, Any]:
        """
        Transcribe audio file to text
        
        Args:
            audio_path: Path to audio file
            language: Language code (e.g., 'en', 'es')
            task: 'transcribe' or 'translate'
            
        Returns:
            Dictionary containing transcription and metadata
        """
        if not audio_path.exists():
            logger.error(f"Audio file not found: {audio_path}")
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        try:
            logger.info(f"Transcribing audio: {audio_path}")
            result = self.model.transcribe(
                str(audio_path),
                language=language,
                task=task,
                verbose=False,
            )

            logger.info(f"Transcription completed successfully")
            return {
                "text": result["text"],
                "language": result.get("language", "unknown"),
                "duration": result.get("duration", 0),
                "segments": result.get("segments", []),
            }

        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise

    async def transcribe_async(
        self,
        audio_path: Path,
        language: Optional[str] = None,
        task: str = "transcribe",
    ) -> Dict[str, Any]:
        """
        Async wrapper for transcription
        
        Args:
            audio_path: Path to audio file
            language: Language code
            task: 'transcribe' or 'translate'
            
        Returns:
            Dictionary containing transcription and metadata
        """
        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, self.transcribe, audio_path, language, task
        )

    def transcribe_with_timestamps(self, audio_path: Path) -> Dict[str, Any]:
        """
        Transcribe audio with segment-level timestamps
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Dictionary with timestamped segments
        """
        try:
            logger.info(f"Transcribing with timestamps: {audio_path}")
            result = self.model.transcribe(str(audio_path), verbose=False)

            segments = []
            for segment in result["segments"]:
                segments.append(
                    {
                        "id": segment.get("id", 0),
                        "start": segment.get("start", 0),
                        "end": segment.get("end", 0),
                        "text": segment.get("text", ""),
                    }
                )

            return {
                "text": result["text"],
                "language": result.get("language", "unknown"),
                "segments": segments,
            }

        except Exception as e:
            logger.error(f"Transcription with timestamps failed: {e}")
            raise

    def get_supported_formats(self) -> list:
        """Get list of supported audio formats"""
        return settings.AUDIO_FORMATS


# Global transcriber instance
_transcriber = None


def get_transcriber(model_size: str = None) -> AudioTranscriber:
    """Get or create singleton transcriber"""
    global _transcriber
    if _transcriber is None:
        model_size = model_size or settings.WHISPER_MODEL
        _transcriber = AudioTranscriber(model_size=model_size)
    return _transcriber
