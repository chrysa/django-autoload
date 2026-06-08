"""URL configuration — assembled by auto-discovery.

``autodiscover_urls("api")`` globs every ``api/urls.py`` under the scan roots
and wires them in, so adding a new app's API routes needs no edit here.
"""

from __future__ import annotations

from django_autoload import autodiscover_urls

urlpatterns = autodiscover_urls("api")
