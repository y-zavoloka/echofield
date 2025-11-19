from __future__ import annotations

from typing import Mapping
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from django.conf import settings
from django.http import HttpRequest
from django.utils.translation import get_language


def _with_lang_param(url: str, lang: str) -> str:
    parts = urlparse(url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query["lang"] = lang
    new_query = urlencode(query, doseq=True)
    return urlunparse(parts._replace(query=new_query))


def build_canonical_url(
    request: HttpRequest, path: str | None = None, lang: str | None = None
) -> str:
    """Return an absolute canonical URL for the current language."""
    lang = lang or get_language() or settings.LANGUAGE_CODE
    base = request.build_absolute_uri(path)
    return _with_lang_param(base, lang)


def build_alternate_links(
    request: HttpRequest,
    per_language_paths: Mapping[str, str] | None = None,
) -> list[dict[str, str]]:
    """Return hreflang link data for all configured languages."""
    alternates: list[dict[str, str]] = []
    for lang, _ in settings.LANGUAGES:
        if per_language_paths and lang in per_language_paths:
            url = request.build_absolute_uri(per_language_paths[lang])
        else:
            url = request.build_absolute_uri()
        alternates.append({"lang": lang, "url": _with_lang_param(url, lang)})
    return alternates


__all__ = ["build_canonical_url", "build_alternate_links"]
