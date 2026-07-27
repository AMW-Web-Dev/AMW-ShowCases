# Phase 6: Core App & Homepage

## Objective
Create the core app with homepage and shared utilities.

## Duration
2-3 hours

## Dependencies
- Phase 4: Blog System
- Phase 5: Skills & Projects

## Tasks

### Task 6.1: Core Views
```python
# apps/core/core.py
from django.shortcuts import render
from django.views.generic import TemplateView
from apps.blog.models import BlogPost
from apps.projects.models import Project
from apps.skills.models import Skill

class HomepageView(TemplateView):
    template_name = 'core/homepage.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_projects'] = Project.objects.filter(featured=True)[:3]
        context['recent_posts'] = BlogPost.objects.published().select_related('author').prefetch_related('tags')[:3]
        context['featured_skills'] = Skill.objects.filter(featured=True)[:6]
        return context

def about_view(request):
    """About page view."""
    return render(request, 'core/about.html')

def contact_view(request):
    """Contact page view."""
    return render(request, 'core/contact.html')
```

### Task 6.2: Core URLs
```python
# apps/core/urls.py
from django.urls import path
from . import core

app_name = 'core'

urlpatterns = [
    path('', core.HomepageView.as_view(), name='homepage'),
    path('about/', core.about_view, name='about'),
    path('contact/', core.contact_view, name='contact'),
]
```

### Task 6.3: Base Template
```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}AMW Portfolio{% endblock %}</title>
    <meta name="description" content="{% block meta_description %}Professional portfolio showcasing skills, projects, and expertise{% endblock %}">
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Bootstrap Icons -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
    
    <!-- Highlight.js -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
    
    <!-- Custom CSS -->
    <link href="{% static 'css/custom.css' %}" rel="stylesheet">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top">
        <div class="container">
            <a class="navbar-brand" href="{% url 'core:homepage' %}">
                <strong>AMW</strong> Portfolio
            </a>
            
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'core:homepage' %}">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'skills:list' %}">Skills</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'projects:list' %}">Projects</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'blog:list' %}">Blog</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'core:about' %}">About</a>
                    </li>
                    {% if user.is_staff %}
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'admin:index' %}">Admin</a>
                    </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>
    
    <!-- Main Content -->
    <main class="flex-shrink-0">
        {% block content %}{% endblock %}
    </main>
    
    <!-- Footer -->
    <footer class="footer mt-auto py-3 bg-dark text-white">
        <div class="container text-center">
            <span class="text-muted">
                &copy; {{ current_year }} AMW Portfolio. Built with Django & HTMX.
            </span>
        </div>
    </footer>
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- HTMX -->
    <script src="https://unpkg.com/htmx.org@1.9.12"></script>
    
    <!-- Highlight.js -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script>hljs.highlightAll();</script>
    
    <!-- Custom JS -->
    <script src="{% static 'js/custom.js' %}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### Task 6.4: Homepage Template
```html
<!-- templates/core/homepage.html -->
{% extends 'base.html' %}

{% block title %}AMW Portfolio - Home{% endblock %}

{% block content %}
<!-- Hero Section -->
<section class="hero-section bg-primary text-white py-5">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-6">
                <h1 class="display-4 fw-bold mb-3">AMW</h1>
                <p class="lead mb-4">
                    DevOps Engineer | Python Developer | Linux Specialist
                </p>
                <p class="mb-4">
                    Building scalable solutions with modern technologies.
                    Specializing in automation, cloud infrastructure, and web development.
                </p>
                <div class="d-flex gap-2">
                    <a href="{% url 'projects:list' %}" class="btn btn-light btn-lg">View Projects</a>
                    <a href="{% url 'core:contact' %}" class="btn btn-outline-light btn-lg">Contact Me</a>
                </div>
            </div>
            <div class="col-lg-6 text-center">
                {% if user.avatar %}
                <img src="{{ user.avatar.url }}" class="rounded-circle img-fluid" alt="AMW" style="max-width: 300px;">
                {% else %}
                <div class="avatar-placeholder rounded-circle mx-auto" style="width: 300px; height: 300px; background-color: rgba(255,255,255,0.2);">
                    <span class="display-1">AMW</span>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
