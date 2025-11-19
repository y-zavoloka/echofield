from __future__ import annotations

from datetime import datetime

from django.contrib.sitemaps import Sitemap
from django.db.models import QuerySet

from .models import Post


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self) -> QuerySet[Post]:
        return Post.public.published()

    def lastmod(self, obj: Post) -> datetime | None:
        return obj.updated_at or obj.published_at

    def location(self, obj: Post) -> str:
        return obj.get_absolute_url()


__all__ = ["PostSitemap"]
