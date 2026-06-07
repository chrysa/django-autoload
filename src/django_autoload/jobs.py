"""Optional RQ extra: import every discovered app's job module.

Requires RQ or django-rq (``pip install 'django-autoload[rq]'`` /
``'django-autoload[django-rq]'``). Unlike Celery, RQ has no task autodiscovery —
workers resolve jobs by dotted path at runtime, so modules holding
``@job``-decorated functions (rq or django_rq) or rq-scheduler registrations must
be imported once for those decorators to take effect. This imports them for every
discovered app, so the module list is never hand-maintained. Works for both plain
``rq`` and ``django_rq``.
"""

from __future__ import annotations

import importlib

from .conf import dotted_path
from .conf import get_base_dir
from .discovery import discover_app_markers


def autodiscover_jobs(*, related_name: str = "jobs") -> list[str]:
    """Import the ``<related_name>`` module/package of every discovered app.

    Ensures ``@job`` decorators and rq-scheduler registrations run. Returns the
    list of imported dotted paths (useful for logging/tests).

    Usage::

        # your project's AppConfig.ready() or a dedicated rq init module
        from django_autoload.jobs import autodiscover_jobs
        autodiscover_jobs()
    """
    base = get_base_dir()
    imported: list[str] = []
    for marker_file in discover_app_markers():
        app_dir = marker_file.parent
        package_dir = app_dir / related_name
        module_file = app_dir / f"{related_name}.py"
        if package_dir.is_dir():
            for sub in sorted(package_dir.iterdir()):
                if sub.suffix == ".py" and not sub.stem.startswith("__"):
                    dotted = dotted_path(sub, base=base)
                    importlib.import_module(dotted)
                    imported.append(dotted)
        elif module_file.exists():
            dotted = dotted_path(module_file, base=base)
            importlib.import_module(dotted)
            imported.append(dotted)
    return imported
