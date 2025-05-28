"""Builds a standalone Whisper Transcriber executable using PyInstaller."""

import PyInstaller.__main__


def main() -> None:
    PyInstaller.__main__.run(
        [
            "src/run_app.py",
            "--paths",
            "src",
            "--name=WhisperTranscriber",
            "--onefile",
            "--windowed",
            "--noconfirm",
            "--distpath",
            "dist",
        ]
    )


if __name__ == "__main__":  # pragma: no cover - not tested
    main()
