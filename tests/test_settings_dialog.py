import os
import sys
import importlib
import types

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from test_main_window import make_pyside6_stub


def test_settings_dialog_updates_and_persists(monkeypatch, tmp_path):
    stubs = make_pyside6_stub()
    for name, module in stubs.items():
        monkeypatch.setitem(sys.modules, name, module)

    settings_mod = importlib.import_module('settings')
    settings_mod = importlib.reload(settings_mod)
    path = tmp_path / 'settings.json'
    settings = settings_mod.Settings(str(path))

    tw = types.ModuleType('transcribe_worker'); tw.TranscribeWorker = lambda *a, **k: None
    dr = types.ModuleType('diarizer'); dr.Diarizer = lambda *a, **k: None
    kw = types.ModuleType('keyword_index'); kw.KeywordIndex = lambda p: types.SimpleNamespace(search=lambda s,q: [], find_all_editorial=lambda s: [])
    ce = types.ModuleType('clip_exporter'); ce.ClipExporter = lambda: types.SimpleNamespace()
    monkeypatch.setitem(sys.modules, 'transcribe_worker', tw)
    monkeypatch.setitem(sys.modules, 'diarizer', dr)
    monkeypatch.setitem(sys.modules, 'keyword_index', kw)
    monkeypatch.setitem(sys.modules, 'clip_exporter', ce)

    mw_module = importlib.import_module('main_window')
    mw_module = importlib.reload(mw_module)

    dialog = mw_module.SettingsDialog(settings)
    dialog.keyword_edit.setText(str(tmp_path / 'kw.json'))
    dialog.theme_edit.setText('dark')
    dialog.accept()

    settings.save()
    loaded = settings_mod.Settings(str(path))
    assert loaded.keyword_path == str(tmp_path / 'kw.json')
    assert loaded.ui['theme'] == 'dark'
