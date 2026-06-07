# Decisions

## Adopt chrysa canonical CI/process workflows and pre-commit baseline

- **Date:** 2026-06-07
- **Status:** Accepted
- **Context:** Repo configuration drifted from the chrysa standard (OPS-190).
- **Decision:** Adopt the canonical hygiene files, GitHub process workflows,
  and the Full pre-commit baseline defined in `chrysa/shared-standards`
  (EXECUTION_STANDARD section 8/14, ADR 0001).
- **Consequences:** CI job contract (pre-commit/lint/test/sonar) and branch
  protection align across the ecosystem; per-repo tuning stays in this file.
