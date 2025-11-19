from __future__ import annotations

import re

from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from markdown import markdown
from typing_extensions import Self

from ..utils.images import (
    WEBP_VARIANT_WIDTHS,
    delete_webp_variants,
    generate_webp_variants,
    get_variant_urls,
)


class PostPublicQuerySet(models.QuerySet["Post"]):
    def published(self) -> "Self":
        """Return posts whose publication date has passed.

        A post is considered published if:
        - ``published_at`` is set, and
        - ``published_at`` is less than or equal to the current time.
        """
        now = timezone.now()
        return self.filter(
            published_at__isnull=False,
            published_at__lte=now,
        )

    def for_slug(self, slug: str, lang: str | None = None) -> "Self":
        """Filter *published* posts by their slug.

        If a language is provided, filters by the slug field for that language (e.g., 'slug_en').
        If no language is provided, searches all available localized slug fields (including 'slug').
        Assumes fields such as slug_en and slug_uk exist for localized slugs.
        """
        qs: "PostPublicQuerySet" = self.published()
        if lang:
            # Assumes fields like slug_en, slug_uk, etc. If only a single slug field exists, use slug=slug.
            filter_kwargs = {f"slug_{lang}": slug}
            return qs.filter(**filter_kwargs)
        return qs.filter(Q(slug=slug) | Q(slug_en=slug) | Q(slug_uk=slug))


class PostPublicManager(models.Manager["Post"]):
    def get_queryset(self) -> PostPublicQuerySet:
        """
        Return a type-annotated PostQuerySet for queryset operations.
        """
        return PostPublicQuerySet(self.model, using=self._db)

    def published(self) -> PostPublicQuerySet:
        """
        Shortcut to return only published posts.
        """
        return self.get_queryset().published()

    def for_slug(self, slug: str, lang: str | None = None) -> PostPublicQuerySet:
        """
        Shortcut to filter posts by slug and (optionally) by language.
        """
        return self.get_queryset().for_slug(slug, lang)


class Post(models.Model):
    title = models.CharField(_("Title"), max_length=300)
    slug = models.SlugField(_("Slug"), max_length=320, unique=True)
    # Language-specific slugs live on explicit fields so we can query them
    # directly without relying on modeltranslation to generate virtual fields.
    slug_en = models.SlugField(
        _("Slug (English)"), max_length=320, unique=True, null=True, blank=True
    )
    slug_uk = models.SlugField(
        _("Slug (Ukrainian)"), max_length=320, unique=True, null=True, blank=True
    )
    content = models.TextField(_("Content"), blank=True, null=False)
    featured_image = models.ImageField(
        _("Featured image"), upload_to="posts/featured/", null=True, blank=True
    )
    published_at = models.DateTimeField(_("Published at"), null=True, blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    categories = models.ManyToManyField(
        "Category",
        verbose_name=_("Categories"),
        related_name="posts",
        blank=True,
    )
    FEATURED_IMAGE_VARIANTS = tuple(WEBP_VARIANT_WIDTHS.keys())

    objects: models.Manager["Post"] = models.Manager()
    public: PostPublicManager = PostPublicManager()

    class Meta:
        ordering = ["-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["published_at"]),
        ]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("post_detail", kwargs={"slug": self.slug})

    @property
    def content_html(self) -> str:
        """Return the post content rendered from Markdown to HTML.

        The raw Markdown is stored in the ``content`` TextField. For rendering,
        we convert it to HTML on the backend so the public frontend never needs
        to load any Markdown libraries.
        """

        if not self.content:
            return ""

        # Basic backwards-compatibility: if the content already looks like HTML,
        # don't re-run it through the Markdown renderer.
        if "<" in self.content and re.search(r"<[a-zA-Z][^>]*>", self.content):
            return self.content

        return markdown(self.content)

    def save(self, *args: object, **kwargs: object) -> None:  # type: ignore[override]
        previous_image: str | None = None
        if self.pk:
            previous_image = (
                Post.objects.filter(pk=self.pk)
                .values_list("featured_image", flat=True)
                .first()
            )
        super().save(*args, **kwargs)
        self._sync_featured_image_variants(previous_image)

    def delete(self, *args: object, **kwargs: object) -> None:  # type: ignore[override]
        current_image = self.featured_image.name if self.featured_image else None
        storage = self._meta.get_field("featured_image").storage
        super().delete(*args, **kwargs)
        if current_image:
            delete_webp_variants(current_image, storage, self.FEATURED_IMAGE_VARIANTS)

    def _sync_featured_image_variants(self, previous_image: str | None) -> None:
        storage = self._meta.get_field("featured_image").storage
        new_image = self.featured_image.name if self.featured_image else None

        if previous_image and previous_image != new_image:
            delete_webp_variants(previous_image, storage, self.FEATURED_IMAGE_VARIANTS)

        if not self.featured_image or not new_image:
            return

        if previous_image == new_image:
            return

        generate_webp_variants(self.featured_image, WEBP_VARIANT_WIDTHS)

    @property
    def featured_image_webp_srcset(self) -> str:
        if not self.featured_image:
            return ""
        urls = get_variant_urls(self.featured_image, self.FEATURED_IMAGE_VARIANTS)
        ordered = []
        for label in self.FEATURED_IMAGE_VARIANTS:
            url = urls.get(label)
            if url:
                ordered.append(f"{url} {label}")
        return ", ".join(ordered)

    @property
    def seo_description(self) -> str:
        plain = strip_tags(self.content_html)
        normalized = " ".join(plain.split())
        return (normalized[:155] + "...") if len(normalized) > 155 else normalized

    def get_social_image_url(self) -> str | None:
        if not self.featured_image:
            return None
        urls = get_variant_urls(self.featured_image, ("2x", "1x"))
        return urls.get("2x") or urls.get("1x") or self.featured_image.url

    def build_json_ld(self, canonical_url: str) -> dict[str, object]:
        data: dict[str, object] = {
            "@context": "https://schema.org",
            "@type": "Article",
            "mainEntityOfPage": canonical_url,
            "headline": self.title,
            "description": self.seo_description,
            "datePublished": (
                self.published_at.isoformat() if self.published_at else None
            ),
            "dateModified": self.updated_at.isoformat() if self.updated_at else None,
            "author": {"@type": "Organization", "name": "EchoField"},
            "publisher": {
                "@type": "Organization",
                "name": "EchoField",
            },
        }
        image_url = self.get_social_image_url()
        if image_url:
            data["image"] = [image_url]
        return {k: v for k, v in data.items() if v}
