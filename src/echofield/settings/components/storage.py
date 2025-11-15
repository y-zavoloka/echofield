# src/echofield/settings/components/storage.py
from __future__ import annotations

from echofield.settings.components.base import BASE_DIR
from echofield.settings.config import cfg


def _build_storage() -> tuple[dict[str, object], str, str]:
    if cfg.USE_R2_STATIC:
        cdn = cfg.R2_CUSTOM_DOMAIN or "static.echofield.dev"
        storages: dict[str, object] = {
            "staticfiles": {
                "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
            },
            "default": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"},
        }
        return storages, f"https://{cdn}/static/", f"https://{cdn}/media/"
    storages = {
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    }
    return storages, "/static/", "/media/"


STORAGES, STATIC_URL, MEDIA_URL = _build_storage()

# File-system roots for local static and media when not using R2.
# These are still required by Django even if static/media are served via R2.
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "media"

MARKDOWNX_MEDIA_PATH = "uploads/%Y/%m/"

__all__ = [
    "STORAGES",
    "STATIC_URL",
    "MEDIA_URL",
    "STATIC_ROOT",
    "MEDIA_ROOT",
    "MARKDOWNX_MEDIA_PATH",
]
