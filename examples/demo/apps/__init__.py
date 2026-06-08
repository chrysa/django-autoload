"""Container package for the demo apps.

``LOADED_COMPONENTS`` lets the demo prove that each app's ``signals`` module was
auto-imported on ``ready()`` without any manual import.
"""

from __future__ import annotations

LOADED_COMPONENTS: list[str] = []
