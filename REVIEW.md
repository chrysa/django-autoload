# Documentation Review — django-autoload

> Output of the documentation pass. Records what was generated, contradictions
> found, docs skipped, and open unknowns. Documentation only; no source changed.

## Scope

Repository: `chrysa/django-autoload` (branch `chore/claude-config-drift-hook`).
Docs-only pass: root Markdown created/updated; source, tests, deps, CI and
config untouched.

## Files generated (root)

PRD.md, ARCHITECTURE.md (updated/expanded), REQUIREMENTS.md, CONSTRAINTS.md,
DECISIONS.md, TESTING.md, SECURITY.md, GLOSSARY.md, REVIEW.md.

## Docs skipped (with reason)

- **TRD.md** — folded into ARCHITECTURE.md + REQUIREMENTS.md; a separate
  technical requirements doc would duplicate them for a single-purpose library.
- **OBSERVABILITY.md** — this is a synchronous discovery library with no runtime
  service, logging pipeline, metrics or tracing of its own (helpers return lists
  "useful for logging/tests" but emit no telemetry). Nothing verifiable to
  document. Recorded as intentionally skipped.
- **ROADMAP.md** — no roadmap, milestones or open-issue backlog is present in the
  repo (`CHANGELOG.md` is an empty git-cliff placeholder; version `0.1.0`).
  Skipped to avoid fabrication.

## Contradictions found (not fixed — owner action)

1. **Build backend.** `pyproject.toml` uses `setuptools>=70` + `wheel`, but
   `CLAUDE.md` states "Build backend: `hatchling`". One is stale. (DECISIONS
   ADR-008.)
2. **`py.typed`.** `CLAUDE.md` and README claim `py.typed` is present; the file
   `src/django_autoload/py.typed` was NOT found in this pass. Either it is
   missing (PEP 561 typing marker would not ship) or excluded from the tree.
   (REQ-NFR-004.) Owner should verify.
3. **Classifiers vs Python floor.** `requires-python = ">=3.14"` but PyPI
   classifiers list only generic `Programming Language :: Python :: 3` (no
   minor-version classifier). Cosmetic; not blocking.

## fastapi-autoload relationship

Task states django-autoload is the original that `fastapi-autoload` ports.
No in-repo reference to `fastapi-autoload` exists, so the relationship is
asserted, not verifiable from this repository. Recorded in PRD.md §8 and
DECISIONS ADR-009. The public API shapes (`discover_*`, `autodiscover_*`,
`apply_settings`) are plausibly the port surface but this is INFERENCE.

## Documentation debt / open UNKNOWNs

- Exact `DEFAULTS` literals for `APP_MARKER`, `COMPONENTS`, `URL_PATTERNS`,
  `SETTINGS_DIRS` are in `conf.py`; roles documented, exact default values not
  all transcribed here (kept as FACT-by-reference).
- PyPI publication status of `0.1.0` — UNKNOWN.
- Tested Django/Python version matrix beyond the declared floors — UNKNOWN.
- Whether `py.typed` ships — UNKNOWN (see contradiction #2).

## Existing docs preserved

`README.md`, `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, `CHANGELOG.md`,
`ai-instructions.md`, `handover.md`, `standards/`, `legal/`, `.claude/rules/`
were left unchanged. Only `ARCHITECTURE.md` (a root doc) was expanded in place.

## CLAUDE.md

Left unchanged in this pass — it already carries a rich standards map and a
`## graphify` managed section. No "Documentation map" block was injected to
avoid touching the managed content; the new root docs are discoverable by name.
A compact map may be added later if the owner wants it (PROPOSAL, not done).
