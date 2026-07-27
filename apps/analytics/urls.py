from django.urls import path

from . import analytics

app_name = "analytics"

urlpatterns = [
    path("", analytics.AnalyticsDashboardView.as_view(), name="dashboard"),
]
