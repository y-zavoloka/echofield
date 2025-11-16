# src/echofield/settings/components/storage.py
from __future__ import annotations

from echofield.settings.components.base import BASE_DIR
from echofield.settings.config import cfg


def _build_storage() -> tuple[dict[str, object], str, str]:
    """Build Django STORAGES config and URLs.

    When USE_R2_STATIC is enabled, both static and media files are served from
    the Cloudflare R2 bucket via django-storages S3 backend. Static files are
    stored under the "static/" prefix and media under "media/".

    Otherwise, everything stays on the local filesystem.
    """

    if cfg.USE_R2_STATIC:
        cdn = cfg.R2_CUSTOM_DOMAIN or "static.echofield.dev"

        # Map R2-specific settings to the AWS_* variables expected by
        # django-storages' S3Boto3Storage backend.
        global AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
        global AWS_STORAGE_BUCKET_NAME, AWS_S3_ENDPOINT_URL
        global AWS_S3_REGION_NAME, AWS_S3_CUSTOM_DOMAIN

        AWS_ACCESS_KEY_ID = cfg.R2_ACCESS_KEY_ID or ""
        AWS_SECRET_ACCESS_KEY = cfg.R2_SECRET_ACCESS_KEY or ""
        AWS_STORAGE_BUCKET_NAME = cfg.R2_BUCKET or ""
        AWS_S3_ENDPOINT_URL = cfg.R2_ENDPOINT or ""
        AWS_S3_REGION_NAME = getattr(cfg, "AWS_S3_REGION_NAME", "auto")
        AWS_S3_CUSTOM_DOMAIN = cfg.R2_CUSTOM_DOMAIN or None

        storages: dict[str, object] = {
            # Static files go to R2 under the "static/" prefix.
            "staticfiles": {
                "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
                "OPTIONS": {
                    "location": "static",
                },
            },
            # Default file storage (uploads) also goes to R2 under "media/".
            "default": {
                "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
                "OPTIONS": {
                    "location": "media",
                },
            },
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
