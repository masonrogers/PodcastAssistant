import argparse
from pathlib import Path

from transcribe_worker import TranscribeWorker
from diarizer import Diarizer
from transcript_aggregator import TranscriptAggregator
from keyword_index import KeywordIndex
from settings import Settings


def main():
    parser = argparse.ArgumentParser(description="Whisper Transcriber (stub)")
    parser.add_argument('files', nargs='+', help='Audio files to transcribe')
    parser.add_argument('--keyword', help='Keyword to search after transcription')
    args = parser.parse_args()

    settings = Settings()
    settings.load()
    kw_index = KeywordIndex(settings.keyword_path)

    worker = TranscribeWorker()
    diarizer = Diarizer()
    agg = TranscriptAggregator()

    for f in args.files:
        text = worker.transcribe(f)
        text = diarizer.tag_speakers(text)
        agg.add(f, text)
        print(f"Processed {f}")

    transcript = agg.merged_text()
    print("\nFull Transcript:\n", transcript)

    if args.keyword:
        kw_index.add(args.keyword)
        matches = kw_index.search(transcript)
        print(f"\nKeyword matches: {matches}")


if __name__ == '__main__':
    main()
