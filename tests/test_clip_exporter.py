import os
import sys
import types
import importlib
from unittest.mock import MagicMock

# add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_export_clip_invokes_ffmpeg(monkeypatch):
    fake_stream = MagicMock()
    fake_output_stream = MagicMock()
    fake_output_stream.overwrite_output.return_value = fake_output_stream
    fake_output_stream.run.return_value = None
    fake_stream.output.return_value = fake_output_stream

    fake_ffmpeg = types.ModuleType('ffmpeg')
    fake_ffmpeg.input = MagicMock(return_value=fake_stream)
    monkeypatch.setitem(sys.modules, 'ffmpeg', fake_ffmpeg)

    clip_mod = importlib.import_module('clip_exporter')
    clip_mod = importlib.reload(clip_mod)
    exporter = clip_mod.ClipExporter()

    result = exporter.export_clip('in.wav', 0.5, 2.5, 'out.wav')

    fake_ffmpeg.input.assert_called_once_with('in.wav', ss=0.5, to=2.5)
    fake_stream.output.assert_called_once_with('out.wav')
    fake_output_stream.overwrite_output.assert_called_once()
    fake_output_stream.run.assert_called_once()
    assert result == 'out.wav'
