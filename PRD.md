# PRD — django-autoload

> Product Requirements. Tags: FACT (verified in-repo), INFERENCE (reasoned from
> evidence), UNKNOWN (not determinable from the repo). Generated as documentation
> only; no source was changed.

## 1. Problem

FACT: Django projects hand-maintain `INSTALLED_APPS`, URL `include()`s and
settings imports. As a project grows, these lists drift from the actual on-disk
apps and must be edited by hand for every new app, component or router
(evidence: `README.md`, `src/django_autoload/__init__.py` module docstring).

## 2. Product summary

FACT: `django-autoload` is a dependency-light Django library providing
convention-over-configuration auto-discovery of apps, URL includes, settings
fragments and per-app components, plus optional integrations for DRF routers,
Celery tasks and RQ/django-rq jobs (evidence: `src/django_autoload/*.py`,
`README.md`, `ARCHITECTURE.md`).

FACT: It makes no assumption about project layout — an `apps/` directory is not
required; with no `AUTOLOAD` setting, discovery scans `settings.BASE_DIR`
(evidence: `conf.py` `DEFAULTS`, `__init__.py` docstring).

FACT: Runtime dependency is Django only (`dependencies = ["django>=4.2"]`,
`pyproject.toml`). Optional extras pull DRF / Celery / RQ / django-rq
(evidence: module docstrings in `routers.py`, `tasks.py`, `jobs.py`).

## 3. Target users

INFERENCE: Django application developers and teams (evidence: PyPI classifier
`Intended Audience :: Developers`, library framing in `README.md`). This is a
developer-facing library, not an end-user application.

## 4. Goals

- FACT: Eliminate hand-maintenance of `INSTALLED_APPS`, URL includes and
  settings imports (evidence: `README.md` opening).
- FACT: Impose no mandatory project layout (evidence: `__init__.py` docstring).
- FACT: Add no runtime dependency beyond Django (evidence: `pyproject.toml`).
- INFERENCE: Fail loudly on misconfiguration via Django system checks
  (evidence: `checks.py`, `apps.py` `ready()` registers `check_autoload`).

## 5. Non-goals

- FACT: The library does one thing — discovery. It does not manage app
  lifecycle beyond discovery (evidence: `README.md` "It does one thing").
- INFERENCE: It is not a project scaffolder or code generator.

## 6. Public capabilities (see REQUIREMENTS.md for the matrix)

FACT (evidence: `src/django_autoload/__init__.py` exports):
- `discover_apps()` → `list[str]` for `INSTALLED_APPS`.
- `autoload_into(list)` — append discovered apps in place.
- `autodiscover_urls(name)` — `include()` URL patterns by logical name.
- `load_settings()` / `discover_app_settings()` — merge UPPER_CASE settings.
- `apply_settings(values, target=...)` — inject settings onto a module at runtime.

FACT (optional extras): `autodiscover_routers()` (`routers.py`, DRF),
`autodiscover_tasks(app)` (`tasks.py`, Celery), `autodiscover_jobs()`
(`jobs.py`, RQ/django-rq).

## 7. Success measures

FACT: Test coverage gate enforced at 85% (`--cov-fail-under=85`, `pyproject.toml`
`addopts`). SonarCloud analysis configured in CI (`.github/workflows/ci.yml`,
`CLAUDE.md`).

UNKNOWN: Adoption / download metrics — not present in the repo. Package version
is `0.1.0` (`pyproject.toml`); PyPI publication status is UNKNOWN from the repo
(a `release.yml` workflow exists but its target registry is not verified here).

## 8. Relationship to fastapi-autoload

FACT (per task brief, corroborated by structure): this Django library is the
original that `fastapi-autoload` ports. No in-repo cross-reference to
`fastapi-autoload` was found; the relationship is asserted by the task, not
verifiable from files in this repository. See DECISIONS.md / REVIEW.md.
