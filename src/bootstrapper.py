from __future__ import annotations

"""Install required packages at runtime if missing."""

import os
import sys
import subprocess
import importlib.util


def ensure_pyside6() -> None:
    """Install PySide6 if it's not already available."""
    if importlib.util.find_spec("PySide6") is None:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "PySide6"], check=False
        )


ensure_pyside6()

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
        with open(self.requirements_path, 'r', encoding='utf-8') as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith('#')]

    def _missing_packages(self, packages: list[str]) -> list[str]:
        missing = []
        for pkg in packages:
            name = pkg.split('==')[0]
            if importlib.util.find_spec(name) is None:
                missing.append(pkg)
        return missing

    def run(self) -> None:  # pragma: no cover - integration with PySide6 runtime
        pkgs = self._read_packages()
        missing = self._missing_packages(pkgs)
        total = len(missing)
        for i, pkg in enumerate(missing):
            subprocess.run([sys.executable, '-m', 'pip', 'install', pkg], check=False)
            if total:
                self.progress.emit((i + 1) / total)
        self.finished.emit()
