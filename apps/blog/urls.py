from django.urls import path

from . import blog

app_name = "Blog"

urlpatterns = [
    path("", blog.BlogListView.as_view(), name="BlogList"),
    path("create/", blog.BlogCreateView.as_view(), name="BlogCreate"),
    path("<slug:slug>/", blog.BlogDetailView.as_view(), name="BlogDetail"),
    path("<slug:slug>/update/", blog.BlogUpdateView.as_view(), name="BlogUpdate"),
    path("<slug:slug>/delete/", blog.BlogDeleteView.as_view(), name="BlogDelete"),
    path("tag/<slug:tag_slug>/", blog.blog_tag_view, name="BlogTag"),
]
