# Changelog

All notable changes to this project will be documented in this file.
Whenever a feature is added or removed, update the "Unreleased" section with a detailed entry and move it to the appropriate release heading when the version is published.

## [Unreleased]
### Added
- `ensure_ffmpeg()` installs `ffmpeg-static` automatically when FFmpeg is not present.

### Changed
 - Replaced `docs/user_guide.pdf` with a plain-text version. The generator
   script now writes `docs/user_guide.txt` instead of a PDF and the PDF file was
   removed from the repository.
 - `build_installer.py` now passes `--paths src` to `PyInstaller.__main__.run`
   so bundled executables can import the `bootstrapper` module without errors.

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
