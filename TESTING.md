# Testing — django-autoload

> Documentation only. Commands are transcribed from the repo; they were not
> executed during this pass (env is container-first per repo policy).

## Framework (FACT)

pytest + pytest-django. Config in `pyproject.toml` `[tool.pytest.ini_options]`:
`addopts = "-v --tb=short --cov=django_autoload --cov-report=term-missing --cov-fail-under=85"`.

## Suite (FACT — `tests/`)

| File                         | Focus                                   |
| ---------------------------- | --------------------------------------- |
| `tests/conftest.py`          | pytest-django fixtures / settings setup |
| `tests/test_discovery.py`    | app discovery (`discover_apps`, markers)|
| `tests/test_settings_components.py` | settings merge + component loading |
| `tests/test_checks.py`       | Django system check behaviour           |
| `tests/test_extras.py`       | optional DRF/Celery/RQ integrations     |

FACT: 19 `def test_*` functions across the suite (grep count).

## Commands (FACT — `Makefile`, `CLAUDE.md`)

All checks run via `make` or `pre-commit` only — never invoke `ruff` / `pytest`
/ `mypy` directly on the host (per `CLAUDE.md`).

```bash
make install      # pip install -e ".[dev]" + pre-commit install
make lint         # ruff check src tests
make typecheck    # mypy src/django_autoload
make test         # run unit tests
make test-cov     # tests + coverage (term + xml)
make test-docker  # build Dockerfile.test and run the suite in a container
make build        # build wheel
make clean        # remove caches/build artifacts
```

INFERENCE: `make test-docker` (name per `Makefile`) builds `Dockerfile.test`,
runs the container without `--rm`, then `docker cp` extracts `coverage.xml`
before removing the container (evidence: `Makefile` recipe comments).

## Coverage gate (FACT)

85% minimum (`--cov-fail-under=85`). `coverage.xml` uses repo-relative paths so
SonarCloud can map sources (`pyproject.toml` comment).

## Test dependencies (FACT — `pyproject.toml` `test` extra)

`pytest`, `pytest-cov>=5.0`, `pytest-django`, `djangorestframework>=3.14`,
`celery>=5.3`, `rq>=1.10`, `django-rq>=2.5` — the last four back
`tests/test_extras.py`.

## CI (FACT — `.github/workflows/ci.yml`)

Runs test + sonar on PRs and pushes. Lint/type are NOT in this workflow by
design (they live in pre-commit and in release-time CI) to avoid per-push lint
billing. Job names `test` / `sonar` are branch-protection required checks.
