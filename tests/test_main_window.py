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
            self._slots = {}

        def __get__(self, instance, owner):
            if instance is None:
                return self
            slots = self._slots.setdefault(instance, [])

            class Bound:
                def connect(self_inner, slot):
                    slots.append(slot)

                def emit(self_inner, *args):
                    for s in list(slots):
                        s(*args)

            return Bound()

    class QThread(StubObject):
        def start(self):
            if hasattr(self, "run"):
                self.run()

    class QPlainTextEdit(StubObject):
        def __init__(self, *a, **kw):
            super().__init__(*a, **kw)
            self._text = ""
            self._selected_line = 0

        def appendPlainText(self, t):
            if self._text:
                self._text += "\n"
            self._text += t

        def toPlainText(self):
            return self._text

        def textCursor(self):
            parent = self

            class Cursor:
                def blockNumber(self):
                    return parent._selected_line

            return Cursor()

        def set_selected_line(self, line):
            self._selected_line = line

    class QLineEdit(StubObject):
        def __init__(self, *a, **kw):
            super().__init__(*a, **kw)
            self._text = ""

        def text(self):
            return self._text

        def setText(self, t):
            self._text = t

    class QPushButton(StubObject):
        clicked = Signal()
        def __init__(self, *a, **kw):
            super().__init__(*a, **kw)

    class QFileDialog(StubObject):
        @staticmethod
        def getSaveFileName(*a, **kw):
            return ("", "")

    class QListWidgetItem(StubObject):
        def __init__(self, text=""):
            self._text = text
            self._data = {}

        def text(self):
            return self._text

        def setData(self, role, value):
            self._data[role] = value

        def data(self, role):
            return self._data.get(role)

    class QListWidget(StubObject):
        def __init__(self, *a, **kw):
            super().__init__(*a, **kw)
            self.items = []
            self.dragDropMode = None

        def addItem(self, item):
            self.items.append(item)

        def setItemWidget(self, item, widget):
            item.widget = widget

        def count(self):
            return len(self.items)

        def item(self, index):
            return self.items[index]

        def takeItem(self, index):
            return self.items.pop(index)

        def insertItem(self, index, item):
            self.items.insert(index, item)

        def setDragDropMode(self, mode):
            self.dragDropMode = mode

    qtwidgets = types.ModuleType('PySide6.QtWidgets')
    for cls in [
        'QWidget',
        'QMainWindow',
        'QVBoxLayout',
        'QProgressBar',
        'QHBoxLayout',
        'QLabel',
    ]:
        qtwidgets.__dict__[cls] = type(cls, (StubObject,), {})
    qtwidgets.QPlainTextEdit = QPlainTextEdit
    qtwidgets.QLineEdit = QLineEdit
    qtwidgets.QPushButton = QPushButton
    qtwidgets.QFileDialog = QFileDialog
    qtwidgets.QListWidget = QListWidget
    qtwidgets.QListWidgetItem = QListWidgetItem

    qtcore = types.ModuleType('PySide6.QtCore')
    qtcore.QThread = QThread
    qtcore.QObject = StubObject
    qtcore.Signal = Signal
    qtcore.Qt = types.SimpleNamespace(UserRole=0)

    qtwidgets.QAbstractItemView = types.SimpleNamespace(InternalMove=1)
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
    kw = types.ModuleType('keyword_index')
    kw.KeywordIndex = lambda path: types.SimpleNamespace(search=lambda s,q: [], find_all_editorial=lambda s: [])
    st = types.ModuleType('settings')
    st.Settings = lambda *a, **k: types.SimpleNamespace(keyword_path='kw.json')
    monkeypatch.setitem(sys.modules, 'transcribe_worker', tw)
    monkeypatch.setitem(sys.modules, 'diarizer', dr)
    monkeypatch.setitem(sys.modules, 'keyword_index', kw)
    monkeypatch.setitem(sys.modules, 'settings', st)

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
    kw = types.ModuleType('keyword_index')
    kw.KeywordIndex = lambda path: types.SimpleNamespace(search=lambda s,q: [], find_all_editorial=lambda s: [])
    st = types.ModuleType('settings')
    st.Settings = lambda *a, **k: types.SimpleNamespace(keyword_path='kw.json')
    monkeypatch.setitem(sys.modules, "transcribe_worker", tw)
    monkeypatch.setitem(sys.modules, "diarizer", dr)
    monkeypatch.setitem(sys.modules, 'keyword_index', kw)
    monkeypatch.setitem(sys.modules, 'settings', st)

    mw_module = importlib.import_module("main_window")
    mw_module = importlib.reload(mw_module)

    window = mw_module.MainWindow()
    window.add_file("a.wav")
    window.start_processing()

    assert "[Spk1] hi" in window.transcript.toPlainText()


