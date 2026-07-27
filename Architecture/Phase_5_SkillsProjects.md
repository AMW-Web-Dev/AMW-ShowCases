# Phase 5: Skills & Projects

## Objective
Create skills management and project showcase features.

## Duration
3-4 hours

## Dependencies
- Phase 2: Data Models
- Phase 3: Admin Interface

## Tasks

### Task 5.1: Skills Views
```python
# apps/skills/skills.py
from django.shortcuts import render
from django.views.generic import ListView
from .models import SkillCategory, Skill

class SkillsListView(ListView):
    model = SkillCategory
    template_name = 'skills/skills_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return SkillCategory.objects.prefetch_related('skills').order_by('order')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_skills'] = Skill.objects.filter(featured=True)
        return context
```

### Task 5.2: Skills URLs
```python
# apps/skills/urls.py
from django.urls import path
from . import skills

app_name = 'skills'

urlpatterns = [
    path('', skills.SkillsListView.as_view(), name='list'),
]
```

### Task 5.3: Skills Templates
```html
<!-- templates/skills/skills_list.html -->
{% extends 'base.html' %}

{% block title %}Skills - AMW Portfolio{% endblock %}

{% block content %}
<div class="container">
    <h1 class="mb-4">Skills & Expertise</h1>
    
    {% if featured_skills %}
    <div class="mb-5">
        <h2 class="h3 mb-3">Featured Skills</h2>
        <div class="row">
            {% for skill in featured_skills %}
            <div class="col-md-4 mb-3">
                <div class="card text-center">
                    <div class="card-body">
                        <h5 class="card-title">{{ skill.name }}</h5>
                        <div class="progress mb-2" style="height: 20px;">
                            <div class="progress-bar bg-primary" role="progressbar" 
                                 style="width: {{ skill.proficiency }}%"
                                 aria-valuenow="{{ skill.proficiency }}" 
                                 aria-valuemin="0" 
                                 aria-valuemax="100">
                                {{ skill.proficiency }}%
                            </div>
                        </div>
                        <small class="text-muted">{{ skill.years_experience }} years experience</small>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    {% endif %}
    
    {% for category in categories %}
    <div class="mb-5">
        <h2 class="h3 mb-3">{{ category.name }}</h2>
        {% if category.description %}
        <p class="text-muted">{{ category.description }}</p>
        {% endif %}
        
        <div class="row">
            {% for skill in category.skills.all %}
            <div class="col-md-6 mb-3">
                <div class="card">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <h5 class="card-title mb-0">{{ skill.name }}</h5>
                            <span class="badge bg-primary">{{ skill.proficiency }}%</span>
                        </div>
                        <div class="progress mb-2" style="height: 10px;">
                            <div class="progress-bar bg-primary" role="progressbar" 
                                 style="width: {{ skill.proficiency }}%"
                                 aria-valuenow="{{ skill.proficiency }}" 
                                 aria-valuemin="0" 
                                 aria-valuemax="100">
                            </div>
                        </div>
                        <small class="text-muted">
                            {{ skill.years_experience }} years experience
                        </small>
                        {% if skill.description %}
                        <p class="mt-2 mb-0 small">{{ skill.description }}</p>
                        {% endif %}
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}
```

### Task 5.4: Projects Views
```python
# apps/projects/projects.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Project

class ProjectsListView(ListView):
    model = Project
    template_name = 'projects/projects_list.html'
    context_object_name = 'projects'
    paginate_by = 12
    
    def get_queryset(self):
        return Project.objects.prefetch_related('technologies')

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
```

### Task 5.5: Projects URLs
```python
# apps/projects/urls.py
from django.urls import path
from . import projects

app_name = 'projects'

urlpatterns = [
    path('', projects.ProjectsListView.as_view(), name='list'),
    path('<slug:slug>/', projects.ProjectDetailView.as_view(), name='detail'),
]
```

### Task 5.6: Projects Templates
```html
<!-- templates/projects/projects_list.html -->
{% extends 'base.html' %}

{% block title %}Projects - AMW Portfolio{% endblock %}

{% block content %}
<div class="container">
    <h1 class="mb-4">Projects</h1>
    
    <div class="row">
        {% for project in projects %}
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="card h-100">
                {% if project.image %}
                <img src="{{ project.image.url }}" class="card-img-top" alt="{{ project.title }}">
                {% endif %}
                <div class="card-body">
                    <h5 class="card-title">{{ project.title }}</h5>
                    <p class="card-text">{{ project.description|truncatewords:20 }}</p>
                    <div class="mb-2">
                        {% for tech in project.technologies.all %}
                        <span class="badge bg-secondary">{{ tech.name }}</span>
                        {% endfor %}
                    </div>
                </div>
                <div class="card-footer">
                    <div class="d-flex justify-content-between">
                        {% if project.github_url %}
                        <a href="{{ project.github_url }}" class="btn btn-outline-secondary btn-sm" target="_blank">
                            <i class="bi bi-github"></i> GitHub
                        </a>
                        {% endif %}
                        {% if project.live_url %}
                        <a href="{{ project.live_url }}" class="btn btn-primary btn-sm" target="_blank">
                            <i class="bi bi-box-arrow-up-right"></i> Live Demo
                        </a>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
        {% empty %}
        <div class="col-12">
            <p>No projects yet.</p>
        </div>
        {% endfor %}
    </div>
    
    {% if is_paginated %}
    <nav aria-label="Projects pagination">
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
<!-- templates/projects/project_detail.html -->
{% extends 'base.html' %}

{% block title %}{{ project.title }} - AMW Portfolio{% endblock %}

{% block content %}
<div class="container">
    <article class="mt-4">
        <header class="mb-4">
            <h1>{{ project.title }}</h1>
            <div class="mb-3">
                {% for tech in project.technologies.all %}
                <span class="badge bg-primary">{{ tech.name }}</span>
                {% endfor %}
            </div>
        </header>
        
        {% if project.image %}
        <img src="{{ project.image.url }}" class="img-fluid rounded mb-4" alt="{{ project.title }}">
        {% endif %}
        
        <div class="project-content mb-4">
            {{ project.long_description|default:project.content|linebreaks }}
        </div>
        
        <div class="d-flex gap-2 mb-4">
            {% if project.github_url %}
            <a href="{{ project.github_url }}" class="btn btn-outline-secondary" target="_blank">
                <i class="bi bi-github"></i> View on GitHub
            </a>
            {% endif %}
            {% if project.live_url %}
            <a href="{{ project.live_url }}" class="btn btn-primary" target="_blank">
                <i class="bi bi-box-arrow-up-right"></i> Live Demo
            </a>
            {% endif %}
        </div>
    </article>
    
    <hr class="my-4">
    
    <a href="{% url 'projects:list' %}" class="btn btn-outline-secondary">← Back to Projects</a>
</div>
{% endblock %}
```

### Task 5.7: Skills CSS
```css
/* static/css/skills.css */
.skill-bar {
    height: 10px;
    background-color: #e9ecef;
    border-radius: 5px;
    overflow: hidden;
}

.skill-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #2563eb, #3b82f6);
    border-radius: 5px;
    transition: width 0.5s ease-in-out;
}

.skill-card {
    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.skill-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
```

## Verification
- [ ] Skills list page working
- [ ] Projects list page working
- [ ] Project detail page working
- [ ] Filtering and pagination working

## Commands
```bash
# Test skills and projects
python manage.py runserver
# Visit http://localhost:8000/skills/
# Visit http://localhost:8000/projects/
# Add data via admin: http://localhost:8000/admin/
```

## Next Phase
Phase 6: Core App & Homepage
