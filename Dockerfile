# ---------- Base ----------
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UV_SYSTEM_PYTHON=1

WORKDIR /app

# Install uv (replaces pip/venv/poetry)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy only dependency files first
COPY pyproject.toml uv.lock* ./

# Sync dependencies (no venv, global within image)
RUN uv sync --no-dev

# ---------- Build ----------
FROM base AS build

# Copy project code
COPY . .

# Collect static assets if needed
RUN uv run python manage.py collectstatic --noinput

# ---------- Runtime ----------
FROM python:3.11-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1

# Copy env + installed deps
COPY --from=build /root/.cache/uv /root/.cache/uv
COPY --from=build /app /app

# Expose Django port
EXPOSE 8000

CMD ["uv", "run", "gunicorn", "echofield.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
