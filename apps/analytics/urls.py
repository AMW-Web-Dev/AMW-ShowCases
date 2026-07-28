from django.urls import path

from . import analytics

app_name = "Analytics"

urlpatterns = [
    path("", analytics.AnalyticsDashboardView.as_view(), name="AnalyticsDashboard"),
]
