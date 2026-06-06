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


def test_autodiscover_jobs_imports_app_job_modules(project_tree: Path) -> None:
    import importlib

    from django_autoload.jobs import autodiscover_jobs

    # Default related_name: a jobs.py exposing a sentinel in the blog app.
    (project_tree / "apps" / "blog" / "jobs.py").write_text("LOADED = True\n")
    # Custom related_name: a queue_tasks.py in the shop app.
    (project_tree / "apps" / "shop" / "queue_tasks.py").write_text("LOADED = True\n")

    with override_settings(AUTOLOAD=_autoload(project_tree)):
        default = autodiscover_jobs()
        custom = autodiscover_jobs(related_name="queue_tasks")

    assert default == ["apps.blog.jobs"]
    assert importlib.import_module("apps.blog.jobs").LOADED is True
    assert custom == ["apps.shop.queue_tasks"]
    assert importlib.import_module("apps.shop.queue_tasks").LOADED is True


def test_autodiscover_jobs_with_django_rq(project_tree: Path) -> None:
    pytest.importorskip("django_rq")

    from django_autoload.jobs import autodiscover_jobs

    (project_tree / "apps" / "blog" / "jobs.py").write_text(
        "from django_rq import job\n@job\ndef add(a, b):\n    return a + b\n"
    )

    with override_settings(
        AUTOLOAD=_autoload(project_tree),
        RQ_QUEUES={"default": {"HOST": "localhost", "PORT": 6379, "DB": 0}},
    ):
        returned = autodiscover_jobs()

    assert returned == ["apps.blog.jobs"]
