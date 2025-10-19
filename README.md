# EchoField

> A fast, bilingual (uk/en) personal blog and public notebook — built for clarity, speed, and long-term maintainability.

EchoField is a Django-based publishing platform designed around **human-first content**, **server-rendered pages**, and **clean CSS** with almost no JavaScript.  
It’s a living project: part blog, part knowledge base, part digital garden.

---

### ✨ Features
- **Minimal JS, clean HTML/CSS** via Vite
- **Bilingual** content (uk/en) with locale-aware routing
- **Markdown-native editor** in Django admin
- **Static & media** via Cloudflare R2 + CDN
- **Automated CI/CD** (GitHub Actions → DigitalOcean)
- **Lighthouse 100/100/100/100** target

---

### 🧰 Tech stack
- Django 5 + PostgreSQL 18  
- Gunicorn + Nginx (Docker)  
- Cloudflare R2 storage  
- Ruff, pytest, pre-commit via uv  

---

### 🚀 Development
```bash
uv sync --group dev
uv run django-admin runserver
uvx ruff check .
uvx pytest -q
