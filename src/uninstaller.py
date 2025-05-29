from __future__ import annotations

"""Uninstall packages listed in a requirements file."""

import os
import sys
import subprocess


def pip_uninstall(package: str) -> int:
    """Uninstall *package* using pip's internal API."""
    from pip._internal.cli.main import main as pip_main

    try:  # register PyInstaller's loader so distlib works in a frozen app
        import pip._vendor.distlib.resources as dist_resources
        import importlib.machinery

        dist_resources._finder_registry[importlib.machinery.FrozenImporter] = (
            dist_resources.ResourceFinder
        )

        try:
            from PyInstaller.loader import pyimod02_importers

            dist_resources._finder_registry[
                pyimod02_importers.FrozenImporter
            ] = dist_resources.ResourceFinder
        except Exception:
            pass
    except Exception:  # pragma: no cover - defensive
        pass

    return pip_main(["uninstall", "-y", package])


def uninstall_packages(requirements_path: str) -> None:
    """Read ``requirements_path`` and uninstall each package listed."""
    with open(requirements_path, 'r', encoding='utf-8') as fh:
        packages = [line.strip() for line in fh if line.strip() and not line.startswith('#')]

    for pkg in packages:
        pip_uninstall(pkg)


if __name__ == '__main__':  # pragma: no cover - used by installer
    default_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    uninstall_packages(default_path)
