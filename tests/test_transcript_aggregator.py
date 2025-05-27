from transcript_aggregator import TranscriptAggregator


def test_merge():
    agg = TranscriptAggregator()
    agg.add('a.wav', 'hello')
    agg.add('b.wav', 'world')
    assert agg.merged_text() == 'hello\nworld'
