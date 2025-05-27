try:
    from PySide6 import QtWidgets, QtCore
except Exception:  # PySide6 not installed
    QtWidgets = None
    QtCore = None


class MainWindow(QtWidgets.QMainWindow if QtWidgets else object):
    """Minimal GUI placeholder for Whisper Transcriber."""

    def __init__(self):
        if not QtWidgets:
            raise RuntimeError("PySide6 not available")
        super().__init__()
        self.setWindowTitle("Whisper Transcriber")
        self.text = QtWidgets.QTextEdit()
        self.setCentralWidget(self.text)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):  # type: ignore[override]
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):  # type: ignore[override]
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            self.text.append(f)
