import os
import sys
import types
import importlib
from unittest.mock import MagicMock

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_transcribe_worker_returns_structured_segments(monkeypatch):
    fake_model = MagicMock()
    fake_model.transcribe.return_value = {
        "segments": [
            {"start": 0.0, "end": 1.0, "text": "Hello"},
            {"start": 1.0, "end": 2.0, "text": "World"},
        ]
    }
    fake_whisper = types.ModuleType('whisper')
    fake_whisper.load_model = MagicMock(return_value=fake_model)
    monkeypatch.setitem(sys.modules, 'whisper', fake_whisper)

    transcribe_worker = importlib.import_module('transcribe_worker')
    worker = transcribe_worker.TranscribeWorker()
    segments = worker.transcribe('dummy.wav')

    expected = [
        {"start": 0.0, "end": 1.0, "speaker": "Speaker 1", "text": "Hello"},
        {"start": 1.0, "end": 2.0, "speaker": "Speaker 1", "text": "World"},
    ]
    assert segments == expected
    fake_whisper.load_model.assert_called_once_with('base')
    fake_model.transcribe.assert_called_once_with('dummy.wav')
