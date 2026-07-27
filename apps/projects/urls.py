from django.urls import path

from . import projects

app_name = "projects"

urlpatterns = [
    path("", projects.ProjectsListView.as_view(), name="list"),
    path("<slug:slug>/", projects.ProjectDetailView.as_view(), name="detail"),
]
