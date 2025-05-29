"""PodcastAssistant public interface.

Only lazily exposes the underlying modules. This avoids importing heavy
dependencies until explicitly requested.
"""

from __future__ import annotations

import importlib
import types

__all__ = [
    "transcript_aggregator",
    "keyword_index",
    "clip_exporter",
    "transcript_exporter",
    "settings",
    "main_window",
]


def __getattr__(name: str) -> types.ModuleType:
    """Dynamically import submodules when accessed.

    This function implements PEP 562 module ``__getattr__`` so accessing an
    attribute like ``src.transcript_aggregator`` triggers an import of the
    corresponding submodule.
    """
    if name in __all__:
        return importlib.import_module(f".{name}", __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    """Return available attributes for ``dir()`` calls."""
    return sorted(list(globals().keys()) + __all__)
