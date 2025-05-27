import json
import os
from pathlib import Path
from dataclasses import dataclass, field


APP_DIR = Path(os.getenv('APPDATA') or Path.home() / '.whisper_transcriber')
SETTINGS_FILE = APP_DIR / 'settings.json'


@dataclass
class Settings:
    keyword_path: Path = field(default=APP_DIR / 'keywords.json')

    def load(self):
        if SETTINGS_FILE.exists():
            data = json.loads(SETTINGS_FILE.read_text())
            self.keyword_path = Path(data.get('keyword_path', self.keyword_path))

    def save(self):
        APP_DIR.mkdir(parents=True, exist_ok=True)
        SETTINGS_FILE.write_text(json.dumps({'keyword_path': str(self.keyword_path)}))
