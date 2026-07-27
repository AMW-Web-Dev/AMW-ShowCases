# Phase 4: Blog System

## Objective
Create a fully functional blog with Markdown support and tagging.

## Duration
4-5 hours

## Dependencies
- Phase 2: Data Models
- Phase 3: Admin Interface

## Tasks

### Task 4.1: Blog Views
```python
# apps/blog/blog.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import BlogPost

class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        return BlogPost.objects.published().select_related('author').prefetch_related('tags')

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        return BlogPost.objects.published()

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'excerpt', 'image', 'tags']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'excerpt', 'image', 'tags', 'is_published']

class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogPost
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:list')

def blog_tag_view(request, tag_slug):
    """View posts by tag."""
    posts = BlogPost.objects.published().filter(
        tags__slug=tag_slug
    ).select_related('author').prefetch_related('tags')
    
    return render(request, 'blog/blog_tag.html', {
        'posts': posts,
        'tag': tag_slug
    })
```

### Task 4.2: Blog URLs
```python
# apps/blog/urls.py
from django.urls import path
from . import blog

app_name = 'blog'

urlpatterns = [
    path('', blog.BlogListView.as_view(), name='list'),
    path('create/', blog.BlogCreateView.as_view(), name='create'),
    path('<slug:slug>/', blog.BlogDetailView.as_view(), name='detail'),
    path('<slug:slug>/update/', blog.BlogUpdateView.as_view(), name='update'),
    path('<slug:slug>/delete/', blog.BlogDeleteView.as_view(), name='delete'),
    path('tag/<slug:tag_slug>/', blog.blog_tag_view, name='tag'),
]
```

### Task 4.3: Blog Forms
```python
# apps/blog/forms.py
from django import forms
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'excerpt', 'image', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
        }
```

### Task 4.4: Blog Templates
```html
<!-- templates/blog/blog_list.html -->
{% extends 'base.html' %}

{% block title %}Blog - AMW Portfolio{% endblock %}

{% block content %}
<div class="container">
    <h1 class="mb-4">Blog Posts</h1>
    
    <div class="row">
        {% for post in posts %}
        <div class="col-md-6 mb-4">
            <div class="card h-100">
                {% if post.image %}
                <img src="{{ post.image.url }}" class="card-img-top" alt="{{ post.title }}">
                {% endif %}
                <div class="card-body">
                    <h5 class="card-title">{{ post.title }}</h5>
                    <p class="card-text">{{ post.excerpt|default:post.content|truncatewords:30 }}</p>
                    <div class="mb-2">
                        {% for tag in post.tags.all %}
                        <span class="badge bg-secondary">{{ tag.name }}</span>
                        {% endfor %}
                    </div>
                </div>
                <div class="card-footer">
                    <small class="text-muted">
                        {{ post.published_at|date:"F j, Y" }} by {{ post.author.get_full_name }}
                    </small>
                    <a href="{% url 'blog:detail' post.slug %}" class="btn btn-primary btn-sm float-end">Read More</a>
                </div>
            </div>
        </div>
        {% empty %}
        <div class="col-12">
            <p>No blog posts yet.</p>
        </div>
        {% endfor %}
    </div>
    
    {% if is_paginated %}
    <nav aria-label="Blog pagination">
        <ul class="pagination justify-content-center">
            {% if page_obj.has_previous %}
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.previous_page_number }}">Previous</a>
            </li>
            {% endif %}
            
            {% for num in page_obj.paginator.page_range %}
            <li class="page-item {% if page_obj.number == num %}active{% endif %}">
                <a class="page-link" href="?page={{ num }}">{{ num }}</a>
            </li>
            {% endfor %}
            
            {% if page_obj.has_next %}
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.next_page_number }}">Next</a>
            </li>
            {% endif %}
        </ul>
    </nav>
    {% endif %}
</div>
{% endblock %}
```

```html
<!-- templates/blog/blog_detail.html -->
{% extends 'base.html' %}
{% load markdown %}

{% block title %}{{ post.title }} - AMW Portfolio{% endblock %}

{% block meta_description %}{{ post.excerpt|default:post.content|truncatewords:30 }}{% endblock %}

{% block content %}
<div class="container">
    <article class="mt-4">
        <header class="mb-4">
            <h1>{{ post.title }}</h1>
            <p class="text-muted">
                {{ post.published_at|date:"F j, Y" }} by {{ post.author.get_full_name }}
            </p>
            <div class="mb-3">
                {% for tag in post.tags.all %}
                <a href="{% url 'blog:tag' tag.slug %}" class="badge bg-primary text-decoration-none">{{ tag.name }}</a>
                {% endfor %}
            </div>
        </header>
        
        {% if post.image %}
        <img src="{{ post.image.url }}" class="img-fluid rounded mb-4" alt="{{ post.title }}">
        {% endif %}
        
        <div class="blog-content">
            {{ post.content|markdown }}
        </div>
    </article>
    
    <hr class="my-4">
    
    <div class="d-flex justify-content-between">
        <a href="{% url 'blog:list' %}" class="btn btn-outline-secondary">← Back to Blog</a>
        {% if user.is_staff %}
        <a href="{% url 'blog:update' post.slug %}" class="btn btn-outline-primary">Edit Post</a>
        {% endif %}
    </div>
</div>
{% endblock %}
```

### Task 4.5: Markdown Integration
```python
# apps/blog/templatetags/markdown.py
from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    """Convert markdown to HTML."""
    md = markdown.Markdown(extensions=['extra', 'codehilite', 'toc'])
    return mark_safe(md.convert(text))
```

### Task 4.6: Blog CSS
```css
/* static/css/blog.css */
.blog-content {
    line-height: 1.8;
    font-size: 1.1rem;
}

.blog-content h2 { margin-top: 2rem; margin-bottom: 1rem; }
.blog-content h3 { margin-top: 1.5rem; margin-bottom: 0.75rem; }
.blog-content p { margin-bottom: 1.5rem; }

.blog-content pre {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 0.5rem;
    overflow-x: auto;
}

.blog-content code {
    background-color: #f8f9fa;
    padding: 0.2rem 0.4rem;
    border-radius: 0.25rem;
    font-size: 0.9rem;
}

.blog-content pre code {
    background-color: transparent;
    padding: 0;
}

.blog-content img {
    max-width: 100%;
    height: auto;
    border-radius: 0.5rem;
}

.blog-content blockquote {
    border-left: 4px solid #2563eb;
    margin-left: 0;
    padding-left: 1rem;
    color: #6b7280;
    font-style: italic;
}
```

## Verification
- [ ] Blog list page working
- [ ] Blog detail page working
- [ ] Markdown rendering working
- [ ] Tagging system working
- [ ] CRUD operations working

## Commands
```bash
python manage.py runserver
# Visit http://localhost:8000/blog/
# Create posts via admin: http://localhost:8000/admin/blog/blogpost/add/
```

## Next Phase
Phase 5: Skills & Projects