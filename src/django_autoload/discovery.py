"""App discovery: locate app packages and build ``INSTALLED_APPS`` entries."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .conf import dotted_path
from .conf import get_base_dir
from .conf import get_config
from .conf import get_roots


def _overrides(base_dir: Any, roots: Any, marker: Any) -> dict[str, Any]:
    return {"BASE_DIR": base_dir, "ROOTS": roots, "APP_MARKER": marker}


def discover_app_markers(
    *, base_dir: Any = None, roots: list[str] | None = None, marker: str | None = None
) -> list[Path]:
    """Return the sorted list of app-marker files found under the scan roots.

    Explicit ``base_dir`` / ``roots`` / ``marker`` take precedence over
    ``settings.AUTOLOAD`` and let this run before settings are configured.
    """
    overrides = _overrides(base_dir, roots, marker)
    marker_name = get_config(overrides)["APP_MARKER"]
    found: list[Path] = []
    for root in get_roots(overrides):
        if root.exists():
            found.extend(root.glob(f"**/{marker_name}"))
    return sorted(set(found))


def discover_apps(
    *, base_dir: Any = None, roots: list[str] | None = None, marker: str | None = None
) -> list[str]:
    """Return importable dotted paths of every discovered app package.

    Suitable for extending ``INSTALLED_APPS``. Pass ``base_dir`` (and optionally
    ``roots`` / ``marker``) explicitly to run at settings-build time without
    touching ``django.conf.settings``::

        from django_autoload import discover_apps
        INSTALLED_APPS = [*DJANGO_APPS, *discover_apps(base_dir=BASE_DIR, roots=["apps"])]
    """
    overrides = _overrides(base_dir, roots, marker)
    base = get_base_dir(overrides)
    apps: list[str] = []
    for marker_file in discover_app_markers(base_dir=base_dir, roots=roots, marker=marker):
        dotted = dotted_path(marker_file.parent, base=base)
        if dotted and dotted not in apps:
            apps.append(dotted)
    return apps


def autoload_into(
    installed_apps: list[str],
    *,
    base_dir: Any = None,
    roots: list[str] | None = None,
    marker: str | None = None,
) -> list[str]:
    """Append discovered apps to ``installed_apps`` in place, skipping duplicates."""
    for app in discover_apps(base_dir=base_dir, roots=roots, marker=marker):
        if app not in installed_apps:
            installed_apps.append(app)
    return installed_apps
