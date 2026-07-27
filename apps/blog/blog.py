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

from .models import BlogPost


class BlogListView(ListView):
    model = BlogPost
    template_name = "blog/blog_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        return BlogPost.published.select_related("author").prefetch_related("tags")


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = "blog/blog_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return BlogPost.published


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    template_name = "blog/blog_form.html"
    fields = ["title", "content", "excerpt", "image", "tags"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    template_name = "blog/blog_form.html"
    fields = ["title", "content", "excerpt", "image", "tags", "is_published"]


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogPost
    template_name = "blog/blog_confirm_delete.html"
    success_url = reverse_lazy("blog:list")


def blog_tag_view(request, tag_slug):
    posts = (
        BlogPost.published.filter(tags__slug=tag_slug)
        .select_related("author")
        .prefetch_related("tags")
    )
    return render(
        request,
        "blog/blog_tag.html",
        {"posts": posts, "tag": tag_slug},
    )
