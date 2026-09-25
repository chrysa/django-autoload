# Constraints — django-autoload

> Tags: [HARD] enforced by code/tooling; [SOFT] convention/policy; [ENV]
> environment; [UNKNOWN]. Documentation only.

## Language / runtime

- [HARD] Python `>=3.14` (`pyproject.toml requires-python`).
- [HARD] Django `>=4.2` runtime dependency; no other runtime deps
  (`pyproject.toml dependencies`).
- [SOFT] Public API fully typed; `mypy --strict` clean; `py.typed` present
  (`CLAUDE.md`). Enforcement location: pre-commit / release CI.

## Optional integrations

- [HARD] DRF / Celery / RQ / django-rq are optional extras, imported lazily; the
  core must import without them (`routers.py`/`tasks.py`/`jobs.py`).

## Quality gates

- [HARD] Coverage ≥ 85% (`--cov-fail-under=85`, `pyproject.toml`).
- [SOFT] Lint (ruff) + type (mypy) run in pre-commit and at release time, not in
  per-push CI (`ci.yml` header, `CLAUDE.md`).
- [SOFT] SonarCloud analysis in CI.

## Developer loop

- [SOFT] All checks run via `make` or `pre-commit` only — never invoke
  `ruff`/`pytest`/`mypy` directly on the host (`CLAUDE.md`).
- [ENV] Container-first policy (chrysa standards, `standards/rules/containers.md`);
  test container via `Dockerfile.test`.

## SCM / governance

- [SOFT] Branches `feat/`/`fix/`/`chore/`/`docs/`; default branch `main`
  (`CLAUDE.md`). Repo-wide chrysa standards mandate develop workspace + PR-per-issue
  + Shortcut story reference (`standards/rules/scm.md`, workflows
  `enforce-shortcut-link.yml`).
- [SOFT] Repo depends on `project-init`; declares profile + DDD level
  (`standards/rules/architecture.md`).

## Config surface

- [HARD] `AUTOLOAD` settings dict is optional; keys are normalised over
  `DEFAULTS` in `conf.py`. Precedence: DEFAULTS < settings.AUTOLOAD < overrides.

## Unknowns

- [UNKNOWN] Minimum supported Django ceiling / tested Django matrix beyond `>=4.2`.
- [UNKNOWN] Whether the package is published to PyPI at version `0.1.0`.
