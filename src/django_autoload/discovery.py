"""App discovery: locate app packages and build ``INSTALLED_APPS`` entries."""

from __future__ import annotations

from pathlib import Path

from .conf import dotted_path
from .conf import get_base_dir
from .conf import get_config
from .conf import get_roots


def discover_app_markers() -> list[Path]:
    """Return the sorted list of app-marker files found under the scan roots."""
    marker = get_config()["APP_MARKER"]
    found: list[Path] = []
    for root in get_roots():
        if root.exists():
            found.extend(root.glob(f"**/{marker}"))
    return sorted(set(found))


def discover_apps() -> list[str]:
    """Return importable dotted paths of every discovered app package.

    Suitable for extending ``INSTALLED_APPS``::

        from django_autoload import discover_apps
        INSTALLED_APPS = [*DJANGO_APPS, *discover_apps()]
    """
    base = get_base_dir()
    apps: list[str] = []
    for marker_file in discover_app_markers():
        dotted = dotted_path(marker_file.parent, base=base)
        if dotted and dotted not in apps:
            apps.append(dotted)
    return apps


def autoload_into(installed_apps: list[str]) -> list[str]:
    """Append discovered apps to ``installed_apps`` in place, skipping duplicates."""
    for app in discover_apps():
        if app not in installed_apps:
            installed_apps.append(app)
    return installed_apps
