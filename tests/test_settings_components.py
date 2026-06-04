"""Tests for per-app settings discovery and package-style components."""

from __future__ import annotations

from pathlib import Path

from django.test import override_settings

from django_autoload import discover_components
from django_autoload import load_settings
from django_autoload.settings import discover_app_settings


def _autoload(tmp: Path, **extra: object) -> dict:
    return {"BASE_DIR": str(tmp), "ROOTS": ["apps"], **extra}


def test_load_settings_skips_missing_dirs(project_tree: Path) -> None:
    with override_settings(AUTOLOAD=_autoload(project_tree)):
        assert load_settings(dirs=["nope/missing"]) == {}


def test_discover_app_settings_merges_per_app_modules(project_tree: Path) -> None:
    settings_file = project_tree / "apps" / "blog" / "settings.py"
    settings_file.write_text("API_TIMEOUT = 30\nlower = 1\n")
    with override_settings(AUTOLOAD=_autoload(project_tree)):
        assert discover_app_settings() == {"API_TIMEOUT": 30}


def test_discover_components_imports_package_dir(project_tree: Path) -> None:
    pkg = project_tree / "apps" / "blog" / "receivers"
    (pkg / "__init__.py").parent.mkdir(parents=True, exist_ok=True)
    (pkg / "__init__.py").write_text("")
    (pkg / "handlers.py").write_text("LOADED = True\n")
    with override_settings(AUTOLOAD=_autoload(project_tree, COMPONENTS=["receivers"])):
        imported = discover_components()
    assert "apps.blog.receivers" in imported
