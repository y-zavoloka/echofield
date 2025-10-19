from __future__ import annotations

import dj_database_url

from echofield.settings.config import cfg


def _build_databases() -> dict[str, object]:
    if cfg.DATABASE_URL:
        return {"default": dj_database_url.parse(cfg.DATABASE_URL, conn_max_age=600)}
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
