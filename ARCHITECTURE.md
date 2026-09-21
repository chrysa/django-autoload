# Architecture — django-autoload

## Purpose

`django-autoload` is a small, dependency-light library that brings
convention-over-configuration auto-discovery to Django projects. Instead of
hand-maintaining `INSTALLED_APPS`, URL includes and settings imports, the
package discovers apps, URL patterns, settings fragments and per-app components
by scanning the project tree. It makes no assumption about project layout (no
mandatory `apps/` directory) and pulls in no runtime dependency beyond Django.

## Stack

- Language: Python 3 (`django>=4.2`).
- Framework: Django (the sole required dependency).
- Optional extras (imported lazily, only when their helper is called):
  `drf` (djangorestframework), `celery`, `rq`, `django-rq`.
- Packaging: setuptools + wheel via `pyproject.toml` (src layout).
- Tooling: Ruff (lint/format), mypy (type-check), pytest + pytest-cov +
  pytest-django (tests, coverage gate 85%), pre-commit, Docker (`Dockerfile.test`).

## Layout

- `src/django_autoload/` — the library package:
  - `__init__.py` — public API surface and `__version__`.
  - `conf.py` — reads and normalises the `AUTOLOAD` settings dict.
  - `discovery.py` — core discovery of apps (`discover_apps`, `autoload_into`).
  - `urls.py` — `autodiscover_urls(name)` include-pattern discovery.
  - `settings.py` — settings-fragment merging (`load_settings`,
    `discover_app_settings`, `apply_settings`).
  - `components.py` — per-app component import (`discover_components`).
  - `apps.py` — `AutoloadConfig` AppConfig; its `ready()` loads components and
    registers checks.
  - `checks.py` — Django system checks.
  - `routers.py` / `tasks.py` / `jobs.py` — optional-extra integrations (DRF
    routers, Celery task autodiscovery, RQ/django-rq job imports).
- `tests/` — pytest suite (`test_discovery.py`, `test_settings_components.py`,
  `test_checks.py`, `test_extras.py`, `conftest.py`).
- `examples/demo/` — an illustrative Django project (not library code) with
  `apps/blog` and `apps/shop`, showing discovery in action.
- Root: `pyproject.toml`, `Makefile`, `Dockerfile.test`, `README.md`,
  `.pre-commit-config.yaml`, CI config under `.github/`.

## Entrypoints

This is a library, not a runnable service — it has no server or CLI entrypoint.
Integration points are the public API functions imported from
`django_autoload` (see the API table in `README.md`), plus:

- `default_app_config = "django_autoload.apps.AutoloadConfig"` — activated by
  adding `"django_autoload"` to `INSTALLED_APPS`; its `ready()` hook drives
  component loading and check registration.
- The `examples/demo/manage.py` project is the runnable demonstration harness.

## Data & external dependencies

- No database of its own. (The demo ships an `examples/demo/db.sqlite3` for the
  sample project only.)
- No network or external services. Behaviour is configured entirely through the
  optional `AUTOLOAD` dict in Django settings; with no config, discovery scans
  `settings.BASE_DIR`.
- Optional integrations activate only when the corresponding extra is installed
  and its helper is explicitly called.

## Build & test

Real commands (from `Makefile` / `pyproject.toml`):

```bash
make install       # pip install -e ".[dev]" + pre-commit install
make test          # pytest tests/ --tb=short
make test-cov      # pytest with coverage (term + xml)
make lint          # ruff check src tests
make format        # ruff format src tests
make typecheck     # mypy src/django_autoload
make build         # python -m build  (wheel)
make docker-test   # build + run tests in Docker via Dockerfile.test
make ci            # lint + typecheck + test
make pre-commit    # pre-commit run --all-files
```

Coverage gate is enforced at 85% (`--cov-fail-under=85`).
