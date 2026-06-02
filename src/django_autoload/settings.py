"""Settings fragment loading and merging.

Two complementary strategies, both optional:

* :func:`load_settings` merges every module found in the configured
  ``SETTINGS_DIRS`` (e.g. a layered ``settings/base/`` directory).
* :func:`discover_app_settings` merges a per-app settings module
  (``settings.py`` by default) found under the scan roots.

Only ``UPPER_CASE`` names are collected, matching Django's settings convention.
"""

from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any

from .conf import dotted_path
from .conf import get_base_dir
from .conf import get_config
from .conf import get_roots


def _extract(dotted: str) -> dict[str, Any]:
    module = importlib.import_module(dotted)
    return {
        name: value
        for name, value in module.__dict__.items()
        if name.isupper() and not name.startswith("__")
    }


def load_settings(*, dirs: list[str] | None = None) -> dict[str, Any]:
    """Merge UPPER_CASE settings from every module in the given directories.

    ``dirs`` defaults to ``AUTOLOAD["SETTINGS_DIRS"]`` (relative to BASE_DIR).
    Modules are imported in sorted order, so later files override earlier ones.
    """
    base = get_base_dir()
    dirs = dirs if dirs is not None else get_config()["SETTINGS_DIRS"]
    merged: dict[str, Any] = {}
    for directory in dirs:
        dir_path = base / directory
        if not dir_path.exists():
            continue
        for module_file in sorted(dir_path.iterdir()):
            if module_file.suffix == ".py" and not module_file.stem.startswith("__"):
                merged.update(_extract(dotted_path(module_file, base=base)))
    return merged


def discover_app_settings(*, filename: str = "settings.py") -> dict[str, Any]:
    """Merge UPPER_CASE settings from a per-app settings module under the roots."""
    base = get_base_dir()
    merged: dict[str, Any] = {}
    seen: set[str] = set()
    for root in get_roots():
        if not root.exists():
            continue
        for settings_file in sorted(root.glob(f"**/{filename}")):
            dotted = dotted_path(settings_file, base=base)
            if dotted not in seen:
                seen.add(dotted)
                merged.update(_extract(dotted))
    return merged
