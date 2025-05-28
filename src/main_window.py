from __future__ import annotations

"""PySide6 GUI for the Podcast Assistant."""

from PySide6 import QtWidgets, QtCore

from transcript_exporter import export_txt, export_json, export_srt
from clip_exporter import ClipExporter

from settings import Settings
from keyword_index import KeywordIndex

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

    def __init__(self, settings: Settings | None = None) -> None:
        super().__init__()
        self.settings = settings or Settings()
        self.keyword_index = KeywordIndex(self.settings.keyword_path)
        self.setWindowTitle("Whisper Transcriber")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)

        self.file_list = QtWidgets.QListWidget()
        self.file_list.setAcceptDrops(True)
        self.file_list.setDragDropMode(
            QtWidgets.QAbstractItemView.InternalMove
        )
        layout.addWidget(self.file_list)

        search_row = QtWidgets.QHBoxLayout()
        self.search_bar = QtWidgets.QLineEdit()
        self.search_button = QtWidgets.QPushButton("Search")
        self.editorial_button = QtWidgets.QPushButton("Find Editorials")
        search_row.addWidget(self.search_bar)
        search_row.addWidget(self.search_button)
        search_row.addWidget(self.editorial_button)
        layout.addLayout(search_row)

        export_row = QtWidgets.QHBoxLayout()
        self.export_txt_button = QtWidgets.QPushButton("Export TXT")
        self.export_json_button = QtWidgets.QPushButton("Export JSON")
        self.export_srt_button = QtWidgets.QPushButton("Export SRT")
        self.export_segment_button = QtWidgets.QPushButton("Export Segment")
        self.rename_button = QtWidgets.QPushButton("Rename Speakers")
        export_row.addWidget(self.export_txt_button)
        export_row.addWidget(self.export_json_button)
        export_row.addWidget(self.export_srt_button)
        export_row.addWidget(self.export_segment_button)
        export_row.addWidget(self.rename_button)
        layout.addLayout(export_row)

        self.process_button = QtWidgets.QPushButton("Process Files")
        layout.addWidget(self.process_button)

        self.transcript = QtWidgets.QPlainTextEdit()
        layout.addWidget(self.transcript)

        self.results = QtWidgets.QPlainTextEdit()
        layout.addWidget(self.results)

        # Maintain running threads and aggregated transcript
        self.threads: list[QtCore.QThread] = []
        self.aggregator = TranscriptAggregator()
        self.clip_exporter = ClipExporter()
        self.current_index = 0
        self.processing = False

        self.search_button.clicked.connect(self._on_search)
        self.editorial_button.clicked.connect(self._on_find_editorials)
        self.export_txt_button.clicked.connect(self._on_export_txt)
        self.export_json_button.clicked.connect(self._on_export_json)
        self.export_srt_button.clicked.connect(self._on_export_srt)
        self.export_segment_button.clicked.connect(self._on_export_segment)
        self.rename_button.clicked.connect(self._on_rename_speakers)
        self.process_button.clicked.connect(self.start_processing)

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
        item.setData(QtCore.Qt.UserRole, (path, progress))
        self.file_list.addItem(item)
        self.file_list.setItemWidget(item, widget)

    def start_processing(self) -> None:
        """Begin processing files in the current list order."""
        if self.processing:
            return
        self.processing = True
        self.current_index = 0
        self._process_next()

    def _process_next(self) -> None:
        if self.current_index >= self.file_list.count():
            self.processing = False
            return
        item = self.file_list.item(self.current_index)
        path, progress = item.data(QtCore.Qt.UserRole)
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
        self.current_index += 1
        self._process_next()

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

    def _on_search(self) -> None:
        """Search transcript for query text and show results."""
        query = self.search_bar.text()
        segments = self.aggregator.get_transcript()
        results = self.keyword_index.search(segments, query)
        self._show_results(results)

    def _on_find_editorials(self) -> None:
        """Show segments matching any stored keyword."""
        segments = self.aggregator.get_transcript()
        results = self.keyword_index.find_all_editorial(segments)
        self._show_results(results)

    def _show_results(self, segments: list) -> None:
        """Display search results in the results pane."""
        self.results.appendPlainText("---")
        for seg in segments:
            text = f"[{seg.get('speaker', '')}] {seg.get('text', '')}\n"
            self.results.appendPlainText(text)

    def _refresh_transcript_display(self) -> None:
        """Refresh the transcript pane to reflect stored segments."""
        if hasattr(self.transcript, "clear"):
            self.transcript.clear()
        else:  # test stub
            self.transcript._text = ""
        for seg in self.aggregator.get_transcript():
            text = f"[{seg.get('speaker', '')}] {seg.get('text', '')}"
            self.transcript.appendPlainText(text)

    def _on_rename_speakers(self) -> None:
        """Prompt user to rename each detected speaker."""
        segments = self.aggregator.get_transcript()
        names = sorted({seg.get("speaker", "") for seg in segments})
        for name in names:
            new, ok = QtWidgets.QInputDialog.getText(
                self,
                "Rename Speaker",
                f"Enter new name for {name}",
                text=name,
            )
            if ok and new and new != name:
                self.aggregator.rename_speaker(name, new)
        self._refresh_transcript_display()

    # Export helpers
    def _export_transcript(self, exporter, filter_mask: str) -> None:
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Transcript", "", filter_mask)
        if not path:
            return
        segments = self.aggregator.get_transcript()
        data = exporter(segments)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(data)

    def _on_export_txt(self) -> None:
        self._export_transcript(export_txt, "Text Files (*.txt)")

    def _on_export_json(self) -> None:
        self._export_transcript(export_json, "JSON Files (*.json)")

    def _on_export_srt(self) -> None:
        self._export_transcript(export_srt, "SubRip (*.srt)")

    def _selected_segment(self):
        cursor = self.transcript.textCursor()
        line = cursor.blockNumber()
        segments = self.aggregator.get_transcript()
        if 0 <= line < len(segments):
            return segments[line]
        return None

    def _on_export_segment(self) -> None:
        seg = self._selected_segment()
        if not seg:
            return
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Segment", "", "Text Files (*.txt)")
        if not path:
            return
        text = export_txt([seg])
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        audio_path = path.rsplit(".", 1)[0] + ".wav"
        self.clip_exporter.export_clip(seg.get("file", ""), seg.get("start", 0.0), seg.get("end", 0.0), audio_path)
