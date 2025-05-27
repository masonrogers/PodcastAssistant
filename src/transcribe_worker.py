import whisper

class TranscribeWorker:
    """Loads a Whisper model and transcribes audio files."""

    def __init__(self, model_name: str = "base"):
        self.model_name = model_name
        self.model = whisper.load_model(model_name)

    def transcribe(self, audio_path: str):
        """Transcribe the given audio file and return segments."""
        # request timestamps from the Whisper model
        result = self.model.transcribe(audio_path, word_timestamps=False)
        segments = []
        for seg in result.get("segments", []):
            segments.append({
                "start": float(seg.get("start", 0.0)),
                "end": float(seg.get("end", 0.0)),
                "speaker": "Speaker 1",
                "text": seg.get("text", "").strip(),
            })
        return segments
