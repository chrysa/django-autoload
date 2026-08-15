# Deep-dive: `django-autoload`

**Repo:** `chrysa/django-autoload` (local `/home/anthony/Documents/perso/projects/chrysa/django-autoload`)
**Purpose (1 phrase):** A dependency-free, layout-agnostic Django library that auto-discovers apps, URL includes, settings fragments and per-app components (plus optional DRF-router / Celery-task / RQ-job discovery) so `INSTALLED_APPS`, `urlpatterns` and settings imports stop being hand-maintained.
**License:** MIT (permissive — this repo can copy from other permissive sources).

## Scope note

This is a small (~570 LOC) internal-flavoured library, but it sits squarely in a well-trodden
OSS space (Django settings-splitting + module autodiscovery). There are 4 genuinely relevant
references — all BSD-3 (permissive, copiable with attribution). No need to force 10; forcing
more would just list generic Django tutorials. The four below cover the two real mechanisms the
project implements: **(a) merging settings fragments** and **(b) autodiscovering modules across apps**.

Licence summary: **all four references are BSD-3-Clause = permissive/copiable** (keep the copyright
notice). None are copyleft/restrictive. Nothing here needs reimplementation for licence reasons.

---

## 1. wemake-services/django-split-settings — settings-fragment merge

- **owner/repo:** `wemake-services/django-split-settings` (formerly `sobolevn/…`)
- **stars:** ~1.2k
- **activity:** actively maintained (595+ commits, supports Django 4.2→6.0 as of 2026)
- **licence:** **BSD-3-Clause — PERMISSIVE, copiable** (retain copyright)
- **file/module of the pattern:** `split_settings/tools.py` → `include()` / `optional()`
- **mechanism:** Instead of importing settings modules, it **globs** a set of files and `exec()`s
  each compiled file into the **caller's `globals()` scope**, in order, so each later fragment sees
  and can mutate what earlier ones defined. Tracks `__included_files__` to avoid double-execution.
  This is the exact problem `django_autoload.load_settings()` / `apply_settings()` solve — but
  django-autoload merges only `UPPER_CASE` names from discovered dirs rather than exec-ing into
  the caller frame.
- **portable snippet (~15 lines, the core of `include`):**
  ```python
  import glob, os
  def include(*patterns, scope):
      conf_dir = os.path.dirname(scope["__file__"])
      seen = scope.setdefault("__included_files__", [])
      for pattern in patterns:
          for path in sorted(glob.glob(os.path.join(conf_dir, pattern))):
              path = os.path.abspath(path)
              if path in seen:
                  continue
              seen.append(path)
              with open(path, "rb") as fh:
                  exec(compile(fh.read(), path, "exec"), scope)  # noqa: S102
  ```
- **integration into django-autoload:** django-autoload deliberately does **not** exec into the
  caller frame (safer, testable — it returns a dict via `load_settings()`). Two things worth
  borrowing: (1) the **`optional()` marker** so a missing fragment is silently skipped vs a
  required one raising `OSError` — currently `SETTINGS_DIRS` has no "required vs optional"
  distinction; (2) **deterministic ordering** (`sorted(glob(...))`) so merge results are stable —
  verify `discover_app_settings()` sorts before merging (mirrors `discovery.py` which already
  `sorted(set(found))`).
- **gotchas:** `exec`-into-scope leaks *every* local of a fragment (functions, imports) into
  settings, and `sys._getframe(1).f_globals` is fragile under some import machinery — django-autoload's
  "return a filtered UPPER_CASE dict" approach is strictly better; keep it. Only lift the
  optional/required + ordering ideas, not the exec model.

## 2. django/django — `autodiscover_modules` / `import_string`

- **owner/repo:** `django/django`
- **stars:** ~85k
- **activity:** the framework itself — continuously maintained
- **licence:** **BSD-3-Clause — PERMISSIVE, copiable** (retain copyright/notice)
- **file/module of the pattern:** `django/utils/module_loading.py` →
  `autodiscover_modules(*module_names, register_to=None)`, `import_string()`, `cached_import()`
- **mechanism:** For every app in the registry it tries to `import_module(f"{app}.{name}")`; it
  **swallows `ModuleNotFoundError` only when the submodule genuinely doesn't exist** (re-checks via
  `module_has_submodule`) and **re-raises** if the module exists but fails to import — the critical
  subtlety that separates "app has no `tasks.py`" from "app's `tasks.py` has a bug". Also snapshots
  and **restores a registry's state** if a later import fails, to avoid half-registered state.
- **portable snippet (~12 lines, the safe-swallow core):**
  ```python
  from importlib import import_module
  from django.apps import apps
  from django.utils.module_loading import module_has_submodule

  def autodiscover(name):
      for config in apps.get_app_configs():
          try:
              import_module(f"{config.name}.{name}")
          except Exception:
              if module_has_submodule(config.module, name):
                  raise          # real error in an existing module -> surface it
              # else: app simply has no such submodule -> ignore
  ```
