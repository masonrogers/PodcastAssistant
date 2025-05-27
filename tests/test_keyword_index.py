from keyword_index import KeywordIndex
from pathlib import Path
from transcribe_worker import TranscriptSegment


def test_keyword_add_and_search(tmp_path):
    path = tmp_path / 'keywords.json'
    kw = KeywordIndex(path)
    kw.add('test')
    result = kw.search('this is a test transcript')
    assert 'test' in result

    kw2 = KeywordIndex(path)
    assert kw2.search('another test transcript') == ['test']

    segments = [TranscriptSegment(0, 1, 'S1', 'this is a test')]
    hits = kw.search_segments(segments)
    assert 'test' in hits and hits['test'][0].text == 'this is a test'
