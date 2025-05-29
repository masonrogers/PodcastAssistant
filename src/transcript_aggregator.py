from typing import List, Dict
from logger import get_logger

logger = get_logger(__name__)

class TranscriptAggregator:
    """Collects transcript segments from multiple audio files."""

    def __init__(self):
        self._segments: List[Dict] = []
        logger.debug("TranscriptAggregator initialized")

    def add_segments(self, audio_file: str, segments: List[Dict]):
        """Add segments for the given audio file.

        Each segment will be copied and annotated with the source filename.
        """
        logger.info("Adding %d segments from %s", len(segments), audio_file)
        for seg in segments:
            entry = seg.copy()
            entry["file"] = audio_file
            self._segments.append(entry)

    def get_transcript(self) -> List[Dict]:
        """Return all collected segments ordered by start time."""
        logger.debug("Retrieving transcript with %d segments", len(self._segments))
        return sorted(self._segments, key=lambda s: s.get("start", 0.0))

    def rename_speaker(self, old_name: str, new_name: str) -> None:
        """Rename a speaker in all stored segments."""
        logger.info("Renaming speaker %s -> %s", old_name, new_name)
        for seg in self._segments:
            if seg.get("speaker") == old_name:
                seg["speaker"] = new_name
