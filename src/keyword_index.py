import json
from typing import List, Dict
from logger import get_logger

logger = get_logger(__name__)


class KeywordIndex:
    """Manage persistent keyword lists and provide search utilities."""

    def __init__(self, path: str):
        self.path = path
        self.keywords: List[str] = []
        logger.debug("KeywordIndex path set to %s", path)
        self.load()

    def load(self) -> None:
        """Load keywords from disk if the file exists."""
        try:
            with open(self.path, "r", encoding="utf-8") as fh:
                self.keywords = json.load(fh)
            logger.info("Loaded %d keywords", len(self.keywords))
        except FileNotFoundError:
            self.keywords = []

    def save(self) -> None:
        """Persist the current keywords to disk."""
        logger.info("Saving %d keywords", len(self.keywords))
        with open(self.path, "w", encoding="utf-8") as fh:
            json.dump(self.keywords, fh, indent=2)

    def add_keyword(self, keyword: str) -> None:
        """Add a keyword to the list and save if not already present."""
        if keyword not in self.keywords:
            self.keywords.append(keyword)
            logger.debug("Added keyword: %s", keyword)
            self.save()

    def remove_keyword(self, keyword: str) -> None:
        """Remove a keyword from the list and save."""
        if keyword in self.keywords:
            self.keywords.remove(keyword)
            logger.debug("Removed keyword: %s", keyword)
            self.save()

    def search(self, segments: List[Dict], query: str) -> List[Dict]:
        """Return transcript segments containing the given text query."""
        query_lc = query.lower()
        logger.info("Searching for '%s'", query)
        return [seg for seg in segments if query_lc in seg.get("text", "").lower()]

    def find_all_editorial(self, segments: List[Dict]) -> List[Dict]:
        """Return segments that contain any stored keyword."""
        logger.info("Finding segments matching keywords")
        keywords_lc = [k.lower() for k in self.keywords]
        results = []
        for seg in segments:
            text_lc = seg.get("text", "").lower()
            if any(k in text_lc for k in keywords_lc):
                results.append(seg)
        return results
