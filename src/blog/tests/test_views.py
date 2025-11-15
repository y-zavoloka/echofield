from __future__ import annotations

from datetime import timedelta

import pytest
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone, translation

from blog.models import Post


@pytest.mark.django_db
def test_post_list_view_shows_only_published_posts(client: Client) -> None:
    now = timezone.now()

    Post.objects.create(
        title="Visible post",
        slug="visible-post",
        content="",
        status=Post.Status.PUBLISHED,
        published_at=now - timedelta(days=1),
    )

    # Draft and future posts should not be listed
    Post.objects.create(
        title="Draft",
        slug="draft-post",
        content="",
        status=Post.Status.DRAFT,
        published_at=now - timedelta(days=1),
    )
    Post.objects.create(
        title="Future",
        slug="future-post",
        content="",
        status=Post.Status.PUBLISHED,
        published_at=now + timedelta(days=1),
    )

    url = reverse("post_list")
    # Use secure requests so tests pass regardless of SECURE_SSL_REDIRECT.
    response = client.get(url, secure=True)

    assert response.status_code == 200
    posts = list(response.context["posts"])

    # Only posts with PUBLISHED status should appear, regardless of published_at.
    assert {p.slug for p in posts} == {"visible-post", "future-post"}


@pytest.mark.django_db
def test_post_detail_view_uses_canonical_slug_for_current_language(
    client: Client,
) -> None:
    now = timezone.now()

    post = Post.objects.create(
        title="Localized post",
        slug="base-slug",
        content="",
        status=Post.Status.PUBLISHED,
        published_at=now - timedelta(days=1),
    )
    setattr(post, "slug_en", "hello-en")
    setattr(post, "slug_uk", "hello-uk")
    post.save()

    with translation.override("en"):
        url = reverse("post_detail", kwargs={"slug": "hello-en"})
        # Use secure request to avoid SSL upgrade redirects in tests.
        response = client.get(url, secure=True)

    assert response.status_code == 200
    assert response.context["post"].pk == post.pk


@pytest.mark.django_db
def test_post_detail_view_redirects_cross_language_slug_to_current_language(
    client: Client,
) -> None:
    now = timezone.now()

    post = Post.objects.create(
        title="Localized post",
        slug="base-slug",
        content="",
        status=Post.Status.PUBLISHED,
        published_at=now - timedelta(days=1),
    )
    setattr(post, "slug_en", "hello-en")
    setattr(post, "slug_uk", "hello-uk")
    post.save()

    # Active language is English, but user requests Ukrainian slug.
    with translation.override("en"):
        url = reverse("post_detail", kwargs={"slug": "hello-uk"})
        # Secure request so any SSL redirect does not mask our cross-language redirect.
        response = client.get(url, secure=True)

    assert response.status_code == 301
    # Compare only the path component to avoid scheme/host differences.
    assert response.headers["Location"].endswith(
        reverse("post_detail", kwargs={"slug": "hello-en"})
    )
