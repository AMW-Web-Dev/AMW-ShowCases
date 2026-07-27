from django.urls import path

from . import blog

app_name = "blog"

urlpatterns = [
    path("", blog.BlogListView.as_view(), name="list"),
    path("create/", blog.BlogCreateView.as_view(), name="create"),
    path("<slug:slug>/", blog.BlogDetailView.as_view(), name="detail"),
    path("<slug:slug>/update/", blog.BlogUpdateView.as_view(), name="update"),
    path("<slug:slug>/delete/", blog.BlogDeleteView.as_view(), name="delete"),
    path("tag/<slug:tag_slug>/", blog.blog_tag_view, name="tag"),
]
