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


def _settings_autoload() -> dict[str, Any]:
    """Return ``settings.AUTOLOAD`` only when settings are already configured.

    Checking ``settings.configured`` does **not** trigger ``LazySettings._setup()``,
    so this is safe to call while a settings module is still being built (e.g. from
    ``INSTALLED_APPS = [*discover_apps()]``). During that phase it returns ``{}``
    and callers fall back to the ``DEFAULTS`` merged with any explicit overrides.
    """
    if not settings.configured:
        return {}
    return getattr(settings, "AUTOLOAD", None) or {}


def get_config(overrides: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return the effective configuration.

    Precedence (lowest to highest): :data:`DEFAULTS`, ``settings.AUTOLOAD`` (only
    when settings are configured), then any non-``None`` values in ``overrides``.
    ``overrides`` lets callers pass configuration explicitly and avoid touching
    ``django.conf.settings`` at settings-build time.
    """
    config = {**DEFAULTS, **_settings_autoload()}
    if overrides:
        config.update(
            {key: value for key, value in overrides.items() if value is not None}
        )
    return config


def get_base_dir(overrides: dict[str, Any] | None = None) -> Path:
    """Resolve the project base directory without assuming any layout."""
    configured = get_config(overrides)["BASE_DIR"]
    if configured:
        return Path(configured)
    base = (
        settings.BASE_DIR
        if settings.configured and getattr(settings, "BASE_DIR", None)
        else None
    )
    if base:
        return Path(base)
    return Path.cwd()


def get_roots(overrides: dict[str, Any] | None = None) -> list[Path]:
    """Return the directories to scan. Defaults to ``[BASE_DIR]`` when unset."""
    base = get_base_dir(overrides)
    roots = get_config(overrides)["ROOTS"]
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
