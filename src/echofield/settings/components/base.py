from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]

ROOT_URLCONF = "echofield.urls"
WSGI_APPLICATION = "echofield.wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

__all__ = [
    "BASE_DIR",
    "ROOT_URLCONF",
    "WSGI_APPLICATION",
    "DEFAULT_AUTO_FIELD",
    "MIDDLEWARE",
    "TEMPLATES",
]
