"""AppConfig for the demo blog app (the apps.py marker autoload looks for)."""

from __future__ import annotations

from django.apps import AppConfig


class BlogConfig(AppConfig):
    """Configuration for the demo blog app."""

    default_auto_field = "django.db.models.AutoField"
    name = "apps.blog"
    label = "blog"
