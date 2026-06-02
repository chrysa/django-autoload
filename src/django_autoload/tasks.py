"""Optional Celery extra: point Celery at every discovered app.

Requires Celery (``pip install 'django-autoload[celery]'``). Wraps Celery's own
``autodiscover_tasks`` with django-autoload's app list, so the package list is
never hand-maintained.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .discovery import discover_apps


if TYPE_CHECKING:
    from celery import Celery


def autodiscover_tasks(celery_app: Celery, *, related_name: str = "tasks") -> list[str]:
    """Register task modules of every discovered app with ``celery_app``.

    Usage::

        # celery.py
        from django_autoload.tasks import autodiscover_tasks
        app = Celery("proj")
        autodiscover_tasks(app)

    Returns the list of app packages handed to Celery.
    """
    packages = discover_apps()
    celery_app.autodiscover_tasks(packages, related_name=related_name)
    return packages
