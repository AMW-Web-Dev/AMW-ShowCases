from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from taggit.models import Tag

from .forms import BlogPostCreateForm, BlogPostUpdateForm
from .models import BlogPost


class BlogListView(ListView):
    model = BlogPost
    template_name = "blog/blog_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        return BlogPost.published.select_related("author").prefetch_related("tags")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_tags"] = (
            Tag.objects.filter(blogpost__is_published=True).distinct().order_by("name")
        )
        return context


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = "blog/blog_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return BlogPost.published


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    template_name = "blog/blog_form.html"
    form_class = BlogPostCreateForm
    login_url = "/admin/login/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    template_name = "blog/blog_form.html"
    form_class = BlogPostUpdateForm
    login_url = "/admin/login/"


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogPost
    template_name = "blog/blog_confirm_delete.html"
    success_url = reverse_lazy("Blog:BlogList")
    login_url = "/admin/login/"


def blog_tag_view(request, tag_slug):
    from taggit.models import Tag

    posts = (
        BlogPost.published.filter(tags__slug=tag_slug)
        .select_related("author")
        .prefetch_related("tags")
    )
    return render(
        request,
        "blog/blog_tag.html",
        {
            "posts": posts,
            "tag": tag_slug,
            "all_tags": (
                Tag.objects.filter(blogpost__is_published=True)
                .distinct()
                .order_by("name")
            ),
        },
    )
