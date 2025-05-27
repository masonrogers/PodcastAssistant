import importlib.util
import subprocess
import sys

from bootstrap import install_missing_packages


def test_install_progress(monkeypatch, capsys):
    packages = ['a', 'b']
    # simulate both packages missing
    monkeypatch.setattr(importlib.util, 'find_spec', lambda name: None)

    calls = []
    def fake_call(cmd, **kwargs):
        calls.append(cmd)
    monkeypatch.setattr(subprocess, 'check_call', fake_call)

    monkeypatch.setattr('bootstrap.REQUIRED_PACKAGES', packages, raising=False)

    install_missing_packages()
    out = capsys.readouterr().out
    # progress bar indicator should be printed twice
    assert calls == [[sys.executable, '-m', 'pip', 'install', 'a'],
                     [sys.executable, '-m', 'pip', 'install', 'b']]
    assert '[#' in out
    assert 'Installing a (1/2)' in out
    assert 'Installing b (2/2)' in out
