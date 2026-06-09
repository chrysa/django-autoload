"""django-autoload — convention-over-configuration auto-discovery for Django.

Public API::

    from django_autoload import (
        discover_apps,          # -> list[str] for INSTALLED_APPS
        autoload_into,          # append discovered apps to a list in place
        autodiscover_urls,      # (name) -> list of include() URL patterns
        load_settings,          # merge settings fragments from SETTINGS_DIRS
        discover_app_settings,  # merge per-app settings.py modules
        apply_settings,         # inject a settings mapping onto a module at runtime
        discover_components,    # import per-app components (called on ready())
    )

No project layout is assumed: with no ``AUTOLOAD`` setting, discovery scans
``settings.BASE_DIR``. An ``apps/`` directory is never required.
"""

from __future__ import annotations

from .components import discover_components
from .conf import get_config
from .discovery import autoload_into
from .discovery import discover_app_markers
from .discovery import discover_apps
from .settings import apply_settings
from .settings import discover_app_settings
from .settings import load_settings
from .urls import autodiscover_urls


__all__ = [
    "apply_settings",
    "autodiscover_urls",
    "autoload_into",
    "discover_app_markers",
    "discover_app_settings",
    "discover_apps",
    "discover_components",
    "get_config",
    "load_settings",
]

default_app_config = "django_autoload.apps.AutoloadConfig"