def test_processing_respects_order(monkeypatch):
    stubs = make_pyside6_stub()
    for name, module in stubs.items():
        monkeypatch.setitem(sys.modules, name, module)

    class FakeTranscribeWorker:
        def __init__(self, *a, **k):
            pass

        def transcribe(self, path):
            return [{"start": 0.0, "end": 1.0, "speaker": "", "text": path}]

    class FakeDiarizer:
        def __init__(self, *a, **k):
            pass

        def assign_speakers(self, audio_path, segments):
            return segments

    order = []
    class FakeAggregator:
        def add_segments(self, path, segs):
            order.append(path)
        def get_transcript(self):
            return []

    tw = types.ModuleType("transcribe_worker"); tw.TranscribeWorker = FakeTranscribeWorker
    dr = types.ModuleType("diarizer"); dr.Diarizer = FakeDiarizer
    ta = types.ModuleType('transcript_aggregator'); ta.TranscriptAggregator = lambda: FakeAggregator()
    kw = types.ModuleType('keyword_index'); kw.KeywordIndex = lambda path: types.SimpleNamespace(search=lambda s,q: [], find_all_editorial=lambda s: [])
    st = types.ModuleType('settings'); st.Settings = lambda *a, **k: types.SimpleNamespace(keyword_path='kw.json')
    ce = types.ModuleType('clip_exporter'); ce.ClipExporter = lambda: types.SimpleNamespace()
    monkeypatch.setitem(sys.modules, 'transcribe_worker', tw)
    monkeypatch.setitem(sys.modules, 'diarizer', dr)
    monkeypatch.setitem(sys.modules, 'transcript_aggregator', ta)
    monkeypatch.setitem(sys.modules, 'keyword_index', kw)
    monkeypatch.setitem(sys.modules, 'settings', st)
    monkeypatch.setitem(sys.modules, 'clip_exporter', ce)

    m = importlib.import_module('main_window'); m = importlib.reload(m)
    window = m.MainWindow()
    window.add_file('a.wav')
    window.add_file('b.wav')
    # reorder: move second item to top
    item = window.file_list.takeItem(1)
    window.file_list.insertItem(0, item)
    window.start_processing()

    assert order == ['b.wav', 'a.wav']


def test_search_displays_results(monkeypatch):
    stubs = make_pyside6_stub()
    for name, module in stubs.items():
        monkeypatch.setitem(sys.modules, name, module)

    class FakeKeywordIndex:
        def __init__(self, path):
            self.calls = []

        def search(self, segs, query):
            self.calls.append(query)
            return segs[:1]

        def find_all_editorial(self, segs):
            return []

    kw = types.ModuleType('keyword_index')
    kw.KeywordIndex = FakeKeywordIndex
    st_mod = types.ModuleType('settings')
    st_mod.Settings = lambda *a, **k: types.SimpleNamespace(keyword_path='kw.json')
    tw = types.ModuleType('transcribe_worker'); tw.TranscribeWorker = lambda *a, **k: None
    dr = types.ModuleType('diarizer'); dr.Diarizer = lambda *a, **k: None
    monkeypatch.setitem(sys.modules, 'keyword_index', kw)
    monkeypatch.setitem(sys.modules, 'settings', st_mod)
    monkeypatch.setitem(sys.modules, 'transcribe_worker', tw)
    monkeypatch.setitem(sys.modules, 'diarizer', dr)

    mw_module = importlib.import_module('main_window')
    mw_module = importlib.reload(mw_module)

    window = mw_module.MainWindow()
    segs = [{"speaker": "S1", "text": "hello world"}, {"speaker": "S1", "text": "bye"}]
    window.aggregator.add_segments('a.wav', segs)
    window.search_bar.setText('world')
    window._on_search()

    assert 'hello world' in window.results.toPlainText()
    assert window.keyword_index.calls == ['world']


