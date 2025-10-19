from django.contrib import admin
from django.urls import include, path

i18n_patterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("markdownx/", include("markdownx.urls")),
    path("", include("blog.urls")),
    *i18n_patterns,
]
