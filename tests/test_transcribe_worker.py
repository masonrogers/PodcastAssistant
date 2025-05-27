from transcribe_worker import TranscribeWorker


def test_transcribe_stub():
    worker = TranscribeWorker()
    result = worker.transcribe('audio.wav')
    assert 'audio.wav' in result
