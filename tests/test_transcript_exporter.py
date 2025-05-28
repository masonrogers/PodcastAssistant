import os
import sys
import json
import importlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_exporter_outputs_formats():
    mod = importlib.import_module('transcript_exporter')
    mod = importlib.reload(mod)
    segments = [
        {'start': 0.0, 'end': 1.0, 'speaker': 'A', 'text': 'Hello'},
        {'start': 1.0, 'end': 2.5, 'speaker': 'B', 'text': 'World'},
    ]

    assert mod.export_txt(segments) == 'Hello\nWorld'
    assert mod.export_json(segments) == json.dumps(segments, indent=2, ensure_ascii=False)

    expected_srt = (
        '1\n'
        '00:00:00,000 --> 00:00:01,000\n'
        'Hello\n\n'
        '2\n'
        '00:00:01,000 --> 00:00:02,500\n'
        'World'
    )
    assert mod.export_srt(segments) == expected_srt


def test_format_timestamp_rounding():
    mod = importlib.import_module('transcript_exporter')
    mod = importlib.reload(mod)

    assert mod._format_timestamp(0.9995) == '00:00:01,000'
