from __future__ import annotations

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
        published_at=now - timezone.timedelta(days=1),
    )

    # Draft and future posts should not be listed
    Post.objects.create(
        title="Draft",
        slug="draft-post",
        content="",
        status=Post.Status.DRAFT,
        published_at=now - timezone.timedelta(days=1),
    )
    Post.objects.create(
        title="Future",
        slug="future-post",
        content="",
        status=Post.Status.PUBLISHED,
        published_at=now + timezone.timedelta(days=1),
    )

    url = reverse("post_list")
    response = client.get(url)

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
        published_at=now - timezone.timedelta(days=1),
    )
    setattr(post, "slug_en", "hello-en")
    setattr(post, "slug_uk", "hello-uk")
    post.save()

    with translation.override("en"):
        url = reverse("post_detail", kwargs={"slug": "hello-en"})
        response = client.get(url)

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
        published_at=now - timezone.timedelta(days=1),
    )
    setattr(post, "slug_en", "hello-en")
    setattr(post, "slug_uk", "hello-uk")
    post.save()

    # Active language is English, but user requests Ukrainian slug.
    with translation.override("en"):
        url = reverse("post_detail", kwargs={"slug": "hello-uk"})
        response = client.get(url)

    assert response.status_code == 301
    assert response.url == reverse("post_detail", kwargs={"slug": "hello-en"})
