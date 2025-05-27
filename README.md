# Whisper Transcriber — Simplified Plan (no timelines)

## 1 — Core Functionality

- Accept multiple audio files (browse or drag-drop) and let the user re-order them.
- Perform local Whisper sentence-level transcription with timestamps and Speaker 1/2/3 tags (users can rename later).
- Display live transcript plus a per-file progress bar during processing.
- After all files finish, enable keyword search and a “Find all editorials” button using a persistent keyword list.
- Export options:
  - Full transcript → TXT, JSON, SRT
  - Highlighted segment → same text formats plus clipped audio (FFmpeg).
- Entirely offline / internal use; no data leaves the machine.

## 2 — Technology Stack

| Layer              | Choice                                           |
| ------------------ | ------------------------------------------------ |
| GUI                | PySide 6 (Qt for Python)                         |
| Speech-to-text     | Whisper.cpp (large model, local)                 |
| Speaker diarization| pyannote.audio                                   |
| Audio clip/export  | FFmpeg (via ffmpeg-python)                       |
| Packaging          | PyInstaller → NSIS signed Windows installer      |
| Data storage       | `%APPDATA%\\WhisperTranscriber\\settings.json` and `keywords.json` |

## 3 — Key Code Modules

| Module                | Responsibility                                         |
| --------------------- | ------------------------------------------------------ |
| `MainWindow`          | Drag-drop file list, progress bars, transcript pane    |
| `TranscribeWorker`    | Runs Whisper streaming + progress updates              |
| `Diarizer`            | Adds speaker tags                                      |
| `TranscriptAggregator`| Merges worker output into ordered transcript           |
| `KeywordIndex`        | Loads/saves keyword list, search, “find all editorial” |
| `ClipExporter`        | Cuts audio for highlighted range via FFmpeg            |
| `Settings`            | Persists UI prefs & keyword path                       |
| `Installer`           | NSIS script for final .exe                             |
The `ClipExporter` in `src/clip_exporter.py` wraps ffmpeg-python and provides
`export_clip(audio_path, start, end, dest_path)` for saving short audio clips.

### Locating Transcription and Diarization

Timestamped transcription segments are generated in `src/transcribe_worker.py` using the Whisper library. Speaker labeling is performed in `src/diarizer.py` with `pyannote.audio`. See the unit tests in `tests/` for basic usage.
The `TranscriptAggregator` in `src/transcript_aggregator.py` can merge these segment lists into a single timeline.

## 4 — If an AI Agent Will Write the Code

- Supply acceptance tests (pytest) that cover every feature above.
- Include a Prompt Pack (system + task prompts) and a self-review checklist in the repo.
- Continuous Integration: agent generates code → tests run → human reviews & merges.

## 5 — Deliverables

- Signed Windows installer (.exe)
- Source repository with tests, prompts, and README
- One-page user guide (PDF)

That’s the entire plan—feature set, tech choices, modules, and deliverables—without any timelines.
