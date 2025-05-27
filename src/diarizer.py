from typing import List

from transcribe_worker import TranscriptSegment


class Diarizer:
    """Assigns speaker labels to transcript segments."""

    def __init__(self):
        try:
            from pyannote.audio import Pipeline  # type: ignore

            self._pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization")
        except Exception:
            self._pipeline = None

    def tag_speakers(self, file_path: str, segments: List[TranscriptSegment]) -> List[TranscriptSegment]:
        if self._pipeline:
            try:
                diarization = self._pipeline(file_path)
                for turn, _, speaker in diarization.itertracks(yield_label=True):
                    for seg in segments:
                        if turn.start <= seg.start < turn.end:
                            seg.speaker = speaker
            except Exception:
                pass
            return segments

        # Fallback assigns speakers round-robin
        speakers = ["Speaker 1", "Speaker 2"]
        for i, seg in enumerate(segments):
            seg.speaker = speakers[i % len(speakers)]
        return segments
