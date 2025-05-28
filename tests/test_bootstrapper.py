import os
import sys
import types
import importlib

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

    def fake_run(args, check=False):
        runs.append(args)

    monkeypatch.setattr(importlib.util, 'find_spec', fake_find_spec)
    import subprocess
    monkeypatch.setattr(subprocess, 'run', fake_run)

    req_path = tmp_path / 'reqs.txt'
    req_path.write_text('pkgA\npkgB\npkgC\n')

    bs_module = importlib.import_module('bootstrapper')
    bs_module = importlib.reload(bs_module)
    boot = bs_module.Bootstrapper(str(req_path))

    progress = []
    boot.progress.connect(lambda p: progress.append(p))
    boot.finished.connect(lambda: progress.append('done'))

    boot.run()

    expected_runs = [
        [sys.executable, '-m', 'pip', 'install', 'pkgA'],
        [sys.executable, '-m', 'pip', 'install', 'pkgC'],
    ]
    assert runs == expected_runs
    assert progress == [0.5, 1.0, 'done']
