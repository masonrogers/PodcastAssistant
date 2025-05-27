import os
import sys
import types
import importlib
from unittest.mock import MagicMock

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class FakeSegment:
    def __init__(self, start, end):
        self.start = start
        self.end = end

class FakeAnnotation:
    def itertracks(self, yield_label=True):
        return [
            (FakeSegment(0.0, 1.0), None, 'SpeakerA'),
            (FakeSegment(1.0, 2.0), None, 'SpeakerB'),
        ]


def test_diarizer_assigns_speakers(monkeypatch):
    fake_pipeline_instance = MagicMock(return_value=FakeAnnotation())

    fake_pipeline_class = MagicMock()
    fake_pipeline_class.from_pretrained.return_value = fake_pipeline_instance

    fake_pyannote = types.ModuleType('pyannote.audio')
    fake_pyannote.Pipeline = fake_pipeline_class

    monkeypatch.setitem(sys.modules, 'pyannote.audio', fake_pyannote)

    diarizer = importlib.import_module('diarizer')
    worker = diarizer.Diarizer()

    segments = [
        {'start': 0.2, 'end': 0.8, 'speaker': 'Speaker 1', 'text': 'Hi'},
        {'start': 1.2, 'end': 1.8, 'speaker': 'Speaker 1', 'text': 'There'},
    ]
    labeled = worker.assign_speakers('dummy.wav', segments)

    assert labeled[0]['speaker'] == 'SpeakerA'
    assert labeled[1]['speaker'] == 'SpeakerB'
    fake_pipeline_class.from_pretrained.assert_called_once()
    fake_pipeline_instance.assert_called_once_with('dummy.wav')
