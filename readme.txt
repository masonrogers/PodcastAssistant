You are an expert software architect and senior Python engineer. Your task is to produce a **single, unified vision** for a standalone Windows 11–style Python application—no phased milestones or separate planning steps—just a complete specification that can be handed directly to a code-generation AI or engineering team.

---

## Application: Multi-File Whisper Transcriber

**Modes**

* **GUI**: full Windows 11–style interface
* **CLI headless**: batch folder processing

---

### 1. Self-Bootstrapping & Dependencies

* On launch, attempt to import each required module; on failure, run
  `python -m pip install <package>`
  from within the app, and log each install in the status bar.
* **Dependencies:**

  * GUI: PySide6 (or PyQt6) with Fluent/Win11 theming
  * Transcription: OpenAI Whisper Python package
  * Audio: pydub (metadata), noisereduce & rnnoise (noise reduction), wave/simpleaudio (playback)
  * Concurrency: `concurrent.futures.ThreadPoolExecutor`
  * Logging: `logging` + `RotatingFileHandler`
  * Persistence: built-in `json` for session data
  * Packaging: PyInstaller for a single-file EXE

---

### 2. Audio Processing & Playback

* **Noise-reduction toggle** supporting both `noisereduce` and `rnnoise` (default off)
* **Duration extraction** via pydub
* **Waveform viewer** with playback controls (play/pause/seek, speed ×0.5–2×)
* **Trimming controls** (“Set In”/“Set Out” markers) to crop before transcription

---

### 3. Transcription Engine

* **Offline-first** with local Whisper models and automatic multilingual detection
* **Fallback option** to OpenAI’s Whisper API if local inference fails (e.g. GPU OOM)
* **Real-time incremental output** with word- or sentence-level timestamps
* **Speaker diarization** clusters (e.g. “Speaker 1”, “Speaker 2”) that users can rename

---

### 4. Concurrency & Performance

* Use `ThreadPoolExecutor(max_workers=os.cpu_count())`; detect and leverage GPU (CUDA/ROCm) if available
* Dynamically tune worker count based on CPU/GPU load
* **Progress reporting:** each worker calls a thread-safe `report_progress(id, percent, eta)` callback every few seconds

---

### 5. User Interface (PySide6/PyQt6)

* **Main window:** “Multi-File Whisper Transcriber” with Win11 icon and Fluent styling
* **Menu bar**

  * **File:** Add Files (Ctrl+O), Clear All, Switch to CLI Mode, Export Transcript (Ctrl+S), Exit
  * **Settings:** Model size, Language override, Thread count, Noise-reduction toggle, GPU toggle, Theme (Light/Dark/High-Contrast)
  * **Help:** Quickstart guide, About
* **Layout:** two-pane split

  * **Left pane:**

    * Drag-&-drop–reorderable table (`QTableWidget`) with columns: Filename, Duration, Status (Pending/Transcribing/Done/Error), Progress (%) + bar + ETA
    * Waveform preview + trimming controls beneath the table
  * **Right pane:**

    * Scrollable transcript editor (`QTextEdit`) showing incremental, sectioned output:
      \=== filename.ext ===
      \[00:00.00] \[Speaker 1] Hello world…
      \=== filename2.wav ===
      \[00:00.00] \[Speaker 2] Welcome back…
    * Toolbar buttons: Copy (Ctrl+C), Export (Ctrl+S) → TXT, Markdown, SRT, WebVTT, per-file TXT

---

### 6. CLI Mode

Launch via:
`python whisper_transcriber.py --headless --input-folder "<path>" --export-format txt,srt,md,vtt [--noise-reduction {noisereduce,rnnoise}] [--model-size medium] [--fallback-api]`
Processes all files in the folder, writes sectioned output to a combined file or per-file outputs, and updates the same JSON session file.

---

### 7. Session Persistence

Store last session’s file list, custom ordering, noise-reduction setting, model choice, theme, and window geometry in `~/.whisper_transcriber/session.json`.

---

### 8. Error Handling & Logging

* **Logging:** write to `~/.whisper_transcriber/app.log` with rotation (5 MB, 3 backups)
* **UI errors:** show `QMessageBox` for failures; mark individual rows as “Error” and continue processing

---

### 9. Packaging & Testing

* **Requirements:** `requirements.txt` listing exact versions
* **PyInstaller:** spec for a single-file, double-clickable EXE
* **Testing:** `pytest` suite covering the core Transcriber class (mock Whisper calls, progress callbacks)
* **Documentation:** Google-style docstrings for all public modules/classes and a `README.md` with install, run (GUI & CLI), and build steps

---

**Final Deliverable**
A complete codebase (directory tree + all source files), ready to `pip install -r requirements.txt`, launch the GUI or CLI, and fulfill every feature above—no further planning needed.
