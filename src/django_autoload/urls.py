"""URL auto-discovery driven by the ``URL_PATTERNS`` configuration mapping."""

from __future__ import annotations

from django.urls import URLPattern
from django.urls import URLResolver
from django.urls import include
from django.urls import path

from .conf import dotted_path
from .conf import get_base_dir
from .conf import get_config
from .conf import get_roots


def autodiscover_urls(name: str, *, prefix: str = "") -> list[URLPattern | URLResolver]:
    """Return ``include()`` patterns for every urls file matching ``name``.

    ``name`` keys into ``AUTOLOAD["URL_PATTERNS"]``; the value is a relative path
    (e.g. ``"api/urls.py"``) globbed under each scan root. Unknown names yield
    an empty list, so callers can compose freely::

        urlpatterns = autodiscover_urls("api") + autodiscover_urls("admin")
    """
    patterns_map = get_config()["URL_PATTERNS"]
    suffix = patterns_map.get(name)
    if not suffix:
        return []

    base = get_base_dir()
    result: list[URLPattern | URLResolver] = []
    seen: set[str] = set()
    for root in get_roots():
        if not root.exists():
            continue
        for urls_file in sorted(root.glob(f"**/{suffix}")):
            module = dotted_path(urls_file, base=base)
            if module in seen:
                continue
            seen.add(module)
            result.append(path(prefix, include(module)))
    return result
