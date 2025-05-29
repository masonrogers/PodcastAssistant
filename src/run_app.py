from logger import setup, get_logger
from bootstrapper import ensure_pyside6

setup()
logger = get_logger(__name__)
ensure_pyside6()

from PySide6 import QtWidgets
from main_window import MainWindow
from bootstrapper import Bootstrapper


def main() -> None:
    logger.info("Starting Whisper Transcriber")
    app = QtWidgets.QApplication([])

    bootstrapper = Bootstrapper()
    progress = QtWidgets.QProgressDialog(
        "Installing dependencies...", None, 0, 100
    )
    progress.setWindowTitle("Bootstrapping")
    progress.setAutoClose(False)
    progress.setAutoReset(False)

    bootstrapper.progress.connect(lambda p: progress.setValue(int(p * 100)))
    bootstrapper.finished.connect(progress.accept)

    bootstrapper.start()
    progress.exec()
    logger.info("Dependencies installed")

    window = MainWindow()
    window.show()
    logger.info("UI initialized")
    app.exec()


if __name__ == "__main__":  # pragma: no cover - manual launch
    main()
