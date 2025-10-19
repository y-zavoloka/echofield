from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "published_at", "updated_at")
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("status",)
    search_fields = ("title", "content")
    ordering = ("-published_at",)
