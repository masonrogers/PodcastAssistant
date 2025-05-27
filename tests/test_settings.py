import os
import sys
import json
import importlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_settings_load_defaults(tmp_path):
    path = tmp_path / 'settings.json'
    settings_mod = importlib.import_module('settings')
    settings_mod = importlib.reload(settings_mod)
    settings = settings_mod.Settings(str(path))

    assert settings.ui == {}
    assert settings.keyword_path == str(tmp_path / 'keywords.json')


def test_settings_save_and_reload(tmp_path):
    path = tmp_path / 'settings.json'
    settings_mod = importlib.import_module('settings')
    settings_mod = importlib.reload(settings_mod)
    settings = settings_mod.Settings(str(path))

    settings.ui['theme'] = 'dark'
    settings.keyword_path = str(tmp_path / 'kw.json')
    settings.save()

    settings2 = settings_mod.Settings(str(path))
    assert settings2.ui == {'theme': 'dark'}
    assert settings2.keyword_path == str(tmp_path / 'kw.json')


def test_settings_keyword_path_property(tmp_path):
    path = tmp_path / 'settings.json'
    settings_mod = importlib.import_module('settings')
    settings_mod = importlib.reload(settings_mod)
    settings = settings_mod.Settings(str(path))

    settings.keyword_path = str(tmp_path / 'new_kw.json')
    settings.save()

    new_settings = settings_mod.Settings(str(path))
    assert new_settings.keyword_path == str(tmp_path / 'new_kw.json')
