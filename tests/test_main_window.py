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
            pass

        def connect(self, slot):
            pass

        def emit(self, *args):
            pass

    qtwidgets = types.ModuleType('PySide6.QtWidgets')
    for cls in [
        'QWidget',
        'QMainWindow',
        'QVBoxLayout',
        'QListWidget',
        'QPlainTextEdit',
        'QProgressBar',
        'QListWidgetItem',
        'QHBoxLayout',
        'QLabel',
    ]:
        qtwidgets.__dict__[cls] = type(cls, (StubObject,), {})

    qtcore = types.ModuleType('PySide6.QtCore')
    qtcore.QThread = type('QThread', (StubObject,), {'start': lambda self: None})
    qtcore.QObject = StubObject
    qtcore.Signal = Signal

    pyside6 = types.ModuleType('PySide6')
    pyside6.QtWidgets = qtwidgets
    pyside6.QtCore = qtcore
    return {'PySide6': pyside6, 'PySide6.QtWidgets': qtwidgets, 'PySide6.QtCore': qtcore}


def test_main_window_instantiates(monkeypatch):
    stubs = make_pyside6_stub()
    for name, module in stubs.items():
        monkeypatch.setitem(sys.modules, name, module)

    tw = types.ModuleType('transcribe_worker')
    tw.TranscribeWorker = lambda *a, **k: None
    dr = types.ModuleType('diarizer')
    dr.Diarizer = lambda *a, **k: None
    monkeypatch.setitem(sys.modules, 'transcribe_worker', tw)
    monkeypatch.setitem(sys.modules, 'diarizer', dr)

    mw_module = importlib.import_module('main_window')
    mw_module = importlib.reload(mw_module)

    window = mw_module.MainWindow()
    assert window is not None
