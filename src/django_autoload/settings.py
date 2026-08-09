"""Settings fragment loading and merging.

Two complementary strategies, both optional:

* :func:`load_settings` merges every module found in the configured
  ``SETTINGS_DIRS`` (e.g. a layered ``settings/base/`` directory).
* :func:`discover_app_settings` merges a per-app settings module
  (``settings.py`` by default) found under the scan roots.

Only ``UPPER_CASE`` names are collected, matching Django's settings convention.
:func:`apply_settings` then injects a merged mapping onto a target module at
runtime, the counterpart of the ``globals().update(load_settings())`` idiom.
"""

from __future__ import annotations

import importlib
from types import ModuleType
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


def load_settings(*, dirs: list[str] | None = None, base_dir: Any = None) -> dict[str, Any]:
    """Merge UPPER_CASE settings from every module in the given directories.

    ``dirs`` defaults to ``AUTOLOAD["SETTINGS_DIRS"]`` (relative to BASE_DIR).
    Pass ``base_dir`` explicitly to run before settings are configured. Modules
    are imported in sorted order, so later files override earlier ones.
    """
    overrides = {"BASE_DIR": base_dir}
    base = get_base_dir(overrides)
    dirs = dirs if dirs is not None else get_config(overrides)["SETTINGS_DIRS"]
    merged: dict[str, Any] = {}
    for directory in dirs:
        dir_path = base / directory
        if not dir_path.exists():
            continue
        for module_file in sorted(dir_path.iterdir()):
            if module_file.suffix == ".py" and not module_file.stem.startswith("__"):
                merged.update(_extract(dotted_path(module_file, base=base)))
    return merged


def discover_app_settings(
    *, filename: str = "settings.py", base_dir: Any = None, roots: list[str] | None = None
) -> dict[str, Any]:
    """Merge UPPER_CASE settings from a per-app settings module under the roots."""
    overrides = {"BASE_DIR": base_dir, "ROOTS": roots}
    base = get_base_dir(overrides)
    merged: dict[str, Any] = {}
    seen: set[str] = set()
    for root in get_roots(overrides):
        if not root.exists():
            continue
        for settings_file in sorted(root.glob(f"**/{filename}")):
            dotted = dotted_path(settings_file, base=base)
            if dotted not in seen:
                seen.add(dotted)
                merged.update(_extract(dotted))
    return merged


def apply_settings(values: dict[str, Any], *, target: ModuleType | str) -> None:
    """Set each item of ``values`` as an attribute on ``target`` at runtime.

    The runtime counterpart of ``globals().update(load_settings())``: use it when
    settings are resolved lazily — typically inside ``AppConfig.ready()`` — and
    must be injected into a module that is not the caller's own namespace.

    ``target`` is a module object or a dotted module name (imported on demand).
    Every key is written as-is; callers usually pass the result of
    :func:`load_settings` or :func:`discover_app_settings`, which already keep
    UPPER_CASE names only.
    """
    module = importlib.import_module(target) if isinstance(target, str) else target
    for name, value in values.items():
        setattr(module, name, value)
