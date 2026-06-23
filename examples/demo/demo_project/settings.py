"""Minimal Django settings for the django-autoload demo project.

Note that ``INSTALLED_APPS`` is never hand-maintained: ``discover_apps()`` scans
the ``apps/`` directory for ``apps.py`` markers and returns the dotted paths.
Adding a new app under ``apps/`` makes it show up with zero edits here.
"""

from __future__ import annotations

import os
from pathlib import Path

from django_autoload import discover_apps

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "demo-insecure-key-not-for-production")  # noqa: S105
DEBUG = True
ALLOWED_HOSTS = ["*"]

# All keys optional. Without AUTOLOAD, discovery scans BASE_DIR directly.
AUTOLOAD = {
    "ROOTS": ["apps"],  # scan apps/ for app packages
    "APP_MARKER": "apps.py",  # a dir with apps.py is an app
    "COMPONENTS": ["signals"],  # auto-import each app's signals module on ready()
    "URL_PATTERNS": {"api": "api/urls.py"},  # autodiscover_urls("api") globs these
}

DJANGO_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django_autoload",
]

# The whole point: discovered apps are appended automatically.
INSTALLED_APPS = [*DJANGO_APPS, *discover_apps()]

MIDDLEWARE: list[str] = []
ROOT_URLCONF = "demo_project.urls"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
