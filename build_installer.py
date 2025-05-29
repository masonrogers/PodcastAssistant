"""Builds a standalone Whisper Transcriber executable using PyInstaller."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.logging_setup import setup_logging, get_logger

logger = get_logger("build_installer")

import os
import PyInstaller.__main__
import pip._vendor.certifi


def main() -> None:
    """Run PyInstaller to build the executable."""
    setup_logging()

    logger.info("Starting PyInstaller build")
    cert_path = pip._vendor.certifi.where()
    out_dir = "dist"
    logger.info("Resolved certificate path: %s", cert_path)
    logger.info("Output directory: %s", out_dir)

    logger.info("Invoking PyInstaller")
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
            "--collect-all=whispercpp",
            "--hidden-import=whispercpp",
            f"--add-data={cert_path}{os.pathsep}pip/_vendor/certifi",
            f"--add-data=requirements.txt{os.pathsep}.",
            f"--add-data=src/uninstaller.py{os.pathsep}.",
            "--distpath",
            out_dir,
        ]
    )
    logger.info("PyInstaller build completed")


if __name__ == "__main__":  # pragma: no cover - not tested
    main()
