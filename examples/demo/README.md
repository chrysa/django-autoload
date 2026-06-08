# django-autoload — runnable demo

A minimal Django project that never hand-maintains `INSTALLED_APPS` or URL
includes: django-autoload discovers them by convention.

## What it shows

- `INSTALLED_APPS = [*DJANGO_APPS, *discover_apps()]` in
  `demo_project/settings.py` — the `apps/` directory is scanned for `apps.py`
  markers.
- `urlpatterns = autodiscover_urls("api")` in `demo_project/urls.py` — every
  `apps/*/api/urls.py` is wired in automatically.
- Per-app `signals.py` modules auto-imported on `ready()` (configured via
  `AUTOLOAD["COMPONENTS"]`).
- Two demo apps under `apps/` (`blog`, `shop`). Drop a third app in with its own
  `apps.py` + `api/urls.py` and it appears with **zero** edits to settings/urls.

## Run it

From the repository root (use Docker or a virtualenv — never system Python):

```bash
pip install -e ".[test]"
```

Then, from this directory (`examples/demo/`):

```bash
python manage.py check       # apps + urls resolve
python manage.py migrate     # contenttypes/auth tables
python manage.py shell -c "from django.conf import settings; print([a for a in settings.INSTALLED_APPS if a.startswith('apps.')])"
```

You should see `['apps.blog', 'apps.shop']` — discovered, not listed by hand —
and the API routes `/blog/posts/` and `/shop/products/` available, each app's
`signals` module already imported.
