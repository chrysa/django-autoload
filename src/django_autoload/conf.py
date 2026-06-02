"""Configuration resolution for django-autoload.

Everything is optional. With no ``AUTOLOAD`` setting at all, discovery scans
``settings.BASE_DIR`` (or the current working directory as a last resort).
No project layout — such as an ``apps/`` directory — is ever assumed.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from django.conf import settings


DEFAULTS: dict[str, Any] = {
    # Sub-directories (relative to BASE_DIR) to scan. Empty -> scan BASE_DIR itself.
    "ROOTS": [],
    # Explicit project root. None -> settings.BASE_DIR, then Path.cwd().
    "BASE_DIR": None,
    # Filename whose presence marks a directory as a Django app package.
    "APP_MARKER": "apps.py",
    # Per-app sub-modules/packages to import on ready() (e.g. "signals", "receivers").
    "COMPONENTS": [],
    # Mapping of logical name -> relative urls file, used by autodiscover_urls().
    # e.g. {"api": "api/urls.py", "admin": "admin_urls.py"}
    "URL_PATTERNS": {},
    # Directories (relative to BASE_DIR) holding settings fragments to merge.
    "SETTINGS_DIRS": [],
}


def get_config() -> dict[str, Any]:
    """Return the effective configuration (defaults merged with ``settings.AUTOLOAD``)."""
    user = getattr(settings, "AUTOLOAD", None) or {}
    return {**DEFAULTS, **user}


def get_base_dir() -> Path:
    """Resolve the project base directory without assuming any layout."""
    configured = get_config()["BASE_DIR"]
    if configured:
        return Path(configured)
    base = getattr(settings, "BASE_DIR", None)
    if base:
        return Path(base)
    return Path.cwd()


def get_roots() -> list[Path]:
    """Return the directories to scan. Defaults to ``[BASE_DIR]`` when unset."""
    base = get_base_dir()
    roots = get_config()["ROOTS"]
    if not roots:
        return [base]
    return [base / root for root in roots]


def dotted_path(target: Path, *, base: Path | None = None) -> str:
    """Convert a filesystem path into an importable dotted module path.

    For a directory, returns the package path. For a ``.py`` file, returns the
    module path (without the ``.py`` suffix).
    """
    base = base or get_base_dir()
    relative = target.relative_to(base)
    if relative.suffix == ".py":
        return ".".join([*relative.parts[:-1], relative.stem])
    return ".".join(relative.parts)
