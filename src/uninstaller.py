from __future__ import annotations

"""Uninstall packages listed in a requirements file."""

import os
import sys
import subprocess


def pip_uninstall(package: str) -> int:
    """Uninstall *package* using pip via a subprocess."""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "uninstall", "-y", package]
    )
    return result.returncode


def uninstall_packages(requirements_path: str) -> None:
    """Read ``requirements_path`` and uninstall each package listed."""
    with open(requirements_path, 'r', encoding='utf-8') as fh:
        packages = [line.strip() for line in fh if line.strip() and not line.startswith('#')]

    for pkg in packages:
        pip_uninstall(pkg)


if __name__ == '__main__':  # pragma: no cover - used by installer
    default_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    uninstall_packages(default_path)
