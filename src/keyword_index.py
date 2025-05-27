import json
from pathlib import Path
from typing import List


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
        return [kw for kw in self.keywords if kw.lower() in transcript.lower()]

    def find_editorials(self, transcript: str) -> List[str]:
        return [line for line in transcript.splitlines() if 'EDITORIAL' in line.upper()]
