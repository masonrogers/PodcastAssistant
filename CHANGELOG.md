# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
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

### Changed
- Bootstrapper now installs PySide6 first so the progress window can launch
  before installing remaining dependencies.

