"""
Static and media storage settings for Echofield.
Supports both local staticfiles and Cloudflare R2 (S3-compatible).
"""

import os

USE_R2 = os.environ.get("USE_R2_STATIC", "False").lower() == "true"

if USE_R2:
    # === Cloudflare R2 config ===
    # AWS S3 settings for R2
    AWS_STORAGE_BUCKET_NAME = os.environ["R2_BUCKET"]
    AWS_S3_ENDPOINT_URL = os.environ["R2_ENDPOINT"]
    AWS_ACCESS_KEY_ID = os.environ["R2_ACCESS_KEY_ID"]
    AWS_SECRET_ACCESS_KEY = os.environ["R2_SECRET_ACCESS_KEY"]

    # R2-specific settings
    AWS_DEFAULT_ACL = None
    AWS_S3_REGION_NAME = "auto"
    AWS_S3_ADDRESSING_STYLE = "virtual"
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_FILE_OVERWRITE = False

    # Custom domain for R2 (e.g. echofield-static.<accountid>.r2.cloudflarestorage.com)
    endpoint_domain = AWS_S3_ENDPOINT_URL.replace("https://", "").rstrip("/")
    AWS_S3_CUSTOM_DOMAIN = os.environ["R2_CUSTOM_DOMAIN"]

    # Static files configuration
    AWS_STATIC_LOCATION = "static"
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_STATIC_LOCATION}/"

    # Media files configuration
    AWS_MEDIA_LOCATION = "media"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_MEDIA_LOCATION}/"

    # Cache control headers
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=31536000, public",
    }

    # Modern Django 4.2+ storage configuration
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                "bucket_name": AWS_STORAGE_BUCKET_NAME,
                "endpoint_url": AWS_S3_ENDPOINT_URL,
                "access_key": AWS_ACCESS_KEY_ID,
                "secret_key": AWS_SECRET_ACCESS_KEY,
                "default_acl": AWS_DEFAULT_ACL,
                "region_name": AWS_S3_REGION_NAME,
                "addressing_style": AWS_S3_ADDRESSING_STYLE,
                "querystring_auth": AWS_QUERYSTRING_AUTH,
                "file_overwrite": AWS_S3_FILE_OVERWRITE,
                "custom_domain": AWS_S3_CUSTOM_DOMAIN,
                "location": AWS_MEDIA_LOCATION,
                "object_parameters": AWS_S3_OBJECT_PARAMETERS,
            },
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                "bucket_name": AWS_STORAGE_BUCKET_NAME,
                "endpoint_url": AWS_S3_ENDPOINT_URL,
                "access_key": AWS_ACCESS_KEY_ID,
                "secret_key": AWS_SECRET_ACCESS_KEY,
                "default_acl": AWS_DEFAULT_ACL,
                "region_name": AWS_S3_REGION_NAME,
                "addressing_style": AWS_S3_ADDRESSING_STYLE,
                "querystring_auth": AWS_QUERYSTRING_AUTH,
                "file_overwrite": AWS_S3_FILE_OVERWRITE,
                "custom_domain": AWS_S3_CUSTOM_DOMAIN,
                "location": AWS_STATIC_LOCATION,
                "object_parameters": AWS_S3_OBJECT_PARAMETERS,
            },
        },
    }

else:
    # === Local static & media for dev / fallback ===
    from pathlib import Path
    BASE_DIR = Path(__file__).resolve().parent.parent

    STATIC_URL = "/static/"
    MEDIA_URL = "/media/"
    STATIC_ROOT = BASE_DIR / "staticfiles"
    MEDIA_ROOT = BASE_DIR / "mediafiles"

    # Modern Django 4.2+ storage configuration for local files
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
            "OPTIONS": {
                "location": MEDIA_ROOT,
                "base_url": MEDIA_URL,
            },
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
            "OPTIONS": {
                "location": STATIC_ROOT,
                "base_url": STATIC_URL,
            },
        },
    }
