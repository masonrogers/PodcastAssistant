from typing import List, Dict

from transcribe_worker import TranscriptSegment


class TranscriptAggregator:
    def __init__(self):
        self.transcripts: List[Dict] = []

    def add(self, file_path: str, segments: List[TranscriptSegment]):
        self.transcripts.append({'file': file_path, 'segments': segments})

    def merged_text(self) -> str:
        lines = []
        for item in self.transcripts:
            for seg in item['segments']:
                lines.append(f"[{seg.start:.2f}] {seg.speaker}: {seg.text}")
        return '\n'.join(lines)
