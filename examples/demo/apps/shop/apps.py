"""AppConfig for the demo shop app (the apps.py marker autoload looks for)."""

from __future__ import annotations

from django.apps import AppConfig


class ShopConfig(AppConfig):
    """Configuration for the demo shop app."""

    default_auto_field = "django.db.models.AutoField"
    name = "apps.shop"
    label = "shop"
