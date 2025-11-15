# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project overview

This repository contains a Django 5.2 project called `echofield`, structured as a blog-style site with bilingual content (English and Ukrainian) and Cloudflare R2-backed static/media storage in production.

Key characteristics:
- Source lives under `src/` with the Django project in `src/echofield` and the main app in `src/blog`.
- Settings are split into modules under `src/echofield/settings/` (`settings.py`, `db.py`, `auth.py`, `installed_apps.py`, `storage.py`) and re-exported via `echofield.settings`.
- Internationalization is handled via `django-modeltranslation` (`blog/translation.py`) and Django i18n URL patterns.
- Static/media storage is switchable between local filesystem and Cloudflare R2 via environment variables.
- Deployment uses a single `Dockerfile` at the repo root; GitHub Actions builds and pushes an image to GHCR and deploys via SSH to a remote host.

When adding or modifying features, assume a standard Django MVC pattern with class-based views, models, and templates.

## Code architecture

### Django project layout

- `src/manage.py` is the entrypoint for Django management commands and sets `DJANGO_SETTINGS_MODULE=echofield.settings`.
- `src/echofield/settings/`:
  - `settings.py` defines core Django settings and imports from modular files:
    - `installed_apps.py` groups `DJANGO_APPS`, third-party apps (`storages`, `modeltranslation`, `markdownx`, `unfold`), and project apps (`blog`) into `INSTALLED_APPS`.
    - `db.py` configures `DATABASES` from `DATABASE_URL` (via `dj-database-url`) or falls back to SQLite at `BASE_DIR / "db.sqlite3"` for local development.
    - `auth.py` contains standard `AUTH_PASSWORD_VALIDATORS`.
    - `storage.py` configures either local filesystem storage (development) or `django-storages` S3 backend targeting Cloudflare R2, controlled by `USE_R2_STATIC` and related R2 env vars.
  - `__init__.py` re-exports from `settings.py` so external references can use `echofield.settings`.
- URL routing (`src/echofield/urls.py`):
  - Registers `admin/`, `markdownx/`, and mounts the `blog` app at the root path.
  - Adds `i18n/` patterns via `django.conf.urls.i18n`.

### Blog app

- Models (`src/blog/models/posts.py`):
  - `Post` model with translated fields (`title`, `content`, `slug` via `modeltranslation`), status (`draft`/`published`), and `published_at` / `created_at` / `updated_at` timestamps.
- Translations (`src/blog/translation.py`):
  - Registers `PostTranslationOptions` so `modeltranslation` manages `title_en`, `title_uk`, `content_en`, etc.
- Views (`src/blog/views/posts.py`):
  - `PostListView` lists published posts ordered by `published_at` then `created_at`.
  - `PostDetailView` shows a single published post by slug and includes fallback logic:
    - If the requested slug is not found in the current language, it looks up by `slug_en`/`slug_uk` and redirects to the slug for the active language.
- URLs (`src/blog/urls.py`):
  - Root `""` path for the post list and `"<slug:slug>/"` for individual post detail.

Templates are expected to live in standard Django app template locations (e.g. `blog/templates/`) and are not exhaustively documented here.

### Storage & deployment

- `storage.py` decides between local and R2-backed storage:
  - Local dev: `STATIC_URL=/static/`, `MEDIA_URL=/media/`, with `STATIC_ROOT`/`MEDIA_ROOT` under `src/echofield/`.
  - R2: uses `django-storages` `S3Storage` and environment variables (`R2_BUCKET`, `R2_ENDPOINT`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_CUSTOM_DOMAIN`, `USE_R2_STATIC`, `AWS_S3_REGION_NAME`) to configure static and media URLs.
- Security-related settings (SSL redirect, HSTS, secure cookies) are toggled via `USE_SSL`.
- `.github/workflows/deploy.yml` builds and pushes a Docker image and then deploys via SSH to a remote server, generating a `.env` file there and starting the app with `docker compose`.

Note: The root `docker-compose.yml` currently references `build: ./app`, which does not match the present layout (`src/` and `Dockerfile` at the repo root); treat it as outdated unless it is updated.

## Environment & configuration

Django settings are driven heavily by environment variables:

- `.env` is loaded via `python-dotenv` in `settings.py` (`load_dotenv(BASE_DIR / '..'/'.env')`).
- Important toggles and config points for local work:
  - `SECRET_KEY`: required by Django; must be set in `.env`.
  - `DEBUG`: string flag (`"True"` or `"False"`).
  - `ALLOWED_HOSTS`: comma-separated list of hosts.
  - `DATABASE_URL`: if set, used to configure the default database; otherwise SQLite is used.
  - `USE_R2_STATIC`, `R2_BUCKET`, `R2_ENDPOINT`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_CUSTOM_DOMAIN`, `AWS_S3_REGION_NAME`: control static/media storage via Cloudflare R2.
  - `USE_SSL`: enables SSL-related security settings when set to a truthy value.

When running locally, you can omit the R2-related variables and let the project fall back to local static/media storage; ensure `SECRET_KEY` and either `DATABASE_URL` or the default SQLite database are available.

## Common commands

Assume you are at the repository root (`/home/eugene/Projects/echo/echofield`).

### Python environment & dependencies

Create a virtual environment and install dependencies using `requirements.txt` (generated from `pyproject.toml` via `uv pip compile`):

```bash path=null start=null
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If you need the development tools defined in `pyproject.toml` (`black`, `ruff`, `django-environ`), install them explicitly (or use `uv` with the `dev` dependency group if available in your environment).

### Running the development server

From the repo root, use the `manage.py` under `src/`:

```bash path=null start=null
source .venv/bin/activate
python src/manage.py migrate
python src/manage.py runserver 0.0.0.0:8000
```

### Tests

Run the full Django test suite:

```bash path=null start=null
source .venv/bin/activate
python src/manage.py test
```

Run a single test module or test case (replace with the actual module/class once tests are added under `blog/tests.py` or similar):

```bash path=null start=null
source .venv/bin/activate
python src/manage.py test blog.tests
```

### Linting & formatting

The project uses `ruff` and `black` as development dependencies:

- Run Ruff (lint only):

```bash path=null start=null
source .venv/bin/activate
ruff check src
```

- Run Black (code formatting):

```bash path=null start=null
source .venv/bin/activate
black src
```

## Notes for future Warp agents

- Treat `echofield.settings` as the central settings module; if you add new settings submodules, ensure they are imported from `settings.py` and thus exposed via `echofield.settings`.
- Maintain the separation between configuration (environment-driven values in settings modules) and application logic (models, views, templates) to keep deployments predictable across local/dev/prod.
- For features involving content or URL structure, consider the bilingual behavior implemented in `PostDetailView` and `modeltranslation` when introducing new user-facing text or slugs.
