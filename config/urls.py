from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.core.health import health_check

urlpatterns = [
    path("health/", health_check, name="HealthCheck"),
    path("admin/", admin.site.urls),
    path("markdownx/", include("markdownx.urls")),
    path("", include("apps.core.urls", namespace="Core")),
    path("auth/", include("apps.humans.urls", namespace="Humans")),
    path("skills/", include("apps.skills.urls", namespace="Skills")),
    path("projects/", include("apps.projects.urls", namespace="Projects")),
    path("blog/", include("apps.blog.urls", namespace="Blog")),
    path("dashboard/", include("apps.analytics.urls", namespace="Analytics")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
