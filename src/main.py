import argparse
from pathlib import Path

from transcribe_worker import TranscribeWorker
from diarizer import Diarizer
from transcript_aggregator import TranscriptAggregator
from keyword_index import KeywordIndex
from settings import Settings
from clip_exporter import export_clip
from gui import MainWindow


def main():
    parser = argparse.ArgumentParser(description="Whisper Transcriber")
    parser.add_argument('files', nargs='*', help='Audio files to transcribe')
    parser.add_argument('--gui', action='store_true', help='Launch GUI')
    parser.add_argument('--keyword', help='Keyword to search after transcription')
    parser.add_argument('--export', nargs=3, metavar=('FILE', 'START', 'END'),
                        help='Export audio clip with FFmpeg')
    args = parser.parse_args()

    settings = Settings()
    settings.load()
    kw_index = KeywordIndex(settings.keyword_path)

    if args.gui:
        try:
            from PySide6 import QtWidgets  # type: ignore
        except Exception:
            print('PySide6 not installed; GUI unavailable.')
            return
        app = QtWidgets.QApplication([])
        win = MainWindow()
        win.show()
        app.exec()
        return

    worker = TranscribeWorker()
    diarizer = Diarizer()
    agg = TranscriptAggregator()

    for f in args.files:
        segments = worker.transcribe(f)
        segments = diarizer.tag_speakers(f, segments)
        agg.add(f, segments)
        print(f"Processed {f}")

    transcript = agg.merged_text()
    print("\nFull Transcript:\n", transcript)

    if args.keyword:
        kw_index.add(args.keyword)
        matches = kw_index.search(transcript)
        print(f"\nKeyword matches: {matches}")

    if args.export:
        file_path, start, end = args.export
        export_clip(Path(file_path), float(start), float(end), Path('clip_' + Path(file_path).name))


if __name__ == '__main__':
    main()
