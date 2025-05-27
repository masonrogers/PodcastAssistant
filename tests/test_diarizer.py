from diarizer import Diarizer
from transcribe_worker import TranscriptSegment


def test_diarizer_round_robin():
    d = Diarizer()
    segments = [TranscriptSegment(0, 0.5, '', 'a'), TranscriptSegment(0.5, 1.0, '', 'b')]
    result = d.tag_speakers('file.wav', segments)
    assert result[0].speaker != result[1].speaker
