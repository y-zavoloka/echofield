# EchoField

[![Better Stack Badge](https://uptime.betterstack.com/status-badges/v2/monitor/29lca.svg)](https://uptime.betterstack.com/?utm_source=status_badge)

> A fast, bilingual (uk/en) personal blog and public notebook — built for clarity, speed, and long-term maintainability.

EchoField is a Django-based publishing platform engineered for **human-first content**, **server-rendered speed**, and **timeless maintainability**.
This project is a living platform: part blog, part knowledge base, part digital garden.

---

### ✨ Features

- **Zero/minimal JavaScript** — crisp, accessible, fast-loading pages
- **Bilingual content** (uk/en) & locale-aware SEO-friendly routing
- **Localized categories** — posts can belong to multiple translated taxonomies
- **Markdown-native editor** with live preview in Django admin
- **Automatic media optimization** — featured images get WebP 1×/2× variants + `<picture>` tags
- **SEO-ready by default** — canonical URLs, hreflang, Open Graph/Twitter cards, sitemap, robots.txt, and Article schema JSON-LD
- **Cloudflare R2** object storage (static & media) + edge CDN
- **Automated CI/CD** (GitHub Actions → DigitalOcean)
- **Accessibility-first** HTML & semantic design
- **Lighthouse 100/100/100/100** target across categories

---

### 🧰 Tech Stack

- Django 5.x & PostgreSQL 15+/18
- Gunicorn + Nginx (Dockerized deployment)
- Cloudflare R2 storage for static/media
- Quality tooling: Ruff, pytest, pre-commit, managed via [uv](https://github.com/astral-sh/uv)

---

### 🚀 Local development

```bash
uv sync --group dev                # Install all development deps
uv run django-admin runserver      # Launch development server
uvx ruff check .                   # Lint & static code analysis
uvx pytest -q                      # Run test suite
```

---

### 🏷️ Taxonomy & categories

- Categories live in `blog.models.Category`, are localizable (`name_en`, `name_uk`, `slug_en`, `slug_uk`), and are editable in Django admin.
- The internal post editor exposes a multi-select so each article can belong to multiple categories; public templates show the translated pill list.
- Tests covering CRUD + rendering live in `src/blog/tests/test_models.py` and `src/blog/tests/test_views.py`.

### 🖼️ Media pipeline

- Featured images automatically generate WebP variants at 1× (1280px) and 2× (2048px) via Pillow in `blog.utils.images`.
- Variants are emitted to Cloudflare R2 alongside the original upload and wired into templates through `<picture>` + `srcset`.
- Old variants are cleaned up whenever an image is replaced or deleted, keeping storage tidy.

### 🔍 SEO & discovery

- Canonical URLs, hreflang alternates, meta/OG/Twitter tags, and structured data are centralized in `blog.utils.seo` + base templates.
- `/sitemap.xml` is powered by `django.contrib.sitemaps` with `PostSitemap`; `/robots.txt` advertises it.
- `Post.build_json_ld` produces Article schema JSON-LD so search engines can render rich cards.

### 🗃️ Deploy & migrations

- Containers now start via `docker/web-entrypoint.sh`, which runs `uv run python src/manage.py migrate --noinput` before Gunicorn launches.
- GitHub Actions deploys also call `docker compose … exec web uv run python src/manage.py migrate --noinput` to fail fast on schema drift.
- Manual command (local dev): `uv run python src/manage.py migrate`.

---

**Production ready**, hackable by design, with speed & clarity as core values.

For setup details and deployment, see [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md).
