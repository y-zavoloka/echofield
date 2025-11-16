"""
Collect settings from components without using 'import *'.
Export only UPPER_CASE variables from each module; order matters.
"""

from __future__ import annotations

import os
from importlib import import_module

from echofield.settings.config import (
    cfg,
)  # Available as cfg if needed in components

_MODULES: tuple[str, ...] = (
    "echofield.settings.components.base",
    "echofield.settings.components.apps",
    "echofield.settings.components.i18n",
    "echofield.settings.components.database",
    "echofield.settings.components.storage",
    "echofield.settings.components.security",
)

_ENV = os.getenv("DJANGO_ENV")  # e.g.: "local" or "production"
if _ENV:
    _MODULES += (f"echofield.settings.environments.{_ENV}",)


def _export_from(modname: str) -> None:
    """
    Import a module and export all UPPER_CASE attributes to the global namespace.

    Args:
        modname: The fully qualified module name to import from.
    """
    m = import_module(modname)
    for name in dir(m):
        if name.isupper():
            globals()[name] = getattr(m, name)


# Import settings from all configured modules
for _m in _MODULES:
    try:
        _export_from(_m)
    except ModuleNotFoundError:
        # Allow missing environment-specific modules
        pass

# Base constants from cfg that don't live in components
SECRET_KEY = cfg.SECRET_KEY.get_secret_value()
DEBUG = cfg.DEBUG


def _split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


ALLOWED_HOSTS = _split_csv(cfg.ALLOWED_HOSTS)
CSRF_TRUSTED_ORIGINS = _split_csv(cfg.CSRF_TRUSTED_ORIGINS)

# Clean up private names (but keep import_module as it's used in _export_from)
del _export_from, _MODULES, _m, _ENV, _split_csv
