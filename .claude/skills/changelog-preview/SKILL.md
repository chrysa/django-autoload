---
name: changelog-preview
description: Regenerate a local preview of the CHANGELOG.md section for an upcoming release from Conventional Commits, before tagging
disable-model-invocation: true
---

# Changelog preview

## When to invoke

User-only, via `/changelog-preview`. Not auto-triggered — this generates
release notes for human review, not a side effect of code changes.

## Procedure

1. Run `git-cliff --unreleased --config cliff.toml` (or the project's
   configured `cliff.toml`) to render the pending changelog section from
   Conventional Commits since the last tag.
2. Print the rendered section without writing it to `CHANGELOG.md` — this is
   a preview only, the real update happens in the `release.yml` CI job.
3. If `git-cliff` is not available locally, tell the user to install it or
   run the equivalent `make` target if one exists, rather than reimplementing
   changelog parsing.

## Output

The rendered Markdown changelog section for the unreleased commits, plus a
one-line note that this is a preview and the authoritative changelog update
happens in CI at tag time.
