from PySide6 import QtWidgets
from main_window import MainWindow


def main() -> None:
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":  # pragma: no cover - manual launch
    main()
