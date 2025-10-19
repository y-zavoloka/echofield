from __future__ import annotations

from echofield.settings.config import cfg

LANGUAGE_CODE = cfg.LANGUAGE_CODE
TIME_ZONE = cfg.TIME_ZONE
USE_I18N = cfg.USE_I18N
USE_TZ = cfg.USE_TZ

MODELTRANSLATION_DEFAULT_LANGUAGE = "en"
MODELTRANSLATION_FALLBACK_LANGUAGES: tuple[str, ...] = ("en", "uk")
MODELTRANSLATION_LANGUAGES: tuple[str, ...] = ("en", "uk")

__all__ = [
    "LANGUAGE_CODE",
    "TIME_ZONE",
    "USE_I18N",
    "USE_TZ",
    "MODELTRANSLATION_DEFAULT_LANGUAGE",
    "MODELTRANSLATION_FALLBACK_LANGUAGES",
    "MODELTRANSLATION_LANGUAGES",
]
