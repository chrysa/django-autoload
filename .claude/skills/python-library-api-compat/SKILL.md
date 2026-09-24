---
name: python-library-api-compat
description: Diff the public API surface of django_autoload against the previous release and flag breaking changes requiring a major version bump
---

# Python library API compatibility

## When to invoke

Auto-invoke when a diff touches public modules under `src/django_autoload/`
(`discovery.py`, `settings.py`, `urls.py`, `components.py`, `conf.py`) before a
PR is opened. Can also be run manually: `/python-library-api-compat`.

## Procedure

1. Identify the previous released tag: `git describe --tags --abbrev=0`.
2. Diff public symbols (functions, classes, method signatures — anything not
   prefixed `_`) in the changed files between that tag and the current branch.
3. Classify each change:
   - **Breaking**: removed symbol, removed/renamed parameter, narrowed
     parameter type, changed return type, new required parameter.
   - **Additive**: new symbol, new optional parameter with a default.
   - **Internal**: change confined to `_`-prefixed names — ignore.
4. If any breaking change is found, state it explicitly and confirm the PR
   bumps the major version per `GitVersion.yml` / semver rules (or flag it as
   missing).
5. Report additive-only changes as informational, no version-bump requirement
   beyond minor.

## Output

One line per changed public symbol: `file:line — symbol — breaking|additive`.
End with a verdict: `SAFE` (no breaking changes) or `MAJOR BUMP REQUIRED`
(with the offending symbols listed).
