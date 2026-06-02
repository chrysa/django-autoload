"""Django system checks validating the autoload configuration."""

from __future__ import annotations

from typing import Any

from django.core.checks import Error
from django.core.checks import Warning as DjangoWarning

from .conf import get_base_dir
from .conf import get_config
from .conf import get_roots
from .discovery import discover_app_markers


def check_autoload(app_configs: Any, **kwargs: Any) -> list[Any]:
    errors: list[Any] = []
    config = get_config()

    base = get_base_dir()
    if not base.exists():
        errors.append(
            Error(
                f"Autoload BASE_DIR does not exist: {base}",
                id="django_autoload.E001",
            )
        )
        return errors

    for root in get_roots():
        if not root.exists():
            errors.append(
                DjangoWarning(
                    f"Configured AUTOLOAD root does not exist: {root}",
                    hint="Remove it from AUTOLOAD['ROOTS'] or create the directory.",
                    id="django_autoload.W001",
                )
            )

    if config["ROOTS"] and not discover_app_markers():
        errors.append(
            DjangoWarning(
                "No app markers found under the configured roots.",
                hint=f"Expected files named {config['APP_MARKER']!r}.",
                id="django_autoload.W002",
            )
        )

    return errors
