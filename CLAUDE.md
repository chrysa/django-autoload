# CLAUDE.md — django-autoload

> @[claude-sonnet-4-6]
> **Claude Code**: also read `.github/copilot-instructions.md` and any `.github/instructions/*.instructions.md`
> for code specifications. For Django rules see `shared-standards/copilot-instructions/django.md`.

## Project

**Name:** django-autoload
**Stack:** Python 3.14 · Django library (no runtime dependency beyond Django)
**Purpose:** Convention-over-configuration auto-discovery for Django — discovers apps, URL includes,
settings and app components so `INSTALLED_APPS` / `urlpatterns` / settings imports stop being
hand-maintained. Makes no assumption about project layout; pulls in no dependency beyond Django.

## Layout

`src/` layout (PEP 561 library). Public package: `src/django_autoload/`.

```
src/django_autoload/
  discovery.py   # app / module discovery
  settings.py    # settings injection (apply_settings)
  urls.py        # URL auto-include
  components.py  # app-component discovery
  routers.py     # DRF / router wiring
  checks.py      # registered Django system checks (fail loudly at manage.py check)
  conf.py        # configuration surface
tests/           # pytest-django suite (mirrors src)
examples/        # runnable demo project
```

## Conventions

- Language: English — all code, comments, docs, and config files.
- Commits: Conventional Commits (`feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `ci`).
- Branches: `feat/`, `fix/`, `chore/`, `docs/`. Default branch: `main`.
- Build backend: `hatchling` (library tier — allowed per `python-library.md`).

## Standards

- Max function lines: 50 · Max file lines: 500 · Lint warnings: 0
- Test coverage: ≥ 85% (public API is the priority surface)
- `mypy --strict` clean · full type annotations on the public API · `py.typed` present

## Setup

```bash
make install      # pip install -e ".[dev]" + pre-commit install
make lint         # ruff check src tests
make typecheck    # mypy src/django_autoload
make test         # run unit tests
make test-cov     # tests + coverage (term + xml)
make build        # build wheel
```

All checks run via `make` or `pre-commit` only — never invoke `ruff` / `pytest` / `mypy` directly on the host.

## CI

- Runs on push to `main` and on PRs. CI must pass before merging.
- SonarCloud analysis is configured in CI.

## Skills

Shared skills from `shared-standards/.claude/skills/` — load `testing-pytest/SKILL.md` for the
pytest DDD + pytest-mock conventions when writing tests.

<!-- chrysa:standards-import:start -->
@.chrysa/STANDARDS.md
<!-- chrysa:standards-import:end -->

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
