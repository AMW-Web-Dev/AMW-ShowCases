from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from apps.blog.models import BlogPost
from apps.projects.models import Project
from apps.skills.models import Skill

from .models import ContactMessage


class HomepageView(TemplateView):
    template_name = "core/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_projects"] = Project.objects.filter(featured=True)[:4]
        context["recent_posts"] = BlogPost.published.select_related(
            "author"
        ).prefetch_related("tags")[:3]
        context["featured_skills"] = Skill.objects.filter(featured=True)[:12]
        return context


def about_view(request):
    return render(request, "core/about.html")


def contact_view(request):
    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST.get("name", "").strip(),
            email=request.POST.get("email", "").strip(),
            subject=request.POST.get("subject", "").strip(),
            message=request.POST.get("message", "").strip(),
        )
        messages.success(request, "Thanks for reaching out! I'll get back to you soon.")
        return redirect("core:contact")
    return render(request, "core/contact.html")
