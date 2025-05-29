import os
import sys
import types
import importlib
from test_main_window import make_pyside6_stub

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_run_app_invokes_uninstaller(monkeypatch):
    runs = []

    stubs = make_pyside6_stub()
    for name, module in stubs.items():
        monkeypatch.setitem(sys.modules, name, module)

    mw = types.ModuleType('main_window')
    mw.MainWindow = lambda: None
    monkeypatch.setitem(sys.modules, 'main_window', mw)

    un = types.ModuleType('uninstaller')
    def fake_remove(path):
        runs.append(path)
    un.remove_app_files = fake_remove
    monkeypatch.setitem(sys.modules, 'uninstaller', un)

    monkeypatch.setattr(sys, 'argv', ['run_app.py', 'uninstaller.py'])

    mod = importlib.import_module('run_app')
    mod = importlib.reload(mod)

    mod.main()

    expected = os.path.dirname(os.path.dirname(mod.__file__))
    assert runs == [expected]


def test_run_app_starts_without_progress_dialog(monkeypatch):
    stubs = make_pyside6_stub()
    for name, module in stubs.items():
        monkeypatch.setitem(sys.modules, name, module)

    def fail(*a, **k):
        raise AssertionError("Progress dialog shown")

    stubs['PySide6.QtWidgets'].QProgressDialog = fail

    shown = []
    class DummyApp:
        def __init__(self, *a, **k):
            shown.append('app')
        def exec(self):
            shown.append('exec')
    stubs['PySide6.QtWidgets'].QApplication = DummyApp

    class DummyWindow:
        def show(self):
            shown.append('show')

    mw = types.ModuleType('main_window')
    mw.MainWindow = DummyWindow
    monkeypatch.setitem(sys.modules, 'main_window', mw)

    monkeypatch.setattr(sys, 'argv', ['run_app.py'])

    mod = importlib.import_module('run_app')
    mod = importlib.reload(mod)

    mod.main()

    assert shown == ['app', 'show', 'exec']

