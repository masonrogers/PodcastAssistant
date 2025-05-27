import importlib.util
import subprocess
import sys
from typing import List

REQUIRED_PACKAGES = [
    "whisper",
    "pyannote.audio",
    "ffmpeg-python",
    "PySide6",
]


def _missing_packages() -> List[str]:
    missing = []
    for pkg in REQUIRED_PACKAGES:
        if importlib.util.find_spec(pkg) is None:
            missing.append(pkg)
    return missing


def _print_progress(iteration: int, total: int, length: int = 30):
    if total == 0:
        return
    filled_len = int(length * iteration / total)
    bar = "#" * filled_len + "-" * (length - filled_len)
    percent = int(100 * iteration / total)
    print(f"[{bar}] {percent}%")


def install_missing_packages():
    missing = _missing_packages()
    total = len(missing)
    if total == 0:
        print("All packages already installed.")
        return

    for i, pkg in enumerate(missing, 1):
        print(f"Installing {pkg} ({i}/{total})")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
        _print_progress(i, total)
