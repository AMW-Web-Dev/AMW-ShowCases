from django.db import models
from django.utils.text import slugify


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    long_description = models.TextField(blank=True)
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    github_url = models.URLField(max_length=200, blank=True)
    live_url = models.URLField(max_length=200, blank=True)
    technologies = models.ManyToManyField(
        "skills.Skill", blank=True, related_name="projects"
    )
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
