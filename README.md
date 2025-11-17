# EchoField

[![Better Stack Badge](https://uptime.betterstack.com/status-badges/v2/monitor/29lca.svg)](https://uptime.betterstack.com/?utm_source=status_badge)

> A fast, bilingual (uk/en) personal blog and public notebook — built for clarity, speed, and long-term maintainability.

EchoField is a Django-based publishing platform engineered for **human-first content**, **server-rendered speed**, and **timeless maintainability**.
This project is a living platform: part blog, part knowledge base, part digital garden.

---

### ✨ Features

- **Zero/minimal JavaScript** — crisp, accessible, fast-loading pages
- **Bilingual content** (uk/en) & locale-aware SEO-friendly routing
- **Markdown-native editor** with live preview in Django admin
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

**Production ready**, hackable by design, with speed & clarity as core values.

For setup details and deployment, see [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md).
