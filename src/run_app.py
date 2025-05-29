from logging_setup import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)

from bootstrapper import ensure_pyside6

ensure_pyside6()

from PySide6 import QtWidgets
from bootstrapper import Bootstrapper


def main() -> None:
    logger.info("Starting application")
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

    logger.info("Initializing main window")
    from main_window import MainWindow
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":  # pragma: no cover - manual launch
    main()
