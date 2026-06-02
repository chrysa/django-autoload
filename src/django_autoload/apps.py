"""AppConfig that wires component auto-loading into Django's startup."""

from __future__ import annotations

from django.apps import AppConfig


class AutoloadConfig(AppConfig):
    name = "django_autoload"
    verbose_name = "Django Autoload"

    def ready(self) -> None:
        # Imported lazily so the app registry is fully populated first.
        from django.core.checks import register

        from .checks import check_autoload
        from .components import discover_components

        register(check_autoload)
        discover_components()
