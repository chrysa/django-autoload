# Architecture — django-autoload

> This file existed before this documentation pass and has been expanded.
> Tags: FACT / INFERENCE / UNKNOWN. Documentation only; no source changed.

## Purpose

FACT: `django-autoload` is a small, dependency-light library that brings
convention-over-configuration auto-discovery to Django: it discovers apps, URL
includes, settings fragments and per-app components so `INSTALLED_APPS`,
`urlpatterns` and settings imports stop being hand-maintained (evidence:
`README.md`, module docstrings).

## Layout (FACT — `src/` PEP 561 library)

```
src/django_autoload/
  __init__.py    # public API surface + __version__ (importlib.metadata)
  conf.py        # reads/normalises the AUTOLOAD dict; DEFAULTS; path helpers
  discovery.py   # discover_apps, autoload_into, discover_app_markers
  urls.py        # autodiscover_urls(name) — include() pattern discovery
  settings.py    # load_settings, discover_app_settings, apply_settings
  components.py  # discover_components() — per-app signals/receivers/... import
  apps.py        # AutoloadConfig; ready() loads components + registers checks
  checks.py      # check_autoload — Django system check (fail loudly)
  routers.py     # optional DRF extra: autodiscover_routers()
  tasks.py       # optional Celery extra: autodiscover_tasks()
  jobs.py        # optional RQ/django-rq extra: autodiscover_jobs()
tests/           # pytest-django suite (mirrors src)
examples/demo/   # runnable demo project (apps/blog, apps/shop)
```

## Configuration surface (FACT — `conf.py` `DEFAULTS`)

The optional `AUTOLOAD` dict in Django settings, merged over `DEFAULTS`:

| Key             | Default            | Role                                                        |
| --------------- | ------------------ | ----------------------------------------------------------- |
| `ROOTS`         | `[]`               | Sub-dirs (relative to BASE_DIR) to scan; empty → scan BASE_DIR |
| `BASE_DIR`      | `None`             | Explicit project root; None → `settings.BASE_DIR`, then `cwd()` |
| `APP_MARKER`    | `apps.py`*         | Filename that marks a directory as a Django app package      |
| `COMPONENTS`    | e.g. `["signals"]`*| Per-app modules/packages imported on `ready()`               |
| `URL_PATTERNS`  | mapping*           | logical name → relative urls file (used by `autodiscover_urls`) |
| `SETTINGS_DIRS` | *                  | Dirs merged by `load_settings()`                            |

INFERENCE (*): exact default literals live in `conf.py` `DEFAULTS`; the roles
above are FACT from the inline comments and docstrings.

Precedence (FACT, `conf.py get_config`): `DEFAULTS` < `settings.AUTOLOAD` (only
when `settings.configured`) < non-`None` `overrides`. `_settings_autoload()`
returns `{}` while a settings module is still being built, so discovery is safe
to call from `INSTALLED_APPS = [*discover_apps()]`.

## Runtime wiring (FACT)

1. Project adds `"django_autoload"` to `INSTALLED_APPS`.
2. `AutoloadConfig.ready()` (`apps.py`) runs at startup: registers the
   `check_autoload` system check and calls `discover_components()`.
3. `discover_components()` (`components.py`) imports each configured component
   (`<component>.py` module or every module in a `<component>/` package) for
   every discovered app marker.
4. URL / settings / router / task / job helpers are explicitly called by the
   host project where needed (they are not auto-invoked by `ready()`).

## Path resolution (FACT — `conf.dotted_path`)

Filesystem paths under the scan roots are converted to importable dotted module
paths relative to BASE_DIR (package path for dirs, module path without `.py` for
files). Discovery de-duplicates via `seen` sets and sorts globs for
determinism.

## Optional integrations (FACT)

- `routers.autodiscover_routers()` — merges each app's DRF `router` registry
  into one `DefaultRouter` (requires `[drf]`).
- `tasks.autodiscover_tasks(celery_app)` — wraps Celery `autodiscover_tasks`
  with the discovered app list (requires `[celery]`).
- `jobs.autodiscover_jobs()` — imports each app's `jobs` module/package so
  `@job` decorators run; RQ has no native task autodiscovery (requires
  `[rq]` / `[django-rq]`).

## Quality gates (FACT)

Coverage gate 85% (`pyproject.toml`). Lint/type (ruff, `mypy --strict`) run in
pre-commit + release-time CI, not per-push (evidence: `CLAUDE.md`, `ci.yml`
header). See TESTING.md.
