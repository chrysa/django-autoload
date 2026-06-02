"""Pytest fixtures: configure a minimal Django and a synthetic project tree."""

from __future__ import annotations

import sys
from pathlib import Path

import django
import pytest
from django.conf import settings


def pytest_configure() -> None:
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            INSTALLED_APPS=["django_autoload"],
            DATABASES={},
            AUTOLOAD={},
        )
        django.setup()


def _write(path: Path, content: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


@pytest.fixture
def project_tree(tmp_path: Path) -> Path:
    """Build a fake project with two apps under ``apps/`` and put it on sys.path.

        <tmp>/apps/blog/apps.py
        <tmp>/apps/blog/api/urls.py
        <tmp>/apps/blog/signals.py
        <tmp>/apps/shop/apps.py
        <tmp>/settings/base/a.py  (UPPER setting)
    """
    _write(tmp_path / "apps" / "__init__.py")
    _write(tmp_path / "apps" / "blog" / "__init__.py")
    _write(tmp_path / "apps" / "blog" / "apps.py")
    _write(tmp_path / "apps" / "blog" / "api" / "__init__.py")
    _write(
        tmp_path / "apps" / "blog" / "api" / "urls.py",
        "from django.urls import path\nurlpatterns = [path('blog/', lambda r: None)]\n",
    )
    _write(
        tmp_path / "apps" / "blog" / "signals.py",
        "LOADED = True\n",
    )
    _write(tmp_path / "apps" / "shop" / "__init__.py")
    _write(tmp_path / "apps" / "shop" / "apps.py")
    _write(tmp_path / "settings" / "__init__.py")
    _write(tmp_path / "settings" / "base" / "__init__.py")
    _write(tmp_path / "settings" / "base" / "a.py", "MY_SETTING = 42\nlower = 1\n")

    sys.path.insert(0, str(tmp_path))
    yield tmp_path
    sys.path.remove(str(tmp_path))
