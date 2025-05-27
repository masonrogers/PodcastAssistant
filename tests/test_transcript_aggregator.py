import os
import sys
import importlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_transcript_aggregator_merges_and_sorts():
    agg_module = importlib.import_module('transcript_aggregator')
    agg_module = importlib.reload(agg_module)
    aggregator = agg_module.TranscriptAggregator()

    segments_a = [
        {'start': 2.0, 'end': 2.5, 'speaker': 'A', 'text': 'Bye'},
        {'start': 0.0, 'end': 1.0, 'speaker': 'A', 'text': 'Hi'},
    ]
    segments_b = [
        {'start': 1.5, 'end': 2.0, 'speaker': 'B', 'text': 'Mid'},
    ]

    aggregator.add_segments('a.wav', segments_a)
    aggregator.add_segments('b.wav', segments_b)

    transcript = aggregator.get_transcript()

    expected = [
        {'start': 0.0, 'end': 1.0, 'speaker': 'A', 'text': 'Hi', 'file': 'a.wav'},
        {'start': 1.5, 'end': 2.0, 'speaker': 'B', 'text': 'Mid', 'file': 'b.wav'},
        {'start': 2.0, 'end': 2.5, 'speaker': 'A', 'text': 'Bye', 'file': 'a.wav'},
    ]

    assert transcript == expected
