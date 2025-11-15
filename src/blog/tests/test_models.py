from __future__ import annotations

from datetime import timedelta

import pytest
from django.utils import timezone

from blog.models import Post


@pytest.mark.django_db
def test_post_public_published_filters_by_date_only() -> None:
    now = timezone.now()

    # Published in the past -> should be included, regardless of status
    past_published = Post.objects.create(
        title="Past published",
        slug="past-published",
        content="",
        status=Post.Status.DRAFT,
        published_at=now - timedelta(days=1),
    )

    # Published in the future -> should NOT be included
    Post.objects.create(
        title="Future published",
        slug="future-published",
        content="",
        status=Post.Status.PUBLISHED,
        published_at=now + timedelta(days=1),
    )

    # No publication date -> should NOT be included
    Post.objects.create(
        title="No date",
        slug="no-date",
        content="",
        status=Post.Status.PUBLISHED,
        published_at=None,
    )

    qs = Post.public.published()
    assert list(qs) == [past_published]


@pytest.mark.django_db
def test_post_public_for_slug_supports_language_specific_and_fallback() -> None:
    now = timezone.now()

    post = Post.objects.create(
        title="Localized post",
        slug="base-slug",
        content="",
        status=Post.Status.PUBLISHED,
        published_at=now - timedelta(days=1),
    )
    # Modeltranslation adds slug_en/slug_uk fields at runtime; assign them directly.
    setattr(post, "slug_en", "hello-en")
    setattr(post, "slug_uk", "hello-uk")
    post.save()

    # Language-specific lookup
    qs_en = Post.public.for_slug("hello-en", lang="en")
    assert qs_en.get() == post

    # Fallback lookup across all slug fields
    qs_any = Post.public.for_slug("hello-uk")
    assert qs_any.get() == post
