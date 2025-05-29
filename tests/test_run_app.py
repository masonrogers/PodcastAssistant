import os
import sys
import types
import importlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_run_app_invokes_uninstaller(monkeypatch):
    runs = []

    qtwidgets = types.ModuleType('PySide6.QtWidgets')
    pyside6 = types.ModuleType('PySide6')
    pyside6.QtWidgets = qtwidgets
    monkeypatch.setitem(sys.modules, 'PySide6', pyside6)
    monkeypatch.setitem(sys.modules, 'PySide6.QtWidgets', qtwidgets)

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

