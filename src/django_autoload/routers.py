"""Optional DRF extra: aggregate per-app routers into a single one.

Requires Django REST Framework (``pip install 'django-autoload[drf]'``).
Each matching module must expose a DRF router instance (named ``router`` by
default); their registries are merged into one combined ``DefaultRouter``.
"""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING

from .conf import dotted_path
from .conf import get_base_dir
from .conf import get_roots


if TYPE_CHECKING:
    from rest_framework.routers import DefaultRouter


def autodiscover_routers(
    *, filename: str = "api/routers.py", attr: str = "router"
) -> DefaultRouter:
    """Return a ``DefaultRouter`` merging every discovered app router.

    Usage::

        # urls.py
        from django_autoload.routers import autodiscover_routers
        router = autodiscover_routers()
        urlpatterns = [path("api/", include(router.urls))]
    """
    from rest_framework.routers import DefaultRouter

    base = get_base_dir()
    combined = DefaultRouter()
    seen: set[str] = set()
    for root in get_roots():
        if not root.exists():
            continue
        for module_file in sorted(root.glob(f"**/{filename}")):
            dotted = dotted_path(module_file, base=base)
            if dotted in seen:
                continue
            seen.add(dotted)
            module = importlib.import_module(dotted)
            router = getattr(module, attr, None)
            if router is not None:
                combined.registry.extend(router.registry)
    return combined
