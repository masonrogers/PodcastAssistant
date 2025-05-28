import os
import sys
import importlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_uninstall_packages_invokes_pip(monkeypatch, tmp_path):
    req = tmp_path / 'req.txt'
    req.write_text('pkgA\npkgB==1.2\n# comment\n\npkgC\n')

    runs = []

    def fake_run(args, check=False):
        runs.append(args)

    import subprocess
    monkeypatch.setattr(subprocess, 'run', fake_run)

    mod = importlib.import_module('uninstaller')
    mod = importlib.reload(mod)
    mod.uninstall_packages(str(req))

    expected = [
        [sys.executable, '-m', 'pip', 'uninstall', '-y', 'pkgA'],
        [sys.executable, '-m', 'pip', 'uninstall', '-y', 'pkgB==1.2'],
        [sys.executable, '-m', 'pip', 'uninstall', '-y', 'pkgC'],
    ]
    assert runs == expected
