from __future__ import annotations

"""Install required packages at runtime if missing."""

import os
import sys
import subprocess
import importlib.util
import shutil
from logging_setup import get_logger

logger = get_logger(__name__)


def pip_install(package: str) -> int:
    """Install *package* using pip via a subprocess."""
    logger.info("Installing package %s", package)
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", package]
    )
    logger.debug("pip install return code: %s", result.returncode)
    return result.returncode


def ensure_pyside6() -> None:
    """Install PySide6 if it's not already available."""
    if importlib.util.find_spec("PySide6") is None:
        logger.info("PySide6 missing, installing...")
        pip_install("PySide6")


ensure_pyside6()


def ensure_ffmpeg() -> None:
    """Install FFmpeg and its Python wrapper if they're not available."""
    if shutil.which("ffmpeg") is None:
        logger.info("FFmpeg executable missing, installing ffmpeg-static...")
        pip_install("ffmpeg-static")
    if importlib.util.find_spec("ffmpeg") is None:
        logger.info("ffmpeg Python module missing, installing ffmpeg-python...")
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
            if getattr(sys, 'frozen', False):
                requirements_path = os.path.join(
                    os.path.dirname(sys.executable),
                    'requirements.txt',
                )
            else:
                requirements_path = os.path.join(
                    os.path.dirname(__file__),
                    '..',
                    'requirements.txt',
                )
        self.requirements_path = os.path.abspath(requirements_path)

    def _read_packages(self) -> list[str]:
        logger.debug("Reading requirements from %s", self.requirements_path)
        with open(self.requirements_path, 'r', encoding='utf-8') as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith('#')]

    def _missing_packages(self, packages: list[str]) -> list[str]:
        missing = []
        for pkg in packages:
            name = pkg.split('==')[0]
            try:
                importlib.import_module(name)
            except ImportError:
                missing.append(pkg)
        return missing

    def run(self) -> None:  # pragma: no cover - integration with PySide6 runtime
        logger.info("Checking for missing packages")
        pkgs = self._read_packages()
        missing = self._missing_packages(pkgs)
        total = len(missing)
        for i, pkg in enumerate(missing):
            pip_install(pkg)
            if total:
                self.progress.emit((i + 1) / total)
        self.finished.emit()
