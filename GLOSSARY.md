# Glossary — django-autoload

> Terms as used in this repository. Documentation only.

| Term | Meaning (FACT unless noted) |
| ---- | --------------------------- |
| **App marker** | Filename whose presence marks a directory as a Django app package (default `apps.py`; `AUTOLOAD["APP_MARKER"]`). |
| **Scan root** | A directory (relative to BASE_DIR) that discovery walks. Empty `ROOTS` → scan BASE_DIR itself. |
| **BASE_DIR** | Project root for resolution. `AUTOLOAD["BASE_DIR"]`, else `settings.BASE_DIR`, else `Path.cwd()`. |
| **Dotted path** | Importable module path (e.g. `apps.blog.signals`) derived from a filesystem path relative to BASE_DIR (`conf.dotted_path`). |
| **Component** | A per-app module/package imported at `ready()` (e.g. `signals`, `receivers`); listed in `AUTOLOAD["COMPONENTS"]`. |
| **URL pattern name** | Logical key in `AUTOLOAD["URL_PATTERNS"]` mapping a name to a relative urls file used by `autodiscover_urls(name)`. |
| **Settings fragment** | A settings module whose UPPER_CASE names are merged by `load_settings()` / `discover_app_settings()`. |
| **Extra** | Optional install target pulling a third-party integration: `[drf]`, `[celery]`, `[rq]`, `[django-rq]`, `[dev]`, `[test]`. |
| **`AutoloadConfig`** | The library's `AppConfig`; its `ready()` registers the system check and loads components. |
| **`check_autoload`** | Registered Django system check that fails loudly on bad `AUTOLOAD` config. |
| **fastapi-autoload** | Sibling project (chrysa) stated to be a FastAPI port of this Django library; not referenced in-repo (see DECISIONS.md ADR-009). |
