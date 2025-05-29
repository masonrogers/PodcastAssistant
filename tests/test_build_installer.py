import os
import sys
import importlib
import types

# add src directory and repository root to path
BASE_DIR = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(BASE_DIR, '..', 'src'))
sys.path.insert(0, os.path.join(BASE_DIR, '..'))


def test_build_installer_creates_log(monkeypatch, tmp_path):
    logs_dir = tmp_path / 'logs'

    logging_setup = importlib.import_module('logging_setup')
    monkeypatch.setattr(logging_setup, 'LOG_DIR', logs_dir)
    monkeypatch.setattr(logging_setup, 'APP_LOG', logs_dir / 'app.log')
    monkeypatch.setattr(logging_setup, 'INSTALLER_LOG', logs_dir / 'installer_build.log')

    fake_run_called = {}

    def fake_run(args):
        fake_run_called['args'] = args

    pyinstaller = types.ModuleType('PyInstaller')
    pyinstaller.__path__ = []
    py_main = types.ModuleType('PyInstaller.__main__')
    py_main.run = fake_run
    pyinstaller.__main__ = py_main
    monkeypatch.setitem(sys.modules, 'PyInstaller', pyinstaller)
    monkeypatch.setitem(sys.modules, 'PyInstaller.__main__', py_main)

    # provide src.logging_setup without importing the full package
    fake_src = types.ModuleType('src')
    fake_src.logging_setup = logging_setup
    monkeypatch.setitem(sys.modules, 'src', fake_src)
    monkeypatch.setitem(sys.modules, 'src.logging_setup', logging_setup)

    build_installer = importlib.import_module('build_installer')
    build_installer.main()

    log_file = logs_dir / 'installer_build.log'
    assert log_file.exists()
    content = log_file.read_text()
    assert 'Starting PyInstaller build' in content
