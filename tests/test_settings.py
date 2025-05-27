from settings import Settings


def test_settings_load_save(tmp_path, monkeypatch):
    monkeypatch.setenv('APPDATA', str(tmp_path))
    s = Settings()
    s.keyword_path = tmp_path / 'kw.json'
    s.save()
    s.keyword_path = None
    s.load()
    assert s.keyword_path == tmp_path / 'kw.json'
