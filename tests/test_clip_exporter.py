from clip_exporter import export_clip
from pathlib import Path


def test_export_clip(tmp_path):
    inp = tmp_path / 'in.wav'
    out = tmp_path / 'out.wav'
    inp.write_bytes(b'data')
    export_clip(inp, 0, 1, out)
    assert out.exists()
    assert out.read_bytes() == inp.read_bytes()
