from __future__ import annotations

from django.contrib import admin

from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "updated_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "published_at", "created_at")
    list_filter = ("published_at", "categories")
    search_fields = ("title", "slug")
    filter_horizontal = ("categories",)
