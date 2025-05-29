import os
import sys
import importlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_remove_app_files_deletes_contents(tmp_path):
    app_dir = tmp_path / 'app'
    app_dir.mkdir()
    (app_dir / 'file.txt').write_text('data')
    sub = app_dir / 'subdir'
    sub.mkdir()
    (sub / 'nested.txt').write_text('data')

    mod = importlib.import_module('uninstaller')
    mod.remove_app_files(str(app_dir))

    assert list(app_dir.iterdir()) == []

