# ---------- Base ----------
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_SYSTEM_PYTHON=1

WORKDIR /app

# Make src/ imports (like `echofield`) work without installing the project as a package
ENV PYTHONPATH=/app/src

# Install curl for fetching uv
RUN apt-get update && apt-get install -y curl ca-certificates && rm -rf /var/lib/apt/lists/*

# Install uv (replaces pip/venv/poetry)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Ensure uv (installed into /root/.local/bin) is on PATH
ENV PATH="/root/.local/bin:${PATH}"

# Copy only dependency files first
COPY pyproject.toml uv.lock* ./

# Sync dependencies (no venv, global within image)
RUN uv sync --no-dev

# ---------- Build ----------
FROM base AS build

# Copy project code
COPY . .

# NOTE: We no longer run collectstatic at build time; it is executed on the
# production host inside the running container so it can access R2 credentials.

# ---------- Runtime ----------
FROM base AS runtime

WORKDIR /app

# Copy project code (including collected static files) from build stage
COPY --from=build /app /app

# Expose Django port
EXPOSE 8000

CMD ["uv", "run", "gunicorn", "echofield.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
