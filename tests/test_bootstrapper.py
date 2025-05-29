import os
import sys
import types
import importlib
import shutil
import subprocess

# add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def make_pyside6_stub():
    class StubObject:
        def __init__(self, *a, **kw):
            pass

        def __getattr__(self, name):
            def method(*a, **kw):
                return None
            return method

    class Signal:
        def __init__(self, *a):
            self._slots = []

        def connect(self, slot):
            self._slots.append(slot)

        def emit(self, *args):
            for s in list(self._slots):
                s(*args)

    class QThread(StubObject):
        def start(self):
            if hasattr(self, "run"):
                self.run()

    qtcore = types.ModuleType('PySide6.QtCore')
    qtcore.QThread = QThread
    qtcore.QObject = StubObject
    qtcore.Signal = Signal

    pyside6 = types.ModuleType('PySide6')
    pyside6.QtCore = qtcore

    return {'PySide6': pyside6, 'PySide6.QtCore': qtcore}


def test_bootstrapper_installs_missing(monkeypatch, tmp_path):
    stubs = make_pyside6_stub()
    for name, module in stubs.items():
        monkeypatch.setitem(sys.modules, name, module)

    missing = {'pkgA': True, 'pkgB': False, 'pkgC': True}

    def fake_find_spec(name):
        if missing.get(name):
            return None
        return object()

    runs = []

    class Result:
        returncode = 0

    def fake_run(cmd, *a, **kw):
        runs.append(cmd[-1])
        return Result()

    monkeypatch.setattr(importlib.util, 'find_spec', fake_find_spec)
    monkeypatch.setattr(shutil, 'which', lambda name: '/usr/bin/ffmpeg')
    monkeypatch.setattr(subprocess, 'run', fake_run)

    req_path = tmp_path / 'reqs.txt'
    req_path.write_text('pkgA\npkgB\npkgC\n')

    sys.modules.pop('bootstrapper', None)
    bs_module = importlib.import_module('bootstrapper')
    boot = bs_module.Bootstrapper(str(req_path))

    progress = []
    boot.progress.connect(lambda p: progress.append(p))
    boot.finished.connect(lambda: progress.append('done'))

    boot.run()

    expected_runs = ['pkgA', 'pkgC']
    assert runs == expected_runs
    assert progress == [0.5, 1.0, 'done']


def test_ensure_pyside6_installs_when_missing_and_skips_when_present(monkeypatch):
    """ensure_pyside6 installs PySide6 only if it's missing."""
    stubs = make_pyside6_stub()
    for name, module in stubs.items():
        monkeypatch.setitem(sys.modules, name, module)

    runs = []

    class Result:
        returncode = 0

    def fake_run(cmd, *a, **kw):
        runs.append(cmd[-1])
        return Result()

    monkeypatch.setattr(shutil, 'which', lambda name: '/usr/bin/ffmpeg')
    monkeypatch.setattr(subprocess, 'run', fake_run)

    # PySide6 missing -> installation should occur. FFmpeg is present so no
    # additional packages are installed.
    def fake_find_spec(name):
        if name == 'PySide6':
            return None
        return object()

    monkeypatch.setattr(importlib.util, 'find_spec', fake_find_spec)
    sys.modules.pop('bootstrapper', None)
    bs_module = importlib.import_module('bootstrapper')

    assert runs == ['PySide6']

    # PySide6 present -> no installation attempt
    runs.clear()
    monkeypatch.setattr(importlib.util, 'find_spec', lambda name: object())
    bs_module.ensure_pyside6()

    assert runs == []


def test_ensure_ffmpeg_installs_when_missing_and_skips_when_present(monkeypatch):
    """ensure_ffmpeg installs ffmpeg dependencies only when missing."""
    stubs = make_pyside6_stub()
    for name, module in stubs.items():
        monkeypatch.setitem(sys.modules, name, module)

    runs = []

    class Result:
        returncode = 0

    def fake_run(cmd, *a, **kw):
        runs.append(cmd[-1])
        return Result()

    # FFmpeg and module missing -> installation should occur
    def fake_find_spec(name):
        return None if name == 'ffmpeg' else object()

    monkeypatch.setattr(importlib.util, 'find_spec', fake_find_spec)
    monkeypatch.setattr(shutil, 'which', lambda name: None)
    monkeypatch.setattr(subprocess, 'run', fake_run)
    sys.modules.pop('bootstrapper', None)
    bs_module = importlib.import_module('bootstrapper')

    assert runs == [
        'ffmpeg-static',
        'ffmpeg-python',
    ]

    # FFmpeg present -> no installation attempt
    runs.clear()
    monkeypatch.setattr(shutil, 'which', lambda name: '/usr/bin/ffmpeg')
    monkeypatch.setattr(importlib.util, 'find_spec', lambda name: object())
    bs_module.ensure_ffmpeg()

    assert runs == []
