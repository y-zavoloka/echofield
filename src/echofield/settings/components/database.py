from __future__ import annotations

import os

import dj_database_url

from echofield.settings.config import cfg


def _build_databases() -> dict[str, object]:
    """Build DATABASES setting from environment-aware config.

    Precedence:
    1. TEST_DATABASE_URL (explicit override, e.g. for local test runs)
    2. DATABASE_URL (single URL for primary database)
    3. Individual PostgreSQL settings with sensible defaults
    """

    # 1) Explicit test database override (useful for running tests against sqlite).
    test_database_url = os.getenv("TEST_DATABASE_URL")
    if test_database_url:
        return {"default": dj_database_url.parse(test_database_url, conn_max_age=0)}

    # 2) Standard DATABASE_URL configuration.
    if cfg.DATABASE_URL:
        return {"default": dj_database_url.parse(cfg.DATABASE_URL, conn_max_age=600)}

    # 3) Fallback to discrete PostgreSQL settings.
    return {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": cfg.DB_NAME or "echofield",
            "USER": cfg.DB_USER or "echouser",
            "PASSWORD": cfg.DB_PASSWORD or "",
            "HOST": cfg.DB_HOST,
            "PORT": str(cfg.DB_PORT),
        }
    }


DATABASES: dict[str, object] = _build_databases()
__all__ = ["DATABASES"]
