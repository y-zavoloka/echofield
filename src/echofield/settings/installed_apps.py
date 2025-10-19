DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "storages",  # R2 via S3
    "modeltranslation",  # uk/en fields
    "markdownx",  # markdown editor
]


PROJECT_APPS = [
    "blog",
]

INSTALLED_APPS = [
    *DJANGO_APPS,
    *THIRD_PARTY_APPS,
    *PROJECT_APPS,
]

__all__ = ["INSTALLED_APPS"]
