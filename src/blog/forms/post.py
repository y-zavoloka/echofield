from typing import Any

from django import forms

from ..models import Post


class PostForm(forms.ModelForm):
    """Form used by the internal post editor views.

    This form now includes localizable fields for title, slug, and content,
    as assumed to be present by modeltranslation. All user-facing edit fields
    related to the Post, including featured_image, and published_at,
    are exposed.
    """

    published_at = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "form-control",
                "placeholder": "YYYY-MM-DD HH:MM",
            }
        ),
        required=False,
        label="Publish Time",
        help_text="Set publish datetime for scheduling (leave blank for draft).",
    )

    # Base fields (populated from *_en fields in save(), but exposed for programmatic access)
    title = forms.CharField(
        required=False,
        label="Title",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    slug = forms.SlugField(
        required=False,
        label="Slug",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    content = forms.CharField(
        required=False,
        label="Content",
        widget=forms.Textarea(attrs={"rows": 10, "class": "rich-textarea"}),
    )

    # Language-specific fields (assuming modeltranslation is in use)
    title_en = forms.CharField(
        required=True,
        label="Title (English)",
        widget=forms.TextInput(
            attrs={"placeholder": "Title (EN)", "class": "form-control"}
        ),
    )
    title_uk = forms.CharField(
        required=True,
        label="Title (Ukrainian)",
        widget=forms.TextInput(
            attrs={"placeholder": "Title (UK)", "class": "form-control"}
        ),
    )
    slug_en = forms.SlugField(
        required=True,
        label="Slug (English)",
        widget=forms.TextInput(
            attrs={"placeholder": "slug-en", "class": "form-control"}
        ),
    )
    slug_uk = forms.SlugField(
        required=True,
        label="Slug (Ukrainian)",
        widget=forms.TextInput(
            attrs={"placeholder": "slug-uk", "class": "form-control"}
        ),
    )
    content_en = forms.CharField(
        required=True,
        label="Content (English)",
        widget=forms.Textarea(
            attrs={
                "rows": 10,
                "placeholder": "Post content (Markdown, EN)",
                "class": "rich-textarea",
            }
        ),
    )
    content_uk = forms.CharField(
        required=True,
        label="Content (Ukrainian)",
        widget=forms.Textarea(
            attrs={
                "rows": 10,
                "placeholder": "Post content (Markdown, UK)",
                "class": "rich-textarea",
            }
        ),
    )
    featured_image = forms.ImageField(
        required=False,
        label="Featured Image",
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Post
        # original `title`, `slug` and `content` should be populated from
        # correlated `*_en` field, but we still expose them explicitly so
        # callers (and tests) can work with canonical values.
        fields = [
            "title",
            "slug",
            "content",
            "title_en",
            "title_uk",
            "slug_en",
            "slug_uk",
            "content_en",
            "content_uk",
            "featured_image",
            "published_at",
        ]
        widgets = {
            "featured_image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def clean(self) -> dict[str, Any]:
        cleaned = super().clean()

        if not cleaned.get("content_en") or not cleaned.get("content_uk"):
            raise forms.ValidationError(
                "Both English and Ukrainian content are required."
            )

        if not cleaned.get("title_en") or not cleaned.get("title_uk"):
            raise forms.ValidationError(
                "Both English and Ukrainian titles are required."
            )

        if not isinstance(cleaned, dict):  # Defensive guard for type checkers.
            raise forms.ValidationError("Invalid cleaned data state.")
        return cleaned

    def save(self, commit: bool = True) -> Post:
        instance = super().save(commit=False)

        # Canonical values primarily come from the base fields; we mirror them
        # into the English-localized fields so that the modeltranslation-backed
        # ``title``/``content`` accessors return these canonical values.
        base_title = self.cleaned_data.get("title") or self.cleaned_data.get(
            "title_en", ""
        )
        base_slug = self.cleaned_data.get("slug") or self.cleaned_data.get(
            "slug_en", ""
        )
        base_content = self.cleaned_data.get("content") or self.cleaned_data.get(
            "content_en", ""
        )

        # Canonical + English fields
        instance.title = base_title
        instance.slug = base_slug
        instance.content = base_content

        instance.title_en = base_title
        instance.content_en = base_content

        # Other localized fields
        instance.title_uk = self.cleaned_data.get("title_uk", "")
        instance.slug_en = self.cleaned_data.get("slug_en", base_slug)
        instance.slug_uk = self.cleaned_data.get("slug_uk", "")
        instance.content_uk = self.cleaned_data.get("content_uk", "")

        # Other metadata
        instance.featured_image = self.cleaned_data.get("featured_image")
        instance.published_at = self.cleaned_data.get("published_at")

        if commit:
            instance.save()
        return instance
