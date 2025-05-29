from whispercpp import Whisper
from logger import get_logger

logger = get_logger(__name__)

class TranscribeWorker:
    """Loads a Whisper model and transcribes audio files."""

    def __init__(self, model_path: str = "large"):
        self.model_path = model_path
        logger.info("Loading Whisper model %s", model_path)
        self.model = Whisper(model_path)

    def transcribe(self, audio_path: str):
        """Transcribe the given audio file and return segments."""
        # request timestamps from the Whisper model
        logger.info("Transcribing %s", audio_path)
        result = self.model.transcribe(audio_path)
        segments = []
        for seg in result.get("segments", []):
            segments.append({
                "start": float(seg.get("start", 0.0)),
                "end": float(seg.get("end", 0.0)),
                "speaker": "Speaker 1",
                "text": seg.get("text", "").strip(),
            })
        logger.debug("Produced %d segments", len(segments))
        return segments
