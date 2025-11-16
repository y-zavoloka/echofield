from typing import Any

from django import forms

from ..models import Post


class PostForm(forms.ModelForm):
    # Add publishing configuration fields: status and published_at
    status = forms.ChoiceField(
        choices=Post.Status.choices,
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True,
        label="Publication Status",
        help_text="Set whether the post is published or still a draft.",
    )
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

    class Meta:
        model = Post
        fields = [
            "title_en",
            "title_uk",
            "content_en",
            "content_uk",
            "featured_image",
            "status",
            "published_at",
        ]
        widgets = {
            "title_en": forms.TextInput(
                attrs={
                    "placeholder": "title in english",
                    "class": "form-control",
                }
            ),
            "title_uk": forms.TextInput(
                attrs={
                    "placeholder": "title in ukrainian",
                    "class": "form-control",
                }
            ),
            "content_en": forms.Textarea(
                attrs={
                    "rows": 10,
                    "placeholder": "content in english",
                    "class": "rich-textarea",
                }
            ),
            "content_uk": forms.Textarea(
                attrs={
                    "rows": 10,
                    "placeholder": "content in ukrainian",
                    "class": "rich-textarea",
                }
            ),
            # Note: status and published_at widgets are defined above.
        }

    def clean(self) -> dict[str, Any]:
        cleaned = super().clean()
        # Ensure both language variants are present; use cleaned_data to avoid None issues.
        if not self.cleaned_data.get("content_en") or not self.cleaned_data.get(
            "content_uk"
        ):
            raise forms.ValidationError("Both language versions are required.")
        # Ensure if status is published, published_at must be present.
        status = self.cleaned_data.get("status")
        published_at = self.cleaned_data.get("published_at")
        if status == Post.Status.PUBLISHED and not published_at:
            self.add_error(
                "published_at",
                "Published posts must have a publish datetime set.",
            )
        # BaseForm.clean() returns a dict for valid forms; guard for type checkers.
        if not isinstance(cleaned, dict):
            raise forms.ValidationError("Invalid cleaned data state.")
        return cleaned

    def save(self, commit: bool = True) -> Post:
        instance = super().save(commit=False)
        # fill the "original" field so that modeltranslation fallback works
        instance.content = self.cleaned_data["content_en"]
        # handle status and published_at
        instance.status = self.cleaned_data["status"]
        instance.published_at = self.cleaned_data.get("published_at")
        if commit:
            instance.save()
        return instance
