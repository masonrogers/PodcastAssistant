from typing import List, Dict

class TranscriptAggregator:
    """Collects transcript segments from multiple audio files."""

    def __init__(self):
        self._segments: List[Dict] = []

    def add_segments(self, audio_file: str, segments: List[Dict]):
        """Add segments for the given audio file.

        Each segment will be copied and annotated with the source filename.
        """
        for seg in segments:
            entry = seg.copy()
            entry["file"] = audio_file
            self._segments.append(entry)

    def get_transcript(self) -> List[Dict]:
        """Return all collected segments ordered by start time."""
        return sorted(self._segments, key=lambda s: s.get("start", 0.0))

    def rename_speaker(self, old_name: str, new_name: str) -> None:
        """Rename a speaker in all stored segments."""
        for seg in self._segments:
            if seg.get("speaker") == old_name:
                seg["speaker"] = new_name
