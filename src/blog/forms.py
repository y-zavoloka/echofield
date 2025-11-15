from __future__ import annotations

from django import forms
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from .models import Post


class PostEditorForm(forms.ModelForm):
    """Form for editing posts in two languages with Markdown content.

    The underlying model uses django-modeltranslation, so we expose only the
    explicit `*_en` and `*_uk` fields. The default values for Ukrainian fields
    are derived from the English ones when they are empty.
    """

    published_at = forms.DateTimeField(
        required=False,
        label=_("Publish at"),
        widget=forms.DateTimeInput(
            format="%Y-%m-%dT%H:%M",
            attrs={
                "type": "datetime-local",
            },
        ),
        input_formats=["%Y-%m-%dT%H:%M"],
    )

    class Meta:
        model = Post
        fields = [
            "title_en",
            "title_uk",
            "slug",
            "slug_en",
            "slug_uk",
            "published_at",
            "content_en",
            "content_uk",
        ]

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)

        self.fields["title_en"].label = _("Title (English)")
        self.fields["title_uk"].label = _("Title (Ukrainian)")
        self.fields["content_en"].label = _("Content (English, Markdown)")
        self.fields["content_uk"].label = _("Content (Ukrainian, Markdown)")
        self.fields["slug_en"].label = _("Slug (English)")
        self.fields["slug_uk"].label = _("Slug (Ukrainian)")

        # Provide a sensible default for publish date on new posts.
        if not self.instance.pk and not self.initial.get("published_at"):
            self.initial["published_at"] = timezone.localtime().strftime(
                "%Y-%m-%dT%H:%M"
            )

        # When there is no explicit Ukrainian value, start with English as a
        # sensible default so editors don't have to copy-paste manually.
        initial_title_en = self.initial.get("title_en") or self.data.get("title_en")
        initial_content_en = self.initial.get("content_en") or self.data.get(
            "content_en"
        )

        if not self.initial.get("title_uk") and initial_title_en:
            self.initial.setdefault("title_uk", initial_title_en)

        if not self.initial.get("content_uk") and initial_content_en:
            self.initial.setdefault("content_uk", initial_content_en)

    def clean(self) -> dict[str, object]:
        cleaned = super().clean()

        title_en = str(cleaned.get("title_en") or "").strip()
        slug_en = str(cleaned.get("slug_en") or "").strip()

        if not slug_en and title_en:
            slug_en = slugify(title_en)[:320]
            cleaned["slug_en"] = slug_en
            self.cleaned_data["slug_en"] = slug_en

        # Keep base slug and Ukrainian slug in sync with English by default.
        if not cleaned.get("slug") and slug_en:
            cleaned["slug"] = slug_en
            self.cleaned_data["slug"] = slug_en

        if not cleaned.get("slug_uk") and slug_en:
            cleaned["slug_uk"] = slug_en
            self.cleaned_data["slug_uk"] = slug_en

        return cleaned
