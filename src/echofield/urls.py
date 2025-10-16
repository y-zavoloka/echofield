from django.contrib import admin
from django.urls import path, include

i18n_patterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
    *i18n_patterns,
]
