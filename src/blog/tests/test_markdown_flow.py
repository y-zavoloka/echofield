from __future__ import annotations

from datetime import timedelta

import pytest
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone, translation

from blog.models import Post


@pytest.mark.django_db
def test_markdown_roundtrip_model_and_view(client: Client) -> None:
    """Full roundtrip: store Markdown, then read back rendered HTML.

    - On write: both English and Ukrainian Markdown variants are stored
      in the translated content fields.
    - On read: the model-level `content_html` property renders Markdown to HTML
      for the active language, and the public detail view returns that HTML
      to the client.
    """

    now = timezone.now() - timedelta(days=1)

    markdown_en = "# Hello EN\n\nThis is **bold**."
    markdown_uk = "# Привіт UA\n\nЦе **жирний** текст."

    post = Post.objects.create(
        title="Localized markdown",
        slug="localized-markdown",
        published_at=now,
    )

    # Assign localized slugs and Markdown content using modeltranslation fields.
    setattr(post, "slug_en", "localized-markdown-en")
    setattr(post, "slug_uk", "localized-markdown-uk")
    setattr(post, "content_en", markdown_en)
    setattr(post, "content_uk", markdown_uk)
    post.save()

    # --- DB layer: raw Markdown is stored as-is ---
    stored = Post.objects.get(pk=post.pk)
    assert getattr(stored, "content_en") == markdown_en
    assert getattr(stored, "content_uk") == markdown_uk

    # --- Model layer: content_html renders Markdown per-language ---
    with translation.override("en"):
        post_en = Post.objects.get(pk=post.pk)
        html_en = post_en.content_html
        assert "Hello EN" in html_en
        assert "<strong>" in html_en  # markdown emphasis rendered

    with translation.override("uk"):
        post_uk = Post.objects.get(pk=post.pk)
        html_uk = post_uk.content_html
        assert "Привіт UA" in html_uk
        assert "<strong>" in html_uk

    # --- View layer: public detail view returns rendered HTML ---
    with translation.override("en"):
        url_en = reverse("post_detail", kwargs={"slug": "localized-markdown-en"})
        # Use secure request to avoid SSL-related redirects in tests.
        resp_en = client.get(url_en, secure=True, HTTP_ACCEPT_LANGUAGE="en")
    assert resp_en.status_code == 200
    body_en = resp_en.content.decode()
    assert "Hello EN" in body_en
    assert "<strong>" in body_en

    with translation.override("uk"):
        url_uk = reverse("post_detail", kwargs={"slug": "localized-markdown-uk"})
        resp_uk = client.get(url_uk, secure=True, HTTP_ACCEPT_LANGUAGE="uk")
    assert resp_uk.status_code == 200
    body_uk = resp_uk.content.decode()
    assert "Привіт UA" in body_uk
    assert "<strong>" in body_uk
