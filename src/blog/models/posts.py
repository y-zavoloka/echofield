from __future__ import annotations

import re

from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from markdown import markdown
from typing_extensions import Self


class PostPublicQuerySet(models.QuerySet["Post"]):
    def published(self) -> "Self":
        """Return posts whose publication date has passed.

        A post is considered published if:
        - ``published_at`` is set, and
        - ``published_at`` is less than or equal to the current time.

        The ``status`` field is ignored for publication; it is kept only for
        legacy data and potential editorial hints.
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
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(_("Title"), max_length=300)
    slug = models.SlugField(_("Slug"), max_length=320, unique=True)
    content = models.TextField(_("Content"), blank=True, null=False)
    featured_image = models.ImageField(
        _("Featured image"), upload_to="posts/featured/", null=True, blank=True
    )
    status = models.CharField(
        _("Status"), max_length=10, choices=Status.choices, default=Status.DRAFT
    )
    published_at = models.DateTimeField(_("Published at"), null=True, blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    objects: models.Manager["Post"] = models.Manager()
    public: PostPublicManager = PostPublicManager()

    class Meta:
        ordering = ["-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["status", "published_at"]),
        ]

    def __str__(self) -> str:
        return self.title

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
