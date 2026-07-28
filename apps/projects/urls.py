from django.urls import path

from . import projects

app_name = "Projects"

urlpatterns = [
    path("", projects.ProjectsListView.as_view(), name="ProjectsList"),
    path("<slug:slug>/", projects.ProjectDetailView.as_view(), name="ProjectDetail"),
]
