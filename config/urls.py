from django.contrib import admin
from django.urls import include, path

from apps.core.health import health_check

urlpatterns = [
    path("health/", health_check, name="health_check"),
    path("admin/", admin.site.urls),
    path("markdownx/", include("markdownx.urls")),
    path("", include("apps.core.urls")),
    path("auth/", include("apps.humans.urls")),
    path("skills/", include("apps.skills.urls")),
    path("projects/", include("apps.projects.urls")),
    path("blog/", include("apps.blog.urls")),
    path("dashboard/", include("apps.analytics.urls")),
]
