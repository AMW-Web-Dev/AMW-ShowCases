from django import forms
from django.utils.text import slugify

from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "content", "excerpt", "image", "tags", "is_published"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Post title"}
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control blog-editor-textarea",
                    "rows": 20,
                    "placeholder": "Write your post in Markdown...",
                }
            ),
            "excerpt": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Brief summary for the blog listing...",
                }
            ),
            "tags": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. django, python, devops",
                }
            ),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if not title:
            return title

        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        instance = self.instance

        exclude_pk = instance.pk if instance and instance.pk else None
        while BlogPost.objects.filter(slug=slug).exclude(pk=exclude_pk).exists():
            counter += 1
            slug = f"{base_slug}-{counter}"

        self._unique_slug = slug
        return title

    def save(self, commit=True):
        instance = super().save(commit=False)
        if hasattr(self, "_unique_slug"):
            instance.slug = self._unique_slug
        if commit:
            instance.save()
            self._save_m2m()
        return instance


class BlogPostCreateForm(BlogPostForm):
    """All fields except author which is set in the view."""

    pass


class BlogPostUpdateForm(BlogPostForm):
    """Form for editing an existing post."""

    pass
