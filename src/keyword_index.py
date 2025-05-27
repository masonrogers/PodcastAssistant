import json
from pathlib import Path
from typing import Dict, List

from transcribe_worker import TranscriptSegment


class KeywordIndex:
    def __init__(self, path: Path):
        self.path = path
        self.keywords: List[str] = []
        self.load()

    def load(self):
        if self.path.exists():
            self.keywords = json.loads(self.path.read_text())

    def save(self):
        self.path.write_text(json.dumps(self.keywords))

    def add(self, word: str):
        if word not in self.keywords:
            self.keywords.append(word)
            self.save()

    def search(self, transcript: str) -> List[str]:
        """Return keywords found in the provided transcript text."""
        return [kw for kw in self.keywords if kw.lower() in transcript.lower()]

    def search_segments(self, segments: List[TranscriptSegment]) -> Dict[str, List[TranscriptSegment]]:
        """Return segments that contain each keyword."""
        hits: Dict[str, List[TranscriptSegment]] = {kw: [] for kw in self.keywords}
        for seg in segments:
            for kw in self.keywords:
                if kw.lower() in seg.text.lower():
                    hits[kw].append(seg)
        return {k: v for k, v in hits.items() if v}

    def find_editorials(self, transcript: str) -> List[str]:
        return [line for line in transcript.splitlines() if 'EDITORIAL' in line.upper()]
