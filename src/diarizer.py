from typing import List, Dict
from logger import get_logger

logger = get_logger(__name__)

# pyannote.audio is heavy, so we import lazily

class Diarizer:
    """Assigns speaker labels using a pyannote.audio pipeline."""

    def __init__(self, model_name: str = "pyannote/speaker-diarization"):
        self.model_name = model_name
        self.pipeline = None

    def _load_pipeline(self):
        """Load the pyannote pipeline when first needed."""
        if self.pipeline is None:
            logger.info("Loading diarization model %s", self.model_name)
            from pyannote.audio import Pipeline
            self.pipeline = Pipeline.from_pretrained(self.model_name)
        return self.pipeline

    def assign_speakers(self, audio_path: str, segments: List[Dict]) -> List[Dict]:
        """Return segments with speaker labels filled in."""
        logger.info("Assigning speakers for %s", audio_path)
        self._load_pipeline()
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
            logger.debug("Segment %s-%s labeled as %s", seg["start"], seg["end"], label)
        return segments