</section>

<!-- Featured Skills -->
{% if featured_skills %}
<section class="py-5">
    <div class="container">
        <h2 class="text-center mb-4">Featured Skills</h2>
        <div class="row">
            {% for skill in featured_skills %}
            <div class="col-md-4 mb-3">
                <div class="card text-center skill-card">
                    <div class="card-body">
                        <h5 class="card-title">{{ skill.name }}</h5>
                        <div class="progress mb-2" style="height: 10px;">
                            <div class="progress-bar bg-primary" role="progressbar" 
                                 style="width: {{ skill.proficiency }}%"
                                 aria-valuenow="{{ skill.proficiency }}" 
                                 aria-valuemin="0" 
                                 aria-valuemax="100">
                            </div>
                        </div>
                        <small class="text-muted">{{ skill.proficiency }}%</small>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        <div class="text-center mt-3">
            <a href="{% url 'skills:list' %}" class="btn btn-outline-primary">View All Skills</a>
        </div>
    </div>
</section>
{% endif %}

<!-- Featured Projects -->
{% if featured_projects %}
<section class="py-5 bg-light">
    <div class="container">
        <h2 class="text-center mb-4">Featured Projects</h2>
        <div class="row">
            {% for project in featured_projects %}
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    {% if project.image %}
                    <img src="{{ project.image.url }}" class="card-img-top" alt="{{ project.title }}">
                    {% endif %}
                    <div class="card-body">
                        <h5 class="card-title">{{ project.title }}</h5>
                        <p class="card-text">{{ project.description|truncatewords:20 }}</p>
                    </div>
                    <div class="card-footer">
                        <a href="{% url 'projects:detail' project.slug %}" class="btn btn-primary btn-sm">View Details</a>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        <div class="text-center mt-3">
            <a href="{% url 'projects:list' %}" class="btn btn-outline-primary">View All Projects</a>
        </div>
    </div>
</section>
{% endif %}

<!-- Recent Blog Posts -->
{% if recent_posts %}
<section class="py-5">
    <div class="container">
        <h2 class="text-center mb-4">Recent Blog Posts</h2>
        <div class="row">
            {% for post in recent_posts %}
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    {% if post.image %}
                    <img src="{{ post.image.url }}" class="card-img-top" alt="{{ post.title }}">
                    {% endif %}
                    <div class="card-body">
                        <h5 class="card-title">{{ post.title }}</h5>
                        <p class="card-text">{{ post.excerpt|default:post.content|truncatewords:20 }}</p>
                        <div class="mb-2">
                            {% for tag in post.tags.all %}
                            <span class="badge bg-secondary">{{ tag.name }}</span>
                            {% endfor %}
                        </div>
                    </div>
                    <div class="card-footer">
                        <small class="text-muted">{{ post.published_at|date:"F j, Y" }}</small>
                        <a href="{% url 'blog:detail' post.slug %}" class="btn btn-primary btn-sm float-end">Read More</a>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        <div class="text-center mt-3">
            <a href="{% url 'blog:list' %}" class="btn btn-outline-primary">View All Posts</a>
        </div>
    </div>
</section>
{% endif %}
{% endblock %}
```

### Task 6.5: About Page
```html
<!-- templates/core/about.html -->
{% extends 'base.html' %}

