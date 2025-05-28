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

    class QPlainTextEdit(StubObject):
        def __init__(self, *a, **kw):
            super().__init__(*a, **kw)
            self._text = ""

        def appendPlainText(self, t):
            if self._text:
                self._text += "\n"
            self._text += t

        def toPlainText(self):
            return self._text

    qtwidgets = types.ModuleType('PySide6.QtWidgets')
    for cls in [
        'QWidget',
        'QMainWindow',
        'QVBoxLayout',
        'QListWidget',
        'QProgressBar',
        'QListWidgetItem',
        'QHBoxLayout',
        'QLabel',
    ]:
        qtwidgets.__dict__[cls] = type(cls, (StubObject,), {})
    qtwidgets.QPlainTextEdit = QPlainTextEdit

    qtcore = types.ModuleType('PySide6.QtCore')
    qtcore.QThread = QThread
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


def test_add_file_triggers_threads(monkeypatch):
    stubs = make_pyside6_stub()
    for name, module in stubs.items():
        monkeypatch.setitem(sys.modules, name, module)

    class FakeTranscribeWorker:
        def __init__(self, *a, **k):
            pass

        def transcribe(self, path):
            return [{"start": 0.0, "end": 1.0, "speaker": "", "text": "hi"}]

    class FakeDiarizer:
        def __init__(self, *a, **k):
            pass

        def assign_speakers(self, audio_path, segments):
            for s in segments:
                s["speaker"] = "Spk1"
            return segments

    tw = types.ModuleType("transcribe_worker")
    tw.TranscribeWorker = FakeTranscribeWorker
    dr = types.ModuleType("diarizer")
    dr.Diarizer = FakeDiarizer
    monkeypatch.setitem(sys.modules, "transcribe_worker", tw)
    monkeypatch.setitem(sys.modules, "diarizer", dr)

    mw_module = importlib.import_module("main_window")
    mw_module = importlib.reload(mw_module)

    window = mw_module.MainWindow()
    window.add_file("a.wav")

    assert "[Spk1] hi" in window.transcript.toPlainText()
