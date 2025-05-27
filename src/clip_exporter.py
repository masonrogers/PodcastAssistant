import ffmpeg

class ClipExporter:
    """Export a clipped portion of an audio file using ffmpeg-python."""

    def export_clip(self, audio_path: str, start: float, end: float, dest_path: str) -> str:
        """Clip audio between ``start`` and ``end`` seconds and save to ``dest_path``."""
        stream = ffmpeg.input(audio_path, ss=start, to=end)
        stream = stream.output(dest_path)
        stream = stream.overwrite_output()
        stream.run()
        return dest_path
