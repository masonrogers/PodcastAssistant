import os
import sys
import json
import importlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_keyword_index_persistence(tmp_path):
    path = tmp_path / 'keywords.json'
    ki_module = importlib.import_module('keyword_index')
    ki_module = importlib.reload(ki_module)
    index = ki_module.KeywordIndex(str(path))

    assert index.keywords == []

    index.add_keyword('ad')
    index.add_keyword('sponsor')

    with open(path, 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    assert data == ['ad', 'sponsor']

    index2 = ki_module.KeywordIndex(str(path))
    assert index2.keywords == ['ad', 'sponsor']


def test_keyword_index_search(tmp_path):
    path = tmp_path / 'keywords.json'
    ki_module = importlib.import_module('keyword_index')
    ki_module = importlib.reload(ki_module)
    index = ki_module.KeywordIndex(str(path))

    segments = [
        {'text': 'Hello World'},
        {'text': 'Other text'},
        {'text': 'WORLD domination'},
    ]

    results = index.search(segments, 'world')
    assert results == [segments[0], segments[2]]


def test_keyword_index_find_all_editorial(tmp_path):
    path = tmp_path / 'keywords.json'
    ki_module = importlib.import_module('keyword_index')
    ki_module = importlib.reload(ki_module)
    index = ki_module.KeywordIndex(str(path))

    index.add_keyword('ad')
    index.add_keyword('sponsor')

    segments = [
        {'text': 'This is an ad spot'},
        {'text': 'Just regular discussion'},
        {'text': 'Our Sponsor thanks you'},
    ]

    results = index.find_all_editorial(segments)
    assert results == [segments[0], segments[2]]