- **integration into django-autoload:** `components.py`, `jobs.py`, `tasks.py`, `routers.py` all
  import a per-app module by name — they should use **exactly this "re-raise if the submodule
  exists" guard**. A bare `except ImportError: pass` (or `contextlib.suppress(ImportError)`) will
  **silently hide a real bug** in an app's `signals.py`/`jobs.py`/`routers.py`, which is the #1
  autodiscovery footgun. Check each of those 4 modules: if any swallow ImportError blindly, replace
  with `module_has_submodule`-gated logic. Django is already a hard dependency, so
  `from django.utils.module_loading import autodiscover_modules, import_string` is free — prefer
  reusing Django's function over re-implementing where the app-registry is available.
- **gotchas:** `autodiscover_modules` needs the app **registry populated** (call it from
  `AppConfig.ready()`, which `apps.py` already does) — it won't work at settings-import time, which
  is precisely why django-autoload's *app* discovery is filesystem-glob based (pre-registry) while
  its *component* discovery is registry-based. Keep that split; document it.

## 3. jazzband/django-configurations — class-based settings composition

- **owner/repo:** `jazzband/django-configurations`
- **stars:** ~1.1k
- **activity:** maintained under Jazzband (512+ commits)
- **licence:** **BSD-3-Clause — PERMISSIVE, copiable**
- **file/module of the pattern:** `configurations/base.py` (the `Configuration` metaclass) +
  `configurations/importer.py` (import hook that materialises a class into a settings module)
- **mechanism:** Settings are a **class**; inheritance + `@property`/`classmethod` compute derived
  values, and an install hook turns the resolved class into the module `django.conf.settings` reads.
  It's the *opposite philosophy* to django-autoload (explicit OOP config vs zero-config discovery),
  which makes it a useful **contrast reference** rather than something to copy wholesale.
- **portable snippet (the "only UPPER_CASE names are settings" filter — same rule django-autoload
  needs when merging fragments):**
  ```python
  def public_settings(namespace: dict) -> dict:
      return {k: v for k, v in namespace.items() if k.isupper() and not k.startswith("_")}
  ```
- **integration into django-autoload:** Confirm `load_settings()`/`apply_settings()` apply the
  `k.isupper()` filter (Django's own convention) so helper functions/imports in a fragment don't
  leak into settings. Also worth stealing: django-configurations' pattern of a **single documented
  install entrypoint** — aligns with the chrysa "uniform `install()` entrypoint" Public-API rule.
- **gotchas:** Don't adopt its import-hook / `DJANGO_CONFIGURATION` env-var machinery — it's heavy
  and couples to a metaclass; django-autoload's value proposition is *no ceremony*. Cite it in
  README as "if you want explicit class-based config instead, use django-configurations" to frame
  the niche.

## 4. celery/celery — `autodiscover_tasks`

- **owner/repo:** `celery/celery`
- **stars:** ~26k
- **activity:** actively maintained (Celery 5.6.x, 2026)
- **licence:** **BSD-3-Clause — PERMISSIVE, copiable**
- **file/module of the pattern:** `celery/app/base.py` → `Celery.autodiscover_tasks(packages, related_name="tasks")`
- **mechanism:** Lazily (on worker/finalize) walks a **list of package names** and imports
  `f"{pkg}.{related_name}"` for each, swallowing absence. The canonical Django wiring is
  `app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)` — passing a **callable** so the package
  list is resolved *late* (after settings/registry are ready), not at import time.
- **portable snippet:**
  ```python
  # celery.py — django-autoload already exposes discover_apps() as the package source
  from django_autoload import discover_apps
  app.autodiscover_tasks(lambda: discover_apps())   # callable => lazy resolution
  ```
- **integration into django-autoload:** This is already the documented `[celery]` extra
  (`autodiscover_tasks(app)`). Key correctness point to verify in `tasks.py`: pass discovery as a
  **`lambda`/callable to Celery**, never an eagerly-evaluated list — otherwise apps discovered after
  the celery module imports are missed. Also note the **known Celery limitation**: `autodiscover_tasks`
  is non-recursive (only `<pkg>.tasks`, not `<pkg>.sub.tasks`); django-autoload's `[rq]`/`[django-rq]`
  `autodiscover_jobs()` exists precisely because RQ has no equivalent — document that asymmetry.
- **gotchas:** `related_name` defaults to `"tasks"`; if an app names its module differently the
  discovery misses it silently. Expose the module name as config (django-autoload already does this
  pattern via `COMPONENTS` / `APP_MARKER`) rather than hardcoding `"tasks.py"`.

---

## Cross-cutting takeaways for django-autoload

1. **The single most important pattern to adopt is Django's `module_has_submodule` re-raise guard**
   (ref #2) across `components.py`/`jobs.py`/`tasks.py`/`routers.py` — silently swallowing
   `ImportError` turns a real bug in an app module into an invisible no-op. This is the classic
   autodiscovery defect and the highest-value hardening here.
2. **Lazy/callable resolution** (refs #2, #4): registry-dependent discovery must run at
   `ready()`/finalize time, not import time. django-autoload already splits filesystem-glob app
   discovery (pre-registry) from registry-based component discovery — keep and document that seam.
3. **Determinism + UPPER_CASE filtering** for settings merge (refs #1, #3): sort globbed fragments
   and merge only `k.isupper()` names; add an `optional` vs `required` distinction for `SETTINGS_DIRS`.
4. **All references are BSD-3 (permissive)** — code/patterns are copiable with attribution; Django
   itself is already a dependency so prefer *reusing* `django.utils.module_loading` over re-implementing.
