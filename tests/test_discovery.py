"""Tests covering app, url, settings and component discovery."""

from __future__ import annotations

import types
from pathlib import Path

from django.test import override_settings

from django_autoload import apply_settings
from django_autoload import autodiscover_urls
from django_autoload import autoload_into
from django_autoload import discover_apps
from django_autoload import discover_components
from django_autoload import load_settings


def _autoload(tmp: Path, **extra: object) -> dict:
    return {"BASE_DIR": str(tmp), "ROOTS": ["apps"], **extra}


def test_discover_apps_finds_marked_packages(project_tree: Path) -> None:
    with override_settings(AUTOLOAD=_autoload(project_tree)):
        assert sorted(discover_apps()) == ["apps.blog", "apps.shop"]


def test_autoload_into_skips_duplicates(project_tree: Path) -> None:
    with override_settings(AUTOLOAD=_autoload(project_tree)):
        installed = ["apps.blog"]
        autoload_into(installed)
        assert installed == ["apps.blog", "apps.shop"]


def test_default_roots_scan_base_dir(project_tree: Path) -> None:
    # No ROOTS -> scans BASE_DIR, still finds both apps.
    with override_settings(AUTOLOAD={"BASE_DIR": str(project_tree)}):
        assert sorted(discover_apps()) == ["apps.blog", "apps.shop"]


def test_autodiscover_urls_known_and_unknown(project_tree: Path) -> None:
    cfg = _autoload(project_tree, URL_PATTERNS={"api": "api/urls.py"})
    with override_settings(AUTOLOAD=cfg):
        assert len(autodiscover_urls("api")) == 1
        assert autodiscover_urls("missing") == []


def test_load_settings_merges_only_upper_case(project_tree: Path) -> None:
    cfg = _autoload(project_tree, SETTINGS_DIRS=["settings/base"])
    with override_settings(AUTOLOAD=cfg):
        loaded = load_settings()
        assert loaded == {"MY_SETTING": 42}


def test_discover_components_imports_module(project_tree: Path) -> None:
    cfg = _autoload(project_tree, COMPONENTS=["signals"])
    with override_settings(AUTOLOAD=cfg):
        imported = discover_components()
        assert "apps.blog.signals" in imported


def test_apply_settings_sets_attrs_on_module_object() -> None:
    target = types.ModuleType("dummy_target")
    apply_settings({"FOO": 1, "BAR": "x"}, target=target)
    assert target.FOO == 1
    assert target.BAR == "x"


def test_apply_settings_accepts_dotted_target(project_tree: Path) -> None:
    # apps.blog.signals exists in the synthetic tree and is importable.
    apply_settings({"INJECTED": 7}, target="apps.blog.signals")
    import apps.blog.signals as signals

    assert signals.INJECTED == 7
