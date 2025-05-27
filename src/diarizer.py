from typing import List, Dict

# pyannote.audio is heavy, so we import lazily
from pyannote.audio import Pipeline

class Diarizer:
    """Assigns speaker labels using a pyannote.audio pipeline."""

    def __init__(self, model_name: str = "pyannote/speaker-diarization"):
        self.model_name = model_name
        self.pipeline = Pipeline.from_pretrained(model_name)

    def assign_speakers(self, audio_path: str, segments: List[Dict]) -> List[Dict]:
        """Return segments with speaker labels filled in."""
        diarization = self.pipeline(audio_path)
        # diarization.itertracks(yield_label=True) yields (segment, track, label)
        tracks = list(diarization.itertracks(yield_label=True))
        for seg in segments:
            mid = (seg["start"] + seg["end"]) / 2
            label = "Unknown"
            for ts, _, speaker in tracks:
                if ts.start <= mid < ts.end:
                    label = speaker
                    break
            seg["speaker"] = label
        return segments
