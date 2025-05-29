"""Builds a standalone Whisper Transcriber executable using PyInstaller."""

from src.logging_setup import setup_logging, get_logger

setup_logging()
logger = get_logger("build_installer")

import os
import PyInstaller.__main__
import pip._vendor.certifi


def main() -> None:
    logger.info("Building installer")
    cert_path = pip._vendor.certifi.where()
    PyInstaller.__main__.run(
        [
            "src/run_app.py",
            "--paths",
            "src",
            "--name=WhisperTranscriber",
            "--onefile",
            "--windowed",
            "--noconfirm",
            "--hidden-import=pip._vendor.certifi",
            f"--add-data={cert_path}{os.pathsep}pip/_vendor/certifi",
            "--distpath",
            "dist",
        ]
    )


if __name__ == "__main__":  # pragma: no cover - not tested
    main()
