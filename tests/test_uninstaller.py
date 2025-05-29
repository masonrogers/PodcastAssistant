import os
import sys
import importlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_uninstall_packages_invokes_pip(monkeypatch, tmp_path):
    req = tmp_path / 'req.txt'
    req.write_text('pkgA\npkgB==1.2\n# comment\n\npkgC\n')

    runs = []

    def fake_uninstall(pkg):
        runs.append(pkg)

    mod = importlib.import_module('uninstaller')
    mod = importlib.reload(mod)
    monkeypatch.setattr(mod, 'pip_uninstall', fake_uninstall)
    mod.uninstall_packages(str(req))

    expected = ['pkgA', 'pkgB==1.2', 'pkgC']
    assert runs == expected
