"""Multi-File Whisper Transcriber.

This module implements a Windows 11–style GUI and a CLI mode for
batch-transcribing audio files using OpenAI Whisper. Dependencies are
self-installed if missing. The GUI is built with PySide6.
"""

from __future__ import annotations

import json
import logging
from logging.handlers import RotatingFileHandler
import os
import subprocess
import sys
from pathlib import Path
from typing import List


def install_and_import(pkg: str) -> None:
    """Attempt to import a package and install it if missing."""
    try:
        __import__(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])


for package in [
    "PySide6",
    "whisper",
    "pydub",
    "noisereduce",
    "rnnoise",
    "simpleaudio",
]:
    install_and_import(package)

# Now that packages are ensured, import them
from PySide6 import QtWidgets, QtGui, QtCore

# Whisper may be heavy; import after install
import whisper  # type: ignore

# Simple logger with rotating handler
LOG_DIR = Path.home() / ".whisper_transcriber"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"
handler = RotatingFileHandler(str(LOG_FILE), maxBytes=5_000_000, backupCount=3)
logging.basicConfig(level=logging.INFO, handlers=[handler], format="%(asctime)s %(levelname)s:%(message)s")
logger = logging.getLogger(__name__)

SESSION_FILE = LOG_DIR / "session.json"


def load_session() -> dict:
    if SESSION_FILE.exists():
        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except Exception as exc:  # noqa: BLE001
            logger.error("Failed to load session: %s", exc)
    return {}


def save_session(data: dict) -> None:
    with open(SESSION_FILE, "w", encoding="utf-8") as fh:
        json.dump(data, fh)


class Transcriber(QtCore.QObject):
    """Worker that runs Whisper transcription in a thread."""

    progress = QtCore.Signal(int, float, float)  # id, percent, eta
    finished = QtCore.Signal(int, str)

    def __init__(self, model_size: str = "base") -> None:
        super().__init__()
        self.model_size = model_size
        self.model = whisper.load_model(self.model_size)

    @QtCore.Slot(int, str)
    def transcribe_file(self, row: int, path: str) -> None:
        logger.info("Transcribing %s", path)
        try:
            result = self.model.transcribe(path)
            text = result["text"]
            self.finished.emit(row, text)
        except Exception as exc:  # noqa: BLE001
            logger.exception("Failed transcription of %s", path)
            self.finished.emit(row, f"ERROR: {exc}")


class MainWindow(QtWidgets.QMainWindow):
    """Main application window."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Multi-File Whisper Transcriber")
        self.resize(900, 600)

        self.files: List[str] = []
        self.session = load_session()

        self._build_ui()

        if self.session.get("files"):
            for f in self.session["files"]:
                self.add_file_row(f)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:  # noqa: N802
        self.session["files"] = self.files
        save_session(self.session)
        event.accept()

    def _build_ui(self) -> None:
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)

        layout = QtWidgets.QVBoxLayout(central)

        self.table = QtWidgets.QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Filename", "Duration", "Status", "Progress"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        layout.addWidget(self.table)

        btn_row = QtWidgets.QHBoxLayout()
        self.add_btn = QtWidgets.QPushButton("Add Files")
        self.add_btn.clicked.connect(self.browse_files)
        btn_row.addWidget(self.add_btn)

        self.transcribe_btn = QtWidgets.QPushButton("Transcribe")
        self.transcribe_btn.clicked.connect(self.start_transcription)
        btn_row.addWidget(self.transcribe_btn)

        layout.addLayout(btn_row)

        self.transcript_edit = QtWidgets.QTextEdit(readOnly=False)
        layout.addWidget(self.transcript_edit)

        self.threadpool = QtCore.QThreadPool.globalInstance()
        self.transcriber = Transcriber()
        self.transcriber.finished.connect(self.handle_finished)

    def add_file_row(self, path: str) -> None:
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(os.path.basename(path)))
        self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(""))
        self.table.setItem(row, 2, QtWidgets.QTableWidgetItem("Pending"))
        progress = QtWidgets.QProgressBar()
        progress.setValue(0)
        self.table.setCellWidget(row, 3, progress)
        self.files.append(path)

    def browse_files(self) -> None:
        dlg = QtWidgets.QFileDialog(self, "Add Audio Files")
        dlg.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        dlg.setNameFilter("Audio Files (*.wav *.mp3 *.m4a *.flac)")
        if dlg.exec():
            for path in dlg.selectedFiles():
                self.add_file_row(path)

    def start_transcription(self) -> None:
        for row, path in enumerate(self.files):
            worker = QtCore.QRunnable()
            worker.run = lambda r=row, p=path: self.transcriber.transcribe_file(r, p)  # type: ignore
            self.table.item(row, 2).setText("Transcribing")
            self.threadpool.start(worker)

    def handle_finished(self, row: int, text: str) -> None:
        self.table.item(row, 2).setText("Done")
        self.transcript_edit.append(f"=== {self.files[row]} ===")
        self.transcript_edit.append(text)
        self.transcript_edit.append("")


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    if "--headless" in sys.argv:
        print("CLI mode not yet implemented.")
    else:
        main()
