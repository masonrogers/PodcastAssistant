from dataclasses import dataclass
from typing import List


@dataclass
class TranscriptSegment:
    start: float
    end: float
    speaker: str
    text: str


class TranscribeWorker:
    """Transcribes audio files using Whisper when available."""

    def __init__(self):
        try:
            import whisper  # type: ignore
            self._model = whisper.load_model("base")
        except Exception:
            self._model = None

    def transcribe(self, file_path: str) -> List[TranscriptSegment]:
        """Return a list of transcript segments with timestamps."""
        if self._model:
            result = self._model.transcribe(file_path, fp16=False)
            segments = [
                TranscriptSegment(
                    start=s["start"],
                    end=s["end"],
                    speaker="Speaker 1",
                    text=s["text"].strip(),
                )
                for s in result.get("segments", [])
            ]
            if segments:
                return segments
        # Fallback stub
        return [
            TranscriptSegment(
                start=0.0,
                end=0.0,
                speaker="Speaker 1",
                text=f"Transcribed text from {file_path}",
            )
        ]
