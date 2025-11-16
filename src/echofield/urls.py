from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.urls import include, path

i18n_patterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
    *i18n_patterns,
]

# Serve static and media files during development
if settings.DEBUG:
    # Serve media files from MEDIA_ROOT
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve static files using staticfiles app (serves from app-level static/ directories)
    # The serve view from staticfiles automatically finds files in app static/ directories
    # Remove trailing slash from STATIC_URL for the path pattern
    static_url_pattern = settings.STATIC_URL.rstrip("/")
    urlpatterns += [
        path(f"{static_url_pattern}/<path:path>", serve),
    ]
