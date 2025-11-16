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

# File-system roots for local static and media.
# We keep them at the project root so they are available at /app/static and /app/media
# inside the Docker container, matching the nginx aliases.
STATIC_ROOT = BASE_DIR.parent.parent / "static"
MEDIA_ROOT = BASE_DIR.parent.parent / "media"

MARKDOWNX_MEDIA_PATH = "uploads/%Y/%m/"

__all__ = [
    "STORAGES",
    "STATIC_URL",
    "MEDIA_URL",
    "STATIC_ROOT",
    "MEDIA_ROOT",
    "MARKDOWNX_MEDIA_PATH",
]
