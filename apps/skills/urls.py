from django.urls import path

from . import skills as skills_views

app_name = "skills"

urlpatterns = [
    path("", skills_views.SkillsListView.as_view(), name="list"),
]
