"""Builds a standalone Whisper Transcriber executable using PyInstaller."""

import os
import PyInstaller.__main__
import pip._vendor.certifi

from src.logging_setup import get_logger, setup_logging


def main() -> None:
    """Build the executable using PyInstaller and log progress."""
    setup_logging()
    logger = get_logger("build_installer")

    cert_path = pip._vendor.certifi.where()
    output_dir = "dist"

    logger.info("Resolved certificate path: %s", cert_path)
    logger.info("Output directory: %s", output_dir)
    logger.info("Starting PyInstaller build")

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
            output_dir,
        ]
    )

    logger.info("PyInstaller build completed")


if __name__ == "__main__":  # pragma: no cover - not tested
    main()
