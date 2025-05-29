"""Remove Whisper Transcriber files from an installation directory."""

from __future__ import annotations

import os
import shutil
from logging_setup import get_logger

logger = get_logger(__name__)


def remove_app_files(install_dir: str) -> None:
    """Delete all files under ``install_dir`` except the running uninstaller."""
    logger.info("Removing application files in %s", install_dir)
    exe_name = os.path.basename(__file__)
    for name in os.listdir(install_dir):
        if name == exe_name:
            continue
        path = os.path.join(install_dir, name)
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        except Exception as exc:  # pragma: no cover - OS-specific failures
            logger.error("Failed to remove %s: %s", path, exc)


if __name__ == "__main__":  # pragma: no cover - used by installer
    default_dir = os.path.dirname(__file__)
    remove_app_files(default_dir)