def test_find_editorials_displays_results(monkeypatch):
    stubs = make_pyside6_stub()
    for name, module in stubs.items():
        monkeypatch.setitem(sys.modules, name, module)

    class FakeKeywordIndex:
        def __init__(self, path):
            self.called = False

        def search(self, segs, query):
            return []

        def find_all_editorial(self, segs):
            self.called = True
            return segs[:1]

    kw = types.ModuleType('keyword_index')
    kw.KeywordIndex = FakeKeywordIndex
    st_mod = types.ModuleType('settings')
    st_mod.Settings = lambda *a, **k: types.SimpleNamespace(keyword_path='kw.json')
    tw = types.ModuleType('transcribe_worker'); tw.TranscribeWorker = lambda *a, **k: None
    dr = types.ModuleType('diarizer'); dr.Diarizer = lambda *a, **k: None
    monkeypatch.setitem(sys.modules, 'keyword_index', kw)
    monkeypatch.setitem(sys.modules, 'settings', st_mod)
    monkeypatch.setitem(sys.modules, 'transcribe_worker', tw)
    monkeypatch.setitem(sys.modules, 'diarizer', dr)

    mw_module = importlib.import_module('main_window')
    mw_module = importlib.reload(mw_module)

    window = mw_module.MainWindow()
    segs = [{"speaker": "S1", "text": "ad spot"}, {"speaker": "S1", "text": "talk"}]
    window.aggregator.add_segments('a.wav', segs)
    window._on_find_editorials()

    assert 'ad spot' in window.results.toPlainText()
    assert window.keyword_index.called is True


def test_export_full_transcript_invokes_exporters(monkeypatch):
    stubs = make_pyside6_stub()
    for name, module in stubs.items():
        monkeypatch.setitem(sys.modules, name, module)

    te = types.ModuleType('transcript_exporter')
    called = {}
    def fake_txt(segs):
        called['txt'] = segs
        return 't'
    def fake_json(segs):
        called['json'] = segs
        return 'j'
    def fake_srt(segs):
        called['srt'] = segs
        return 's'
    te.export_txt = fake_txt
    te.export_json = fake_json
    te.export_srt = fake_srt

    ce = types.ModuleType('clip_exporter'); ce.ClipExporter = lambda: types.SimpleNamespace(export_clip=lambda *a, **k: None)
    kw = types.ModuleType('keyword_index'); kw.KeywordIndex = lambda path: types.SimpleNamespace(search=lambda s,q: [], find_all_editorial=lambda s: [])
    st_mod = types.ModuleType('settings'); st_mod.Settings = lambda *a, **k: types.SimpleNamespace(keyword_path='kw.json')
    tw = types.ModuleType('transcribe_worker'); tw.TranscribeWorker = lambda *a, **k: None
    dr = types.ModuleType('diarizer'); dr.Diarizer = lambda *a, **k: None
    monkeypatch.setitem(sys.modules, 'transcript_exporter', te)
    monkeypatch.setitem(sys.modules, 'clip_exporter', ce)
    monkeypatch.setitem(sys.modules, 'keyword_index', kw)
    monkeypatch.setitem(sys.modules, 'settings', st_mod)
    monkeypatch.setitem(sys.modules, 'transcribe_worker', tw)
    monkeypatch.setitem(sys.modules, 'diarizer', dr)

    monkeypatch.setattr(stubs['PySide6.QtWidgets'].QFileDialog, 'getSaveFileName', staticmethod(lambda *a, **k: ('out.txt', '')))
    m = importlib.import_module('main_window'); m = importlib.reload(m)
    window = m.MainWindow()
    segs = [{'speaker':'S1','text':'hi'}]
    window.aggregator.add_segments('a.wav', segs)
    expected = window.aggregator.get_transcript()

    mo = importlib.import_module('builtins')
    from unittest.mock import mock_open
    monkeypatch.setattr(mo, 'open', mock_open())

    window._on_export_txt()
    window._on_export_json()
    window._on_export_srt()

    assert called['txt'] == expected
    assert called['json'] == expected
    assert called['srt'] == expected


