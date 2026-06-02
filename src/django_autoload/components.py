"""Per-app component loading (signals, receivers, checks, ...).

Invoked from :class:`django_autoload.apps.AutoloadConfig.ready`. For each
discovered app and each configured component name, imports either the matching
``<component>.py`` module or every module inside the ``<component>/`` package.
"""

from __future__ import annotations

import importlib
from pathlib import Path

from .conf import dotted_path
from .conf import get_base_dir
from .conf import get_config
from .discovery import discover_app_markers


def _import_module_dir(directory: Path, *, base: Path) -> None:
    for module_file in sorted(directory.iterdir()):
        if module_file.suffix == ".py" and not module_file.stem.startswith("__"):
            importlib.import_module(dotted_path(module_file, base=base))


def discover_components() -> list[str]:
    """Import all configured components for every discovered app.

    Returns the list of imported dotted paths (useful for logging/tests).
    """
    base = get_base_dir()
    components = get_config()["COMPONENTS"]
    imported: list[str] = []
    if not components:
        return imported

    for marker_file in discover_app_markers():
        app_dir = marker_file.parent
        for component in components:
            package_dir = app_dir / component
            module_file = app_dir / f"{component}.py"
            if package_dir.is_dir():
                _import_module_dir(package_dir, base=base)
                imported.append(dotted_path(package_dir, base=base))
            elif module_file.exists():
                dotted = dotted_path(module_file, base=base)
                importlib.import_module(dotted)
                imported.append(dotted)
    return imported
