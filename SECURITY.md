# Security — django-autoload

> Documentation-only review for the repository owner. No code was changed and no
> finding was fixed here. Severity tags: CRITICAL / HIGH / MEDIUM / LOW / INFO.
> Tags: FACT / INFERENCE.

## Secret scan

FACT: No hardcoded real secrets, keys, tokens or credentials were found in
library source (`src/`) or the demo (`examples/`).

INFO: `examples/demo/demo_project/settings.py` sets
`SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "demo-insecure-key-not-for-production")`
— an environment-driven value with an explicitly-labelled insecure placeholder
default, annotated `# noqa: S105`. This is a demo project, not shipped library
code, and the placeholder is not a real secret. No action required; do not use
the demo settings in production (it also sets `DEBUG = True`, `ALLOWED_HOSTS = ["*"]`).

## Attack surface (FACT / INFERENCE)

INFERENCE (by design, not a vulnerability): the library's core mechanism is
dynamic import of modules discovered on the filesystem (`importlib.import_module`
on paths derived from scan roots in `discovery.py`, `components.py`,
`settings.py`, `urls.py`, `routers.py`, `jobs.py`). This means any `.py` under a
configured scan root that matches a marker/component/urls/settings/jobs pattern
is imported at startup and its top-level code runs.

- INFO: This is inherent to convention-over-configuration autoloading and is the
  same trust boundary as Django's own app loading. The scan roots come from the
  project's own settings, so the trust boundary is the developer's own source
  tree — not external input. No user-supplied or network input reaches the
  import path in this library.
- INFERENCE: Consumers should keep scan roots pointed at trusted first-party
  code and avoid pointing `ROOTS` at directories that can contain attacker-writable
  `.py` files. Worth a one-line note in README for downstream users (owner call).

## Dangerous constructs

FACT: No `eval` / `exec` / `pickle` / `os.system` / `subprocess` / `__import__`
usage in `src/`. Only `importlib.import_module` (intended behaviour).

## Input validation

FACT: The library reads configuration from Django settings (`AUTOLOAD` dict),
not from untrusted request input. The `check_autoload` system check validates
that BASE_DIR and configured roots exist (`checks.py`), surfacing
misconfiguration at `manage.py check` time.

## Findings summary

No HIGH or CRITICAL findings. Items above are INFO/INFERENCE for owner
awareness. Nothing was modified.
