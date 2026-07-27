from django.views.generic import ListView

from .models import Skill, SkillCategory


class SkillsListView(ListView):
    model = SkillCategory
    template_name = "skills/skills_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return SkillCategory.objects.prefetch_related("skills").order_by("order")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_skills"] = Skill.objects.filter(featured=True)
        return context
