import os
import sys
import types
import importlib
import importlib.util
from pathlib import Path

# Add repo root and src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_build_installer_logs_created(monkeypatch):
    # stub PyInstaller
    run_args = []
    pyinstaller_main = types.ModuleType('PyInstaller.__main__')
    def fake_run(args):
        run_args.append(args)
    pyinstaller_main.run = fake_run
    pyinstaller = types.ModuleType('PyInstaller')
    pyinstaller.__main__ = pyinstaller_main
    monkeypatch.setitem(sys.modules, 'PyInstaller', pyinstaller)
    monkeypatch.setitem(sys.modules, 'PyInstaller.__main__', pyinstaller_main)

    # load real logging_setup without importing full src package
    spec = importlib.util.spec_from_file_location(
        'src.logging_setup',
        os.path.join(os.path.dirname(__file__), '..', 'src', 'logging_setup.py'),
    )
    logging_setup = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(logging_setup)
    stub_src = types.ModuleType('src')
    stub_src.logging_setup = logging_setup
    monkeypatch.setitem(sys.modules, 'src', stub_src)
    monkeypatch.setitem(sys.modules, 'src.logging_setup', logging_setup)

    # stub ffmpeg to satisfy src package imports
    fake_ffmpeg = types.ModuleType('ffmpeg')
    monkeypatch.setitem(sys.modules, 'ffmpeg', fake_ffmpeg)

    # stub certifi
    certifi = types.ModuleType('pip._vendor.certifi')
    certifi.where = lambda: '/fake/cert.pem'
    monkeypatch.setitem(sys.modules, 'pip._vendor.certifi', certifi)
    pip_mod = types.ModuleType('pip')
    pip_mod._vendor = types.ModuleType('pip._vendor')
    pip_mod._vendor.certifi = certifi
    monkeypatch.setitem(sys.modules, 'pip', pip_mod)
    monkeypatch.setitem(sys.modules, 'pip._vendor', pip_mod._vendor)

    # ensure log file removed
    log_file = Path(__file__).resolve().parent.parent / 'logs' / 'installer_build.log'
    if log_file.exists():
        log_file.unlink()

    build_installer = importlib.import_module('build_installer')
    build_installer = importlib.reload(build_installer)

    build_installer.main()

    assert run_args, 'PyInstaller.run was not called'
    assert f"--add-data=requirements.txt{os.pathsep}." in run_args[0]
    assert f"--add-data=src/uninstaller.py{os.pathsep}." in run_args[0]
    assert "--collect-all=whispercpp" in run_args[0]
    assert "--collect-binaries=whispercpp" in run_args[0]
    assert "--additional-hooks-dir=pyinstaller_hooks" in run_args[0]
    assert log_file.exists()
    assert 'Starting PyInstaller build' in log_file.read_text()