{% block title %}About - AMW Portfolio{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="row">
        <div class="col-lg-8">
            <h1 class="mb-4">About Me</h1>
            
            <div class="mb-4">
                <h2>Professional Summary</h2>
                <p>
                    DevOps Engineer and Python Developer with extensive experience in 
                    building and maintaining scalable infrastructure. Specializing in 
                    automation, containerization, and cloud-native solutions.
                </p>
            </div>
            
            <div class="mb-4">
                <h2>Specializations</h2>
                <ul class="list-unstyled">
                    <li class="mb-2"><strong>DevOps:</strong> Docker, Kubernetes, CI/CD, Cloud Infrastructure</li>
                    <li class="mb-2"><strong>Backend:</strong> Python, Django, PostgreSQL, REST APIs</li>
                    <li class="mb-2"><strong>Linux:</strong> System Administration, Shell Scripting, Automation</li>
                    <li class="mb-2"><strong>Data:</strong> Analytics, ETL Pipelines, Data Processing</li>
                </ul>
            </div>
            
            <div class="mb-4">
                <h2>Current Focus</h2>
                <ul>
                    <li>Building scalable web applications with Django and HTMX</li>
                    <li>Automating development workflows and infrastructure</li>
                    <li>Contributing to open source projects</li>
                    <li>Exploring cloud-native architectures</li>
                </ul>
            </div>
        </div>
        
        <div class="col-lg-4">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Contact Information</h5>
                    <ul class="list-unstyled">
                        <li class="mb-2">
                            <i class="bi bi-envelope"></i> amw@example.com
                        </li>
                        <li class="mb-2">
                            <i class="bi bi-github"></i> <a href="https://github.com/amw" class="text-decoration-none">github.com/amw</a>
                        </li>
                        <li class="mb-2">
                            <i class="bi bi-linkedin"></i> <a href="https://linkedin.com/in/amw" class="text-decoration-none">linkedin.com/in/amw</a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Task 6.6: Contact Page
```html
<!-- templates/core/contact.html -->
{% extends 'base.html' %}

{% block title %}Contact - AMW Portfolio{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="row">
        <div class="col-lg-8">
            <h1 class="mb-4">Contact Me</h1>
            
            <p class="lead mb-4">
                Get in touch for collaborations, opportunities, or just to say hello.
            </p>
            
            <form method="post" action="{% url 'core:contact' %}">
                {% csrf_token %}
                <div class="mb-3">
                    <label for="name" class="form-label">Name</label>
                    <input type="text" class="form-control" id="name" name="name" required>
                </div>
                <div class="mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input type="email" class="form-control" id="email" name="email" required>
                </div>
                <div class="mb-3">
                    <label for="subject" class="form-label">Subject</label>
                    <input type="text" class="form-control" id="subject" name="subject" required>
                </div>
                <div class="mb-3">
                    <label for="message" class="form-label">Message</label>
                    <textarea class="form-control" id="message" name="message" rows="5" required></textarea>
                </div>
                <button type="submit" class="btn btn-primary">Send Message</button>
            </form>
        </div>
        
        <div class="col-lg-4">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Connect With Me</h5>
                    <ul class="list-unstyled">
                        <li class="mb-3">
                            <a href="https://github.com/amw" class="btn btn-outline-dark w-100" target="_blank">
                                <i class="bi bi-github"></i> GitHub
                            </a>
                        </li>
                        <li class="mb-3">
                            <a href="https://linkedin.com/in/amw" class="btn btn-outline-primary w-100" target="_blank">
                                <i class="bi bi-linkedin"></i> LinkedIn
                            </a>
                        </li>
                        <li class="mb-3">
                            <a href="mailto:amw@example.com" class="btn btn-outline-success w-100">
                                <i class="bi bi-envelope"></i> Email
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Task 6.7: Context Processor for Current Year
```python
# apps/core/context_processors.py
from datetime import datetime

def current_year(request):
    """Add current year to all templates."""
    return {'current_year': datetime.now().year}
```

Add to settings:
```python
# config/settings/base.py
TEMPLATES = [
    {
        ...
        'OPTIONS': {
            'context_processors': [
                ...
                'apps.core.context_processors.current_year',
            ],
        },
    },
]
```

## Verification
- [ ] Homepage working
- [ ] About page working
- [ ] Contact page working
- [ ] Navigation working
- [ ] Footer working

## Commands
```bash
python manage.py runserver
# Visit http://localhost:8000/
# Visit http://localhost:8000/about/
# Visit http://localhost:8000/contact/
```

## Next Phase
Phase 7: Analytics Dashboard