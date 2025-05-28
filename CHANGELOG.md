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

