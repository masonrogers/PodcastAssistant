# Changelog

All notable changes to this project will be documented in this file.
Whenever a feature is added or removed, update the "Unreleased" section with a detailed entry and move it to the appropriate release heading when the version is published.

## [Unreleased]
### Added
- `ensure_ffmpeg()` installs `static-ffmpeg` automatically when FFmpeg is not present, bundling a static binary for packaging.
- `ensure_ffmpeg()` installs `ffmpeg-python` automatically when the Python wrapper is missing.
- `pip_install()` and `pip_uninstall()` helper functions manage package installation and removal.
- `setup_logging()` in `src/logging_setup.py` configures rotating file logs under `logs/` and provides `get_logger()`.
- Added `get_logger` usage across modules with informative log messages.
- `run_app.py` and `build_installer.py` now call `setup_logging()` before other imports so early logging works.
- Log files are generated per module in `logs/`, such as `app.log` for the main application and `installer_build.log` for the installer builder.
- Added a `logs/` directory with a `.gitkeep` file so the log folder is tracked in version control.
- `.gitignore` now excludes log files under `logs/*.log`.
- `.gitignore` now excludes PyInstaller-generated `*.spec` files.
- PyInstaller build now loads `pyinstaller_hooks/hook-whispercpp.py` via
  `--additional-hooks-dir` so WhisperCPP's dynamic libraries bundle correctly.
- Documented Python version requirements in README and user guide; note that newer versions may lack `whispercpp` wheels.
- `requirements.txt` now lists `torch` and `torchaudio`. README and the user guide instruct users to install these packages when running from source.

### Changed
 - Replaced `docs/user_guide.pdf` with a plain-text version. The generator
   script now writes `docs/user_guide.txt` instead of a PDF and the PDF file was
   removed from the repository.
 - `build_installer.py` now passes `--paths src` to `PyInstaller.__main__.run`
   so bundled executables can import the `bootstrapper` module without errors.
- `bootstrapper` and `uninstaller` now invoke pip via subprocess for better
  compatibility with the packaged application.
- Bundled PyInstaller executable now includes pip's CA bundle so pip can
  locate its certificates at runtime.
- Removed `--hidden-import` options for pip's internal commands and
  `pip._vendor.distlib` from the build script.
- `build_installer.py` now invokes `setup_logging()` in `main()` and logs the
  certificate path, output directory and completion status of the PyInstaller
  run.
- `build_installer.py` now prepends the repository's `src` directory to `sys.path` so `src.logging_setup` imports reliably.
    - README logging documentation now clarifies that all modules write to
      `logs/app.log` except `build_installer.py`, which uses
      `logs/installer_build.log`. It also notes that log files rotate and reside in
      the `logs/` directory.
- `pip_install()` now raises an exception when pip exits with a non-zero code and
  `Bootstrapper.run()` aborts installation, logging the error and showing a
  message box when running under Qt.
- `run_app.py` now imports `MainWindow` only after the bootstrapper finishes
   installing packages. This prevents `ModuleNotFoundError` for modules like
  `whispercpp` when launching the packaged executable.
- `Bootstrapper.__init__` now checks `sys.frozen` and reads `requirements.txt`
  from the executable's directory when running as a PyInstaller bundle.
- `Bootstrapper._missing_packages` now imports each module with
  `importlib.import_module` and marks packages missing when an `ImportError`
  occurs. Tests patch `importlib.import_module` accordingly.
- `build_installer.py` now passes `--collect-all=whispercpp` and
  `--hidden-import=whispercpp` to PyInstaller so the packaged executable
  includes WhisperCPP resources.
- `build_installer.py` now passes `--collect-binaries=whispercpp` so the
  transcription engine's binary library is bundled.
- Dependencies are bundled within the executable during the build process.
  `build_installer.py` no longer copies `requirements.txt` or `src/uninstaller.py`
  into the PyInstaller bundle.
- `run_app.py` launches `MainWindow` directly. Startup no longer displays a
  progress dialog or reads `requirements.txt`.
- Uninstaller now removes only application files and is launched via Add/Remove
  Programs.
- Updated README and user guide to remove bootstrapper instructions.
  The bootstrapping section now explains that the packaged executable
  contains all dependencies and uninstallation uses Add/Remove Programs.

### Removed
- **BREAKING**: `src.__init__` no longer imports `TranscriptAggregator`,
  `KeywordIndex`, `ClipExporter`, `transcript_exporter`, `Settings`, or
  `MainWindow` eagerly. Import these objects from their specific modules instead
  of `src`.
- Removed runtime bootstrapper.
- Test suite updated to reflect the simplified startup and uninstall behavior.
  Removed `tests/test_bootstrapper.py` now that installation occurs at build
  time and updated `tests/test_run_app.py` and `tests/test_uninstaller.py`.

## [0.1.0] – YYYY-MM-DD
### Added
- Initial changelog with sections for future releases.
- NSIS script now copies `dist/WhisperTranscriber.exe` into the install directory and cleans it up during uninstall.
- Project plan updated to cover automatic dependency bootstrapping with progress dialog.
- Runtime bootstrapper installs dependencies listed in `requirements.txt` at
  startup with a progress dialog before launching the main window.
- Uninstaller removes packages installed by the bootstrapper during uninstall.
- Main window loads keywords from the path in `Settings` and provides a search
  bar plus a **Find Editorials** button to display matching transcript segments.
- Export buttons allow saving the full transcript as TXT, JSON or SRT. A
  highlighted segment can be saved along with a clipped audio file.
- File list now allows drag-and-drop reordering, and processing respects the
    arranged sequence.
- Rename Speakers dialog allows updating speaker labels and exports reflect the
    new names.
- Concise PDF user guide covers installation, usage, exporting, keyword
  management and uninstallation.
- Settings dialog allows changing the keyword list path and UI preferences with
    saved values reloaded on restart.
- Tests now verify that `ensure_pyside6()` installs PySide6 only when it's
  missing.
- Example `keywords.json` added in `docs/` and README updated with instructions
  for loading or editing it via the Settings dialog.

### Changed
- Bootstrapper now installs PySide6 first so the progress window can launch
  before installing remaining dependencies.
- Uninstaller now invokes the bundled Python interpreter via
  `WhisperTranscriber.exe uninstaller.py` instead of calling `$INSTDIR\python.exe`.


## [0.1.0] - 2025-05-28
### Added
- Created `prompts/` directory at the repository root.
- Added `prompts/system_prompt.txt` defining the system prompt.
- Added `prompts/developer_prompt.txt` with developer instructions.
- Added `prompts/contributor_tasks.txt` describing tasks for contributors.
- Introduced `self_review_checklist.md` to outline verification steps.
- README now links to the prompts directory and the checklist.
