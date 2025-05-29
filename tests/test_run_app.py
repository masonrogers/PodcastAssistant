import os
import sys
import types
import importlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_run_app_invokes_uninstaller(monkeypatch):
    runs = []

    boot = types.ModuleType('bootstrapper')
    boot.ensure_pyside6 = lambda: None
    boot.Bootstrapper = lambda *a, **k: None
    monkeypatch.setitem(sys.modules, 'bootstrapper', boot)

    qtwidgets = types.ModuleType('PySide6.QtWidgets')
    pyside6 = types.ModuleType('PySide6')
    pyside6.QtWidgets = qtwidgets
    monkeypatch.setitem(sys.modules, 'PySide6', pyside6)
    monkeypatch.setitem(sys.modules, 'PySide6.QtWidgets', qtwidgets)

    un = types.ModuleType('uninstaller')
    def fake_uninstall(path):
        runs.append(path)
    un.uninstall_packages = fake_uninstall
    monkeypatch.setitem(sys.modules, 'uninstaller', un)

    monkeypatch.setattr(sys, 'argv', ['run_app.py', 'uninstaller.py'])

    mod = importlib.import_module('run_app')
    mod = importlib.reload(mod)

    mod.main()

    expected = os.path.join(os.path.dirname(mod.__file__), '..', 'requirements.txt')
    assert runs == [expected]
