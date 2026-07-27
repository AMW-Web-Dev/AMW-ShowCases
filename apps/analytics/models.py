from django.db import models


class PageView(models.Model):
    path = models.CharField(max_length=500)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.path} - {self.created_at}"


class Visitor(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    first_visit = models.DateTimeField(auto_now_add=True)
    last_visit = models.DateTimeField(auto_now=True)
    visit_count = models.IntegerField(default=1)

    class Meta:
        ordering = ["-last_visit"]

    def __str__(self):
        return self.ip_address
