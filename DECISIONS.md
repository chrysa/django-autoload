# Decisions (ADRs) — django-autoload

> Lightweight ADRs reconstructed from code and config. Where the rationale was
> not recorded in the repo, it is marked UNKNOWN rather than invented.
> Documentation only.

## ADR-001 — `src/` layout, PEP 561 library

- Status: FACT (adopted).
- Context: distributable Django library.
- Decision: `src/django_autoload/` layout; typed library (`CLAUDE.md` cites
  `py.typed`).
- Evidence: `pyproject.toml` (`tool.setuptools.packages.find` include
  `django_autoload*`), `CLAUDE.md`.

## ADR-002 — No runtime dependency beyond Django

- Status: FACT.
- Decision: `dependencies = ["django>=4.2"]`; DRF/Celery/RQ are optional extras
  imported lazily inside their helper functions.
- Evidence: `pyproject.toml`, `routers.py`/`tasks.py`/`jobs.py` (local imports,
  `TYPE_CHECKING` guards).

## ADR-003 — No mandatory project layout

- Status: FACT.
- Decision: with no `AUTOLOAD` setting, scan `settings.BASE_DIR`; `ROOTS`
  defaults to empty. An `apps/` directory is never required.
- Evidence: `conf.py` `DEFAULTS`, `__init__.py` docstring.

## ADR-004 — Discovery is safe during settings construction

- Status: FACT.
- Decision: `_settings_autoload()` returns `{}` unless `settings.configured`,
  so `INSTALLED_APPS = [*discover_apps()]` works while settings are still being
  built.
- Evidence: `conf.py`.

## ADR-005 — Fail loudly via Django system checks

- Status: FACT.
- Decision: register `check_autoload` in `AppConfig.ready()`; emit `Error`/
  `Warning` for missing BASE_DIR, missing roots, or roots with no markers.
- Evidence: `checks.py`, `apps.py`.

## ADR-006 — Two-strategy settings loading

- Status: FACT.
- Decision: `load_settings()` (directory of fragments) and
  `discover_app_settings()` (per-app module), both UPPER_CASE-only, plus
  `apply_settings()` for lazy runtime injection.
- Evidence: `settings.py`.

## ADR-007 — RQ jobs imported explicitly (no native autodiscovery)

- Status: FACT.
- Decision: `autodiscover_jobs()` imports each app's `jobs` module so `@job`
  decorators/registrations take effect, since RQ resolves jobs by dotted path.
- Evidence: `jobs.py` docstring.

## ADR-008 — Build backend

- Status: CONTRADICTION (see REVIEW.md).
- `pyproject.toml` declares `requires = ["setuptools>=70", "wheel"]`; `CLAUDE.md`
  states "Build backend: `hatchling`". Not reconciled in the repo.
- Rationale: UNKNOWN.

## ADR-009 — Relationship to fastapi-autoload

- Status: asserted by task, UNKNOWN in-repo.
- This Django library is stated to be the original that `fastapi-autoload`
  ports. No file in this repository references `fastapi-autoload`; the
  relationship cannot be verified from repo contents alone.
