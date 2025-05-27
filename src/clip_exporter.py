from pathlib import Path


def export_clip(input_file: Path, start: float, end: float, output_file: Path):
    # Stub that just copies the input file
    output_file.write_bytes(input_file.read_bytes())
