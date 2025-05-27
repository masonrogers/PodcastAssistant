from keyword_index import KeywordIndex
from pathlib import Path


def test_keyword_add_and_search(tmp_path):
    path = tmp_path / 'keywords.json'
    kw = KeywordIndex(path)
    kw.add('test')
    result = kw.search('this is a test transcript')
    assert 'test' in result
