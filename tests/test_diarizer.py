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


def test_diarizer_lazy_load_and_reuse(monkeypatch):
    fake_pipeline_instance = MagicMock(return_value=FakeAnnotation())

    fake_pipeline_class = MagicMock()
    fake_pipeline_class.from_pretrained.return_value = fake_pipeline_instance

    fake_pyannote = types.ModuleType('pyannote.audio')
    fake_pyannote.Pipeline = fake_pipeline_class

    monkeypatch.setitem(sys.modules, 'pyannote.audio', fake_pyannote)

    diarizer = importlib.import_module('diarizer')
    diarizer = importlib.reload(diarizer)
    worker = diarizer.Diarizer()

    # Pipeline should not be loaded during initialization
    fake_pipeline_class.from_pretrained.assert_not_called()

    segments = [
        {'start': 0.2, 'end': 0.8, 'speaker': 'Speaker 1', 'text': 'Hi'},
        {'start': 1.2, 'end': 1.8, 'speaker': 'Speaker 1', 'text': 'There'},
    ]
    labeled = worker.assign_speakers('dummy.wav', segments)

    assert labeled[0]['speaker'] == 'SpeakerA'
    assert labeled[1]['speaker'] == 'SpeakerB'
    fake_pipeline_class.from_pretrained.assert_called_once()
    fake_pipeline_instance.assert_called_once_with('dummy.wav')

    # Subsequent calls should reuse the same pipeline instance
    worker.assign_speakers('dummy2.wav', segments)
    fake_pipeline_class.from_pretrained.assert_called_once()
    assert fake_pipeline_instance.call_count == 2


class FakeAnnotation2:
    def itertracks(self, yield_label=True):
        return [
            (FakeSegment(0.0, 0.5), None, 'Alpha'),
            (FakeSegment(1.0, 1.5), None, 'Beta'),
        ]


def test_assign_speakers_labels_segments(monkeypatch):
    fake_pipeline_instance = MagicMock(return_value=FakeAnnotation2())

    fake_pipeline_class = MagicMock()
    fake_pipeline_class.from_pretrained.return_value = fake_pipeline_instance

    fake_pyannote = types.ModuleType('pyannote.audio')
    fake_pyannote.Pipeline = fake_pipeline_class

    monkeypatch.setitem(sys.modules, 'pyannote.audio', fake_pyannote)

    diarizer = importlib.import_module('diarizer')
    diarizer = importlib.reload(diarizer)
    worker = diarizer.Diarizer()

    segments = [
        {'start': 0.1, 'end': 0.2, 'speaker': '', 'text': 'a'},
        {'start': 1.2, 'end': 1.3, 'speaker': '', 'text': 'b'},
        {'start': 0.6, 'end': 0.7, 'speaker': '', 'text': 'c'},
    ]
    labeled = worker.assign_speakers('audio.wav', segments)

    assert labeled[0]['speaker'] == 'Alpha'
    assert labeled[1]['speaker'] == 'Beta'
    assert labeled[2]['speaker'] == 'Unknown'
    fake_pipeline_instance.assert_called_once_with('audio.wav')
