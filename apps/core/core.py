from django.shortcuts import render
from django.views.generic import TemplateView

from apps.blog.models import BlogPost
from apps.projects.models import Project
from apps.skills.models import Skill


class HomepageView(TemplateView):
    template_name = "core/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_projects"] = Project.objects.filter(featured=True)[:3]
        context["recent_posts"] = BlogPost.published.select_related(
            "author"
        ).prefetch_related("tags")[:3]
        context["featured_skills"] = Skill.objects.filter(featured=True)[:6]
        return context


def about_view(request):
    return render(request, "core/about.html")


def contact_view(request):
    return render(request, "core/contact.html")