def test_export_segment_invokes_clip(monkeypatch):
    stubs = make_pyside6_stub()
    for name, module in stubs.items():
        monkeypatch.setitem(sys.modules, name, module)

    txt_called = {}
    te = types.ModuleType('transcript_exporter')
    def fake_txt(segs):
        txt_called['segs'] = segs
        return 't'
    te.export_txt = fake_txt
    te.export_json = lambda segs: ''
    te.export_srt = lambda segs: ''

    clip_calls = {}
    class FakeClip:
        def export_clip(self, audio_path, start, end, dest):
            clip_calls['args'] = (audio_path, start, end, dest)

    ce = types.ModuleType('clip_exporter'); ce.ClipExporter = lambda: FakeClip()
    kw = types.ModuleType('keyword_index'); kw.KeywordIndex = lambda path: types.SimpleNamespace(search=lambda s,q: [], find_all_editorial=lambda s: [])
    st_mod = types.ModuleType('settings'); st_mod.Settings = lambda *a, **k: types.SimpleNamespace(keyword_path='kw.json')
    tw = types.ModuleType('transcribe_worker'); tw.TranscribeWorker = lambda *a, **k: None
    dr = types.ModuleType('diarizer'); dr.Diarizer = lambda *a, **k: None
    monkeypatch.setitem(sys.modules, 'transcript_exporter', te)
    monkeypatch.setitem(sys.modules, 'clip_exporter', ce)
    monkeypatch.setitem(sys.modules, 'keyword_index', kw)
    monkeypatch.setitem(sys.modules, 'settings', st_mod)
    monkeypatch.setitem(sys.modules, 'transcribe_worker', tw)
    monkeypatch.setitem(sys.modules, 'diarizer', dr)

    monkeypatch.setattr(stubs['PySide6.QtWidgets'].QFileDialog, 'getSaveFileName', staticmethod(lambda *a, **k: ('seg.txt', '')))
    m = importlib.import_module('main_window'); m = importlib.reload(m)
    window = m.MainWindow()
    segs = [{'speaker':'S1','text':'hi','start':0.0,'end':1.0,'file':'a.wav'}]
    window.aggregator.add_segments('a.wav', segs)
    window.display_segments(segs)
    window.transcript.set_selected_line(0)

    mo = importlib.import_module('builtins')
    from unittest.mock import mock_open
    monkeypatch.setattr(mo, 'open', mock_open())

    window._on_export_segment()

    assert txt_called['segs'] == [segs[0]]
    assert clip_calls['args'] == ('a.wav', 0.0, 1.0, 'seg.wav')


def test_rename_speakers_updates_export(monkeypatch):
    stubs = make_pyside6_stub()
    for name, module in stubs.items():
        monkeypatch.setitem(sys.modules, name, module)

    class FakeDialog:
        calls = [("Host", True), ("Guest", True)]
        index = 0

        @staticmethod
        def getText(*a, **k):
            res = FakeDialog.calls[FakeDialog.index]
            FakeDialog.index += 1
            return res

    stubs['PySide6.QtWidgets'].QInputDialog = FakeDialog

    exported = {}
    te = types.ModuleType('transcript_exporter')
    te.export_txt = lambda segs: ''
    def fake_json(segs):
        exported['data'] = segs
        return 'j'
    te.export_json = fake_json
    te.export_srt = lambda segs: ''

    ce = types.ModuleType('clip_exporter'); ce.ClipExporter = lambda: types.SimpleNamespace()
    kw = types.ModuleType('keyword_index'); kw.KeywordIndex = lambda path: types.SimpleNamespace(search=lambda s,q: [], find_all_editorial=lambda s: [])
    st_mod = types.ModuleType('settings'); st_mod.Settings = lambda *a, **k: types.SimpleNamespace(keyword_path='kw.json')
    tw = types.ModuleType('transcribe_worker'); tw.TranscribeWorker = lambda *a, **k: None
    dr = types.ModuleType('diarizer'); dr.Diarizer = lambda *a, **k: None
    monkeypatch.setitem(sys.modules, 'transcript_exporter', te)
    monkeypatch.setitem(sys.modules, 'clip_exporter', ce)
    monkeypatch.setitem(sys.modules, 'keyword_index', kw)
    monkeypatch.setitem(sys.modules, 'settings', st_mod)
    monkeypatch.setitem(sys.modules, 'transcribe_worker', tw)
    monkeypatch.setitem(sys.modules, 'diarizer', dr)

    monkeypatch.setattr(stubs['PySide6.QtWidgets'].QFileDialog, 'getSaveFileName', staticmethod(lambda *a, **k: ('out.json', '')))

    m = importlib.import_module('main_window'); m = importlib.reload(m)
    window = m.MainWindow()
    segs = [
        {'speaker': 'Spk1', 'text': 'hello', 'start': 0.0, 'end': 1.0, 'file': 'a.wav'},
        {'speaker': 'Spk2', 'text': 'bye', 'start': 1.0, 'end': 2.0, 'file': 'a.wav'},
    ]
    window.aggregator.add_segments('a.wav', segs)
    window.display_segments(segs)

    window._on_rename_speakers()
    window._on_export_json()

    assert exported['data'][0]['speaker'] == 'Host'
    assert exported['data'][1]['speaker'] == 'Guest'
