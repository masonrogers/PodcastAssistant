# Whisper Transcriber — Simplified Plan (no timelines)

## 1 — Core Functionality

- On startup, the bootstrapper first ensures PySide6 is installed so the Qt
  progress window can launch. The window then installs any remaining
  dependencies with a progress bar before starting the main application.
- Accept multiple audio files (browse or drag-drop). The file list supports
  drag-and-drop reordering and files are processed in that sequence.
- Perform local Whisper sentence-level transcription with timestamps and Speaker 1/2/3 tags (users can rename later).
- Display live transcript plus a per-file progress bar during processing.
- After all files finish, enable keyword search and a “Find all editorials” button using a persistent keyword list.
- Export options:
  - Full transcript → TXT, JSON, SRT
- Highlighted segment → same text formats plus clipped audio (FFmpeg).
- Entirely offline / internal use; no data leaves the machine.
- Uninstallation cleans up any dependencies installed by the bootstrapper.

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
| `TranscriptExporter`  | Exports transcript segments to TXT, JSON, and SRT |
| `Settings`            | Persists UI prefs & keyword path                       |
| `Bootstrapper`        | Installs PySide6 if needed and then shows a progress dialog while installing the rest |
| `Installer`           | NSIS script for final .exe                             |
| `uninstaller.py`      | Removes packages during uninstall |
The `ClipExporter` in `src/clip_exporter.py` wraps ffmpeg-python and provides
`export_clip(audio_path, start, end, dest_path)` for saving short audio clips.

### Locating Transcription and Diarization

Timestamped transcription segments are generated in `src/transcribe_worker.py` using the Whisper library. Speaker labeling is performed in `src/diarizer.py` with `pyannote.audio`. The diarization model loads only when speaker tags are first needed. See the unit tests in `tests/` for basic usage.
The `TranscriptAggregator` in `src/transcript_aggregator.py` can merge these segment lists into a single timeline.

## Using the Keyword Search

Below the file list is a search bar with **Search** and **Find Editorials** buttons.
Enter text in the bar and click **Search** to show transcript segments containing
that phrase. **Find Editorials** lists segments matching any keywords loaded from
`keywords.json`. Results appear in a pane beneath the transcript.

## Exporting Transcripts

Below the search bar is a row of **Export** buttons.

- **Export TXT**, **Export JSON** and **Export SRT** save the entire transcript
  in the chosen format. After clicking, select the destination path in the file
  dialog.
- To export a single segment, highlight its line in the transcript and click
  **Export Segment**. The text is written to the selected ``.txt`` file and a

## Renaming Speakers

Click **Rename Speakers** to change the automatically detected speaker labels.
Each name is shown in a prompt where you can enter a new label. The transcript
pane and any exports will reflect the updated names.

## Configuration

Use the **Settings** button to adjust application options. The dialog lets you
choose a new path for `keywords.json` and edit UI preferences such as the
`theme` setting. An example file is provided at `docs/keywords.json`. Load this
file or edit it to include your own terms by browsing to its location in the
Settings dialog. Changes are saved to
`%APPDATA%\WhisperTranscriber\settings.json` and take effect the next time the
application is launched.

## 4 — If an AI Agent Will Write the Code

- Supply acceptance tests (pytest) that cover every feature above.
- Include a Prompt Pack (system + task prompts) and a self-review checklist in the repo.
- Continuous Integration: agent generates code → tests run → human reviews & merges.

## 5 — Deliverables

- Signed Windows installer (.exe)
- Source repository with tests, prompts, and README
- [User Guide](docs/user_guide.pdf) with installation and usage instructions

That’s the entire plan—feature set, tech choices, modules, and deliverables—without any timelines.

## Building the Installer

### Prerequisites

- Python with all packages from `requirements.txt`
- `pyinstaller` available on your PATH (`pip install pyinstaller`)
- (Optional) [NSIS](https://nsis.sourceforge.io/) for creating the final
  Windows installer.

### Invocation

Run the helper script which invokes PyInstaller:

```bash
python build_installer.py
```

The resulting executable will be placed in the `dist/` directory. The
`installer/whisper_transcriber.nsi` script can then be adapted to wrap this
binary in an NSIS installer.

## Contributor Resources

The `prompts/` directory contains text prompts used by the automation
agents:

- `prompts/system_prompt.txt`
- `prompts/developer_prompt.txt`
- `prompts/contributor_tasks.txt`

Guidelines for verifying changes before submission are provided in
[`self_review_checklist.md`](self_review_checklist.md).

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

