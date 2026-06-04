"""Tests for the Django system checks in :mod:`django_autoload.checks`."""

from __future__ import annotations

from pathlib import Path

from django.test import override_settings

from django_autoload.checks import check_autoload


def _autoload(tmp: Path, **extra: object) -> dict:
    return {"BASE_DIR": str(tmp), "ROOTS": ["apps"], **extra}


def test_check_passes_when_apps_discovered(project_tree: Path) -> None:
    with override_settings(AUTOLOAD=_autoload(project_tree)):
        assert check_autoload(app_configs=None) == []


def test_check_errors_when_base_dir_missing(project_tree: Path) -> None:
    cfg = {"BASE_DIR": str(project_tree / "does-not-exist"), "ROOTS": ["apps"]}
    with override_settings(AUTOLOAD=cfg):
        errors = check_autoload(app_configs=None)
    assert [e.id for e in errors] == ["django_autoload.E001"]


def test_check_warns_when_root_missing(project_tree: Path) -> None:
    with override_settings(AUTOLOAD=_autoload(project_tree, ROOTS=["ghost"])):
        ids = {e.id for e in check_autoload(app_configs=None)}
    # A missing root yields W001, and since no markers are found, also W002.
    assert "django_autoload.W001" in ids


def test_check_warns_when_no_app_markers(project_tree: Path) -> None:
    # 'settings' exists but holds no apps.py marker -> only W002 fires.
    with override_settings(AUTOLOAD=_autoload(project_tree, ROOTS=["settings"])):
        ids = {e.id for e in check_autoload(app_configs=None)}
    assert ids == {"django_autoload.W002"}
