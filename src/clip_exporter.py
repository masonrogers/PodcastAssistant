from pathlib import Path
import subprocess


def export_clip(input_file: Path, start: float, end: float, output_file: Path):
    """Export an audio clip using FFmpeg if available."""
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_file),
        "-ss",
        str(start),
        "-to",
        str(end),
        "-c",
        "copy",
        str(output_file),
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception:
        # Fallback: copy entire file
        output_file.write_bytes(input_file.read_bytes())
