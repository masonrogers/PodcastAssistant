"""Utilities to export transcript segments to various text formats."""

from __future__ import annotations

import json
from typing import List, Dict
from logging_setup import get_logger

logger = get_logger(__name__)


def export_txt(segments: List[Dict]) -> str:
    """Return the transcript as plain text with each segment on a new line."""
    logger.info("Exporting %d segments as TXT", len(segments))
    lines = [seg.get("text", "") for seg in segments]
    return "\n".join(lines)


def export_json(segments: List[Dict]) -> str:
    """Return the transcript segments serialized as formatted JSON."""
    logger.info("Exporting %d segments as JSON", len(segments))
    return json.dumps(segments, indent=2, ensure_ascii=False)


def _format_timestamp(seconds: float) -> str:
    """Return a timestamp in ``HH:MM:SS,mmm`` format."""
    millis_total = int(round(seconds * 1000))
    seconds_total, millis = divmod(millis_total, 1000)
    minutes_total, secs = divmod(seconds_total, 60)
    hours, minutes = divmod(minutes_total, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def export_srt(segments: List[Dict]) -> str:
    """Return the transcript in SubRip (SRT) subtitle format."""
    logger.info("Exporting %d segments as SRT", len(segments))
    lines: List[str] = []
    for idx, seg in enumerate(segments, 1):
        start = _format_timestamp(float(seg.get("start", 0.0)))
        end = _format_timestamp(float(seg.get("end", 0.0)))
        text = seg.get("text", "")
        lines.append(str(idx))
        lines.append(f"{start} --> {end}")
        lines.append(text)
        lines.append("")  # blank line after each entry
    return "\n".join(lines).rstrip()  # remove trailing newline
