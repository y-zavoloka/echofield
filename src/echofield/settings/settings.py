from pathlib import Path
from dotenv import load_dotenv, dotenv_values
import os


BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / '..'/'.env')

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")


# Application definition

from .installed_apps import *

# Modeltranslation
MODELTRANSLATION_DEFAULT_LANGUAGE = "en"
MODELTRANSLATION_FALLBACK_LANGUAGES = ("en", "uk")
MODELTRANSLATION_LANGUAGES = ("en", "uk")

# Middleware
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

ROOT_URLCONF = "echofield.urls"

LOCALE_PATHS = [BASE_DIR / "locale"]

# Templates
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

# WSGI application
WSGI_APPLICATION = "echofield.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

from .db import *

# Authentication
from .auth import *

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Kyiv"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

from .storage import *


# Security
use_ssl = os.environ.get("USE_SSL", "False") == "True"
if use_ssl:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = 31536000 if not use_ssl else 0
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = "DENY"
else:
    SECURE_SSL_REDIRECT = False
    SECURE_PROXY_SSL_HEADER = None


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
