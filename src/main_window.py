from __future__ import annotations

"""PySide6 GUI for the Podcast Assistant."""

from PySide6 import QtWidgets, QtCore

from transcribe_worker import TranscribeWorker
from diarizer import Diarizer
from transcript_aggregator import TranscriptAggregator


class TranscriberThread(QtCore.QThread):
    """Thread wrapper around :class:`TranscribeWorker`."""

    progress = QtCore.Signal(float)
    finished = QtCore.Signal(list)

    def __init__(self, audio_path: str, model: str = "base", parent=None) -> None:
        super().__init__(parent)
        self.audio_path = audio_path
        self.worker = TranscribeWorker(model)

    def run(self) -> None:  # pragma: no cover - not exercised in tests
        segments = self.worker.transcribe(self.audio_path)
        self.progress.emit(1.0)
        self.finished.emit(segments)


class DiarizerThread(QtCore.QThread):
    """Thread wrapper around :class:`Diarizer`."""

    progress = QtCore.Signal(float)
    finished = QtCore.Signal(list)

    def __init__(self, audio_path: str, segments: list, parent=None) -> None:
        super().__init__(parent)
        self.audio_path = audio_path
        self.segments = segments
        self.worker = Diarizer()

    def run(self) -> None:  # pragma: no cover - not exercised in tests
        labeled = self.worker.assign_speakers(self.audio_path, self.segments)
        self.progress.emit(1.0)
        self.finished.emit(labeled)


class MainWindow(QtWidgets.QMainWindow):
    """Main application window with drag-drop file list and transcript viewer."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Whisper Transcriber")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)

        self.file_list = QtWidgets.QListWidget()
        self.file_list.setAcceptDrops(True)
        layout.addWidget(self.file_list)

        self.transcript = QtWidgets.QPlainTextEdit()
        layout.addWidget(self.transcript)

        # Maintain running threads and aggregated transcript
        self.threads: list[QtCore.QThread] = []
        self.aggregator = TranscriptAggregator()

    # Drag and drop events
    def dragEnterEvent(self, event):  # pragma: no cover - relies on GUI runtime
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):  # pragma: no cover - relies on GUI runtime
        for url in event.mimeData().urls():
            self.add_file(url.toLocalFile())

    def add_file(self, path: str) -> None:
        """Add an audio file entry with a progress bar."""
        item = QtWidgets.QListWidgetItem(path)
        widget = QtWidgets.QWidget()
        h = QtWidgets.QHBoxLayout(widget)
        h.setContentsMargins(0, 0, 0, 0)
        label = QtWidgets.QLabel(path)
        progress = QtWidgets.QProgressBar()
        progress.setRange(0, 100)
        h.addWidget(label)
        h.addWidget(progress)
        self.file_list.addItem(item)
        self.file_list.setItemWidget(item, widget)
        # Start transcription and diarization threads
        t_thread = TranscriberThread(path, parent=self)
        self.threads.append(t_thread)
        t_thread.progress.connect(lambda p: progress.setValue(int(p * 50)))

        def on_transcribed(segs: list) -> None:
            d_thread = DiarizerThread(path, segs, parent=self)
            self.threads.append(d_thread)
            d_thread.progress.connect(
                lambda p: progress.setValue(50 + int(p * 50))
            )
            d_thread.finished.connect(
                lambda labeled: self._on_diarized(path, labeled, progress)
            )
            d_thread.start()

        t_thread.finished.connect(on_transcribed)
        t_thread.start()

    def _on_diarized(self, path: str, segments: list, progress: QtWidgets.QProgressBar) -> None:
        """Handle diarization completion for a file."""
        self.aggregator.add_segments(path, segments)
        self.display_segments(segments)
        progress.setValue(100)

    # Placeholder hooks for workers
    def start_transcription(self, path: str) -> None:
        """Start transcribing a file."""
        thread = TranscriberThread(path, parent=self)
        thread.finished.connect(lambda segs: self.display_segments(segs))
        thread.start()

    def display_segments(self, segments: list) -> None:
        """Append segments to the transcript display."""
        for seg in segments:
            text = f"[{seg.get('speaker', '')}] {seg.get('text', '')}\n"
            self.transcript.appendPlainText(text)
