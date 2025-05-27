import pytest
import gui


def test_gui_import():
    if gui.QtWidgets is None:
        with pytest.raises(RuntimeError):
            gui.MainWindow()
    else:
        win = gui.MainWindow()
        assert win.windowTitle()
