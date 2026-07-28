from django.views.generic import DetailView, ListView

from ..skills.models import SkillCategory
from .models import Project


class ProjectsListView(ListView):
    model = Project
    template_name = "projects/projects_list.html"
    context_object_name = "projects"
    paginate_by = 12

    def get_queryset(self):
        qs = Project.objects.prefetch_related("technologies")
        category_slug = self.request.GET.get("category")
        if category_slug:
            qs = qs.filter(technologies__category__slug=category_slug)
        return qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_categories"] = (
            SkillCategory.objects.filter(skills__projects__isnull=False)
            .distinct()
            .order_by("order", "name")
        )
        context["active_category"] = self.request.GET.get("category", "")
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = "projects/project_detail.html"
    context_object_name = "project"
