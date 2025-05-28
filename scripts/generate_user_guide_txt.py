CONTENT_LINES = [
    "Whisper Transcriber User Guide",
    "",
    "Installation:",
    "1. Install Python. FFmpeg will be installed automatically by the bootstrapper.",
    "2. Run 'python build_installer.py' to create the executable.",
    "3. Launch the installer from 'dist/'.",
    "",
    "Basic Usage:",
    "1. Drag audio files into the file list in order.",
    "2. Click 'Transcribe' to process the files.",
    "3. Search or highlight segments in the transcript.",
    "",
    "Exporting:",
    "Use the Export buttons to save TXT, JSON, SRT, or a clipped audio segment.",
    "",
    "Keyword Management:",
    "Edit 'keywords.json' via the Settings dialog to update search terms.",
    "",
    "Uninstallation:",
    "Run 'python src/uninstaller.py' to remove dependencies.",
]


def generate_txt(path: str) -> None:
    """Write the user guide contents to a text file."""
    with open(path, "w", encoding="utf-8") as f:
        for line in CONTENT_LINES:
            f.write(line + "\n")


if __name__ == "__main__":
    generate_txt("docs/user_guide.txt")
