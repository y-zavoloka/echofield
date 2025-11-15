from __future__ import annotations

from django.utils.translation import gettext_lazy as _

from echofield.settings.config import cfg

LANGUAGE_CODE = cfg.LANGUAGE_CODE
TIME_ZONE = cfg.TIME_ZONE
USE_I18N = cfg.USE_I18N
USE_TZ = cfg.USE_TZ

# Restrict available languages to English and Ukrainian.
LANGUAGES: tuple[tuple[str, str], ...] = (
    ("en", _("English")),
    ("uk", _("Ukrainian")),
)

MODELTRANSLATION_DEFAULT_LANGUAGE = "en"
MODELTRANSLATION_FALLBACK_LANGUAGES: tuple[str, ...] = ("en", "uk")
MODELTRANSLATION_LANGUAGES: tuple[str, ...] = ("en", "uk")

__all__ = [
    "LANGUAGE_CODE",
    "TIME_ZONE",
    "USE_I18N",
    "USE_TZ",
    "LANGUAGES",
    "MODELTRANSLATION_DEFAULT_LANGUAGE",
    "MODELTRANSLATION_FALLBACK_LANGUAGES",
    "MODELTRANSLATION_LANGUAGES",
]
