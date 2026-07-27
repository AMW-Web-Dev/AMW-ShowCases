from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to="blog/", blank=True, null=True)
    author = models.ForeignKey(
        "humans.User", on_delete=models.CASCADE, related_name="blog_posts"
    )
    tags = TaggableManager(blank=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/blog/{self.slug}/"

    @property
    def is_published_now(self):
        from django.utils import timezone

        if self.published_at:
            return self.published_at <= timezone.now()
        return self.is_published
