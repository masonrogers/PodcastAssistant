from logging_setup import setup_logging, get_logger
import os
import sys

setup_logging()
logger = get_logger(__name__)

from PySide6 import QtWidgets
from main_window import MainWindow


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1].endswith("uninstaller.py"):
        if getattr(sys, "frozen", False):
            app_dir = os.path.dirname(sys.executable)
        else:
            app_dir = os.path.dirname(os.path.dirname(__file__))
        import uninstaller
        uninstaller.remove_app_files(app_dir)
        return

    logger.info("Starting application")
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":  # pragma: no cover - manual launch
    main()
