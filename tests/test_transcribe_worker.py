from transcribe_worker import TranscribeWorker, TranscriptSegment


def test_transcribe_stub(tmp_path):
    worker = TranscribeWorker()
    audio = tmp_path / 'audio.wav'
    audio.write_text('data')
    segments = worker.transcribe(str(audio))
    assert isinstance(segments, list)
    assert isinstance(segments[0], TranscriptSegment)
    assert 'audio.wav' in segments[0].text
