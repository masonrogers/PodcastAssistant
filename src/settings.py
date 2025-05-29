"""Manage persistent application settings.

Usage:
    from settings import Settings
    s = Settings()
    s.ui["theme"] = "dark"
    s.keyword_path = "C:/path/keywords.json"
    s.save()
"""

import json
import os
from typing import Dict
from logging_setup import get_logger

logger = get_logger(__name__)


class Settings:
    """Store UI preferences and keyword list location."""

    def __init__(self, path: str | None = None):
        if path is None:
            base = os.getenv("APPDATA") or os.path.expanduser("~")
            path = os.path.join(base, "WhisperTranscriber", "settings.json")
        self.path = path
        self.ui: Dict[str, str] = {}
        self.keyword_path: str = os.path.join(os.path.dirname(self.path), "keywords.json")
        self.load()

    def load(self) -> None:
        """Load settings from disk if available, else defaults."""
        try:
            logger.debug("Loading settings from %s", self.path)
            with open(self.path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            self.ui = data.get("ui", {})
            self.keyword_path = data.get("keyword_path", self.keyword_path)
        except FileNotFoundError:
            logger.info("Settings file not found, using defaults")
            # defaults already set in __init__
            self.ui = {}

    def save(self) -> None:
        """Persist current settings to disk."""
        logger.info("Saving settings to %s", self.path)
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as fh:
            json.dump({"ui": self.ui, "keyword_path": self.keyword_path}, fh, indent=2)
