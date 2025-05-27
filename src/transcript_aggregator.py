from typing import List, Dict


class TranscriptAggregator:
    def __init__(self):
        self.transcripts: List[Dict] = []

    def add(self, file_path: str, transcript: str):
        self.transcripts.append({'file': file_path, 'text': transcript})

    def merged_text(self) -> str:
        return '\n'.join(t['text'] for t in self.transcripts)
