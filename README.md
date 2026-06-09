# django-autoload

Convention-over-configuration auto-discovery for Django. Stop hand-maintaining
`INSTALLED_APPS`, URL includes and settings imports — let the package find them.

It does **one thing**: discovery (apps, urls, settings, app components). It makes
**no assumption** about your project layout — there is no mandatory `apps/`
directory — and pulls in **no dependency** beyond Django.

## Install

```bash
pip install django-autoload
```

Add it to `INSTALLED_APPS` so its `ready()` hook can load app components and
register system checks:

```python
INSTALLED_APPS = ["django_autoload", ...]
```

## Configure (everything optional)

```python
# settings.py
AUTOLOAD = {
    "ROOTS": ["apps"],          # dirs to scan; [] (default) scans BASE_DIR
    "BASE_DIR": BASE_DIR,        # default: settings.BASE_DIR, then cwd
    "APP_MARKER": "apps.py",     # what marks a directory as an app
    "COMPONENTS": ["signals"],   # per-app modules to import on startup
    "URL_PATTERNS": {            # logical name -> relative urls file
        "api": "api/urls.py",
        "admin": "admin_urls.py",
    },
    "SETTINGS_DIRS": ["settings/base"],  # settings fragments to merge
}
```

With no `AUTOLOAD` setting at all, `discover_apps()` finds every package
containing an `apps.py` under `BASE_DIR`.

## Use

```python
# settings.py
from django_autoload import discover_apps, load_settings
INSTALLED_APPS = [*DJANGO_APPS, *discover_apps()]
globals().update(load_settings())            # merge SETTINGS_DIRS fragments

# urls.py
from django_autoload import autodiscover_urls
urlpatterns = autodiscover_urls("api") + autodiscover_urls("admin")
```

When settings must be resolved lazily — e.g. an app injecting its own
`settings.py` from inside `AppConfig.ready()` — use `apply_settings`, the
runtime counterpart of `globals().update(...)`:

```python
# apps/websocket_server/apps.py
import sys
from django.apps import AppConfig
from django_autoload import apply_settings, discover_app_settings

class WebsocketServerConfig(AppConfig):
    name = "apps.websocket_server"

    def ready(self):
        apply_settings(discover_app_settings(), target=sys.modules[__name__])
```

## API

| Function | Purpose |
|---|---|
| `discover_apps()` | dotted paths for `INSTALLED_APPS` |
| `autoload_into(list)` | append discovered apps to an existing list |
| `autodiscover_urls(name)` | `include()` patterns for a `URL_PATTERNS` entry |
| `load_settings(dirs=...)` | merge UPPER_CASE settings from directories |
| `discover_app_settings(filename=...)` | merge per-app settings modules |
| `apply_settings(values, *, target)` | inject a settings mapping onto a module at runtime |
| `discover_components()` | import per-app components (auto-called on `ready()`) |

## Optional extras

These extras pull their dependency in lazily — none is imported unless you
call it, so the core stays Django-only.

### DRF — aggregate routers (`pip install 'django-autoload[drf]'`)

Each app exposes `api/routers.py` with a `router` instance; they are merged:

```python
# urls.py
from django.urls import include, path
from django_autoload.routers import autodiscover_routers

router = autodiscover_routers()                 # filename="api/routers.py", attr="router"
urlpatterns = [path("api/", include(router.urls))]
```

### Celery — autodiscover tasks (`pip install 'django-autoload[celery]'`)

```python
# celery.py
from celery import Celery
from django_autoload.tasks import autodiscover_tasks

app = Celery("proj")
autodiscover_tasks(app)                          # uses discover_apps() as packages
```

### RQ / django-rq — import job modules (`pip install 'django-autoload[rq]'` or `[django-rq]`)

RQ has no task autodiscovery, so each app's job module must be imported once for its
`@job` decorators (rq or django_rq) and rq-scheduler registrations to take effect:

```python
# your AppConfig.ready() or an rq init module
from django_autoload.jobs import autodiscover_jobs

autodiscover_jobs()                              # imports apps/<app>/jobs.py for every app
```

## License

MIT
