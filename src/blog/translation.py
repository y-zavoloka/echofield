from modeltranslation.translator import TranslationOptions, register

from .models import Category, Post


@register(Post)
class PostTranslationOptions(TranslationOptions):
    # We translate title and content only.
    #
    # Slugs are kept canonical on the base ``slug`` field so that
    # ``post.slug`` is stable regardless of active language, while
    # language-specific slugs live on ``slug_en`` / ``slug_uk`` and
    # are used explicitly by query helpers and views.
    fields = ("title", "content")


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    """Expose localized name/slug fields for categories."""

    fields = ("name", "slug")
