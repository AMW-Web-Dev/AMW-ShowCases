from django.views.generic import DetailView, ListView

from .models import Project


class ProjectsListView(ListView):
    model = Project
    template_name = "projects/projects_list.html"
    context_object_name = "projects"
    paginate_by = 12

    def get_queryset(self):
        return Project.objects.prefetch_related("technologies")


class ProjectDetailView(DetailView):
    model = Project
    template_name = "projects/project_detail.html"
    context_object_name = "project"
