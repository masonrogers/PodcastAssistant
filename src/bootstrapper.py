from __future__ import annotations

"""Install required packages at runtime if missing."""

import os
import sys
import subprocess
import importlib.util
import shutil
from logger import get_logger

logger = get_logger(__name__)


def pip_install(package: str) -> int:
    """Install *package* using pip via a subprocess."""
    logger.info("Installing %s", package)
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", package]
    )
    if result.returncode != 0:
        logger.error("Failed to install %s", package)
    return result.returncode


def ensure_pyside6() -> None:
    """Install PySide6 if it's not already available."""
    logger.debug("Checking for PySide6")
    if importlib.util.find_spec("PySide6") is None:
        logger.info("PySide6 not found; installing")
        pip_install("PySide6")


ensure_pyside6()


def ensure_ffmpeg() -> None:
    """Install FFmpeg and its Python wrapper if they're not available."""
    logger.debug("Checking for FFmpeg")
    if shutil.which("ffmpeg") is None:
        logger.info("FFmpeg binary not found; installing ffmpeg-static")
        pip_install("ffmpeg-static")
    if importlib.util.find_spec("ffmpeg") is None:
        logger.info("ffmpeg-python not found; installing")
        pip_install("ffmpeg-python")


ensure_ffmpeg()

from PySide6 import QtCore


class Bootstrapper(QtCore.QThread):
    """Check and install dependencies listed in requirements.txt."""

    progress = QtCore.Signal(float)
    finished = QtCore.Signal()

    def __init__(self, requirements_path: str | None = None, parent=None) -> None:
        super().__init__(parent)
        if requirements_path is None:
            requirements_path = os.path.join(os.path.dirname(__file__), '..', 'requirements.txt')
        self.requirements_path = os.path.abspath(requirements_path)

    def _read_packages(self) -> list[str]:
        logger.debug("Reading packages from %s", self.requirements_path)
        with open(self.requirements_path, 'r', encoding='utf-8') as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith('#')]

    def _missing_packages(self, packages: list[str]) -> list[str]:
        missing = []
        for pkg in packages:
            name = pkg.split('==')[0]
            if importlib.util.find_spec(name) is None:
                logger.debug("Package %s missing", name)
                missing.append(pkg)
        return missing

    def run(self) -> None:  # pragma: no cover - integration with PySide6 runtime
        logger.info("Bootstrapping dependencies")
        pkgs = self._read_packages()
        missing = self._missing_packages(pkgs)
        total = len(missing)
        for i, pkg in enumerate(missing):
            pip_install(pkg)
            if total:
                self.progress.emit((i + 1) / total)
        self.finished.emit()
