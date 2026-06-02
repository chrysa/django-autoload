"""Tests for the optional DRF and Celery extras (skipped if deps absent)."""

from __future__ import annotations

from pathlib import Path

import pytest
from django.test import override_settings


def _autoload(tmp: Path, **extra: object) -> dict:
    return {"BASE_DIR": str(tmp), "ROOTS": ["apps"], **extra}


def test_autodiscover_routers_merges_registries(project_tree: Path) -> None:
    pytest.importorskip("rest_framework")
    from rest_framework.routers import DefaultRouter
    from rest_framework.viewsets import ViewSet

    from django_autoload.routers import autodiscover_routers

    # Drop a routers module into the blog app exposing one registered viewset.
    routers_file = project_tree / "apps" / "blog" / "api" / "routers.py"
    routers_file.write_text(
        "from rest_framework.routers import DefaultRouter\n"
        "from rest_framework.viewsets import ViewSet\n"
        "class ItemViewSet(ViewSet):\n"
        "    pass\n"
        "router = DefaultRouter()\n"
        "router.register('items', ItemViewSet, basename='item')\n"
    )

    with override_settings(AUTOLOAD=_autoload(project_tree)):
        combined = autodiscover_routers()

    assert isinstance(combined, DefaultRouter)
    prefixes = [prefix for prefix, _viewset, _basename in combined.registry]
    assert "items" in prefixes


def test_autodiscover_tasks_passes_discovered_apps(project_tree: Path) -> None:
    pytest.importorskip("celery")

    from django_autoload.tasks import autodiscover_tasks

    captured: dict[str, object] = {}

    class FakeCelery:
        def autodiscover_tasks(self, packages, related_name="tasks"):
            captured["packages"] = list(packages)
            captured["related_name"] = related_name

    with override_settings(AUTOLOAD=_autoload(project_tree)):
        returned = autodiscover_tasks(FakeCelery(), related_name="jobs")

    assert sorted(returned) == ["apps.blog", "apps.shop"]
    assert captured["packages"] == returned
    assert captured["related_name"] == "jobs"
