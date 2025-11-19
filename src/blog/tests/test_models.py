from __future__ import annotations

from datetime import timedelta
from io import BytesIO
from pathlib import Path
from urllib.parse import unquote

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from PIL import Image

from blog.models import Category, Post


@pytest.mark.django_db
def test_post_public_published_filters_by_date_only() -> None:
    now = timezone.now()

    # Published in the past -> should be included
    past_published = Post.objects.create(
        title="Past published",
        slug="past-published",
        content="",
        published_at=now - timedelta(days=1),
    )

    # Published in the future -> should NOT be published
    Post.objects.create(
        title="Future published",
        slug="future-published",
        content="",
        published_at=now + timedelta(days=1),
    )

    # No publication date -> should NOT be published
    Post.objects.create(
        title="No date",
        slug="no-date",
        content="",
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


@pytest.mark.django_db
def test_category_str_returns_name() -> None:
    category = Category.objects.create(name="Tech", slug="tech")
    assert str(category) == "Tech"


@pytest.mark.django_db
def test_post_can_attach_categories() -> None:
    category = Category.objects.create(name="News", slug="news")
    post = Post.objects.create(
        title="With category",
        slug="with-category",
        content="",
    )
    post.categories.add(category)
    assert category in post.categories.all()


def _make_test_image(
    name: str = "featured.jpg",
    size: tuple[int, int] = (1600, 900),
    color: tuple[int, int, int] = (220, 120, 80),
) -> SimpleUploadedFile:
    buffer = BytesIO()
    image = Image.new("RGB", size, color)
    image.save(buffer, format="JPEG")
    buffer.seek(0)
    return SimpleUploadedFile(name, buffer.read(), content_type="image/jpeg")


@pytest.mark.django_db
def test_post_generates_webp_variants(tmp_path, settings) -> None:
    settings.MEDIA_ROOT = tmp_path
    image = _make_test_image()
    post = Post.objects.create(
        title="Optimized",
        slug="optimized",
        content="",
        featured_image=image,
    )

    variant_1x = Path(settings.MEDIA_ROOT) / "posts/featured/featured@1x.webp"
    variant_2x = Path(settings.MEDIA_ROOT) / "posts/featured/featured@2x.webp"
    assert variant_1x.exists()
    assert variant_2x.exists()
    post.refresh_from_db()
    srcset = unquote(post.featured_image_webp_srcset)
    assert "@1x.webp 1x" in srcset
    assert "@2x.webp 2x" in srcset


@pytest.mark.django_db
def test_post_removing_featured_image_cleans_variants(tmp_path, settings) -> None:
    settings.MEDIA_ROOT = tmp_path
    post = Post.objects.create(
        title="Remove Image",
        slug="remove-image",
        content="",
        featured_image=_make_test_image(),
    )
    variant_1x = Path(settings.MEDIA_ROOT) / "posts/featured/featured@1x.webp"
    assert variant_1x.exists()

    post.featured_image = None
    post.save()

    assert not variant_1x.exists()
