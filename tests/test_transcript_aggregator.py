from transcript_aggregator import TranscriptAggregator
from transcribe_worker import TranscriptSegment


def test_merge():
    agg = TranscriptAggregator()
    agg.add('a.wav', [TranscriptSegment(0, 1, 'S1', 'hello')])
    agg.add('b.wav', [TranscriptSegment(1, 2, 'S2', 'world')])
    text = agg.merged_text()
    assert 'hello' in text and 'world' in text
