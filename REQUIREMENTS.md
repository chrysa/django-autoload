# Requirements — django-autoload

> IDs are stable (`REQ-<AREA>-00x`). "Implemented" is marked only where a
> concrete code symbol verifies it. Evidence points to files in this repo.
> Documentation only.

## Functional

| ID            | Requirement                                                        | Status      | Evidence |
| ------------- | ------------------------------------------------------------------ | ----------- | -------- |
| REQ-DISC-001  | Discover app packages under scan roots by marker filename          | IMPLEMENTED | `discovery.py` `discover_app_markers`, `discover_apps` |
| REQ-DISC-002  | Return app list for `INSTALLED_APPS`                               | IMPLEMENTED | `discovery.py` `discover_apps` |
| REQ-DISC-003  | Append discovered apps into an existing list in place, de-duped    | IMPLEMENTED | `discovery.py` `autoload_into` |
| REQ-DISC-004  | Work with no `AUTOLOAD` setting (scan `BASE_DIR`)                  | IMPLEMENTED | `conf.py` `DEFAULTS`/`_settings_autoload`, `get_roots` |
| REQ-URL-001   | Discover `include()` URL patterns by logical name                  | IMPLEMENTED | `urls.py` `autodiscover_urls` |
| REQ-URL-002   | Unknown URL name yields empty list (composable)                    | IMPLEMENTED | `urls.py` `autodiscover_urls` |
| REQ-SET-001   | Merge UPPER_CASE settings from every module in `SETTINGS_DIRS`      | IMPLEMENTED | `settings.py` `load_settings` |
| REQ-SET-002   | Merge per-app settings module under scan roots                     | IMPLEMENTED | `settings.py` `discover_app_settings` |
| REQ-SET-003   | Inject a settings mapping onto a module at runtime                  | IMPLEMENTED | `settings.py` `apply_settings` |
| REQ-CMP-001   | Import configured per-app components at `ready()`                   | IMPLEMENTED | `components.py` `discover_components`, `apps.py` `ready` |
| REQ-CHK-001   | Register Django system check that fails loudly on bad config        | IMPLEMENTED | `checks.py` `check_autoload`, `apps.py` `ready` |
| REQ-DRF-001   | Aggregate per-app DRF routers into one `DefaultRouter` (extra)      | IMPLEMENTED | `routers.py` `autodiscover_routers` |
| REQ-CEL-001   | Point Celery at discovered apps (extra)                            | IMPLEMENTED | `tasks.py` `autodiscover_tasks` |
| REQ-RQ-001    | Import each app's jobs module so `@job` decorators run (extra)      | IMPLEMENTED | `jobs.py` `autodiscover_jobs` |
| REQ-VER-001   | Expose `__version__` from installed package metadata               | IMPLEMENTED | `__init__.py` (`importlib.metadata.version`) |

## Non-functional

| ID            | Requirement                                                        | Status      | Evidence |
| ------------- | ------------------------------------------------------------------ | ----------- | -------- |
| REQ-NFR-001   | No runtime dependency beyond Django (`>=4.2`)                       | IMPLEMENTED | `pyproject.toml` `dependencies` |
| REQ-NFR-002   | Python `>=3.14`                                                    | IMPLEMENTED | `pyproject.toml` `requires-python` |
| REQ-NFR-003   | No mandatory project layout                                        | IMPLEMENTED | `conf.py` `DEFAULTS` (`ROOTS=[]`), `__init__.py` docstring |
| REQ-NFR-004   | Full type annotations on public API; `mypy --strict`; `py.typed`   | STATED      | `CLAUDE.md` (claim); `py.typed` presence UNKNOWN from this pass |
| REQ-NFR-005   | Coverage gate ≥ 85%                                                | IMPLEMENTED | `pyproject.toml` `--cov-fail-under=85` |
| REQ-NFR-006   | Deterministic discovery (sorted globs, de-dup)                     | IMPLEMENTED | `sorted(...)` + `seen` sets across `urls.py`/`settings.py`/`routers.py`/`jobs.py` |
| REQ-NFR-007   | Safe to call while settings still being built                      | IMPLEMENTED | `conf.py` `_settings_autoload` (`settings.configured` guard) |

UNKNOWN: no explicit performance/latency budget is stated in the repo.
