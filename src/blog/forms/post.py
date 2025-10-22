from django import forms

from ..models import Post


class PostForm(forms.ModelForm[Post]):
    class Meta:
        model = Post
        fields = ["title_en", "title_uk", "content_en", "content_uk"]
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
        }

    def clean(self) -> dict[str, object]:
        cleaned = super().clean()
        if not cleaned.get("content_en") or not cleaned.get("content_uk"):
            raise forms.ValidationError("Both language versions are required.")
        return cleaned

    def save(self, commit: bool = True) -> Post:
        instance = super().save(commit=False)
        # fill the "original" field so that modeltranslation fallback works
        instance.content = self.cleaned_data["content_en"]
        if commit:
            instance.save()
        return instance
