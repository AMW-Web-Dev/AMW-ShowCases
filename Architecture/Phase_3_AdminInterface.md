# Phase 3: Admin Interface

## Objective
Create a customized admin interface for easy content management.

## Duration
2-3 hours

## Dependencies
- Phase 2: Data Models

## Tasks

### Task 3.1: Admin Customization
```python
# apps/humans/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['username']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('bio', 'avatar', 'website', 'github', 'linkedin')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('bio', 'avatar', 'website', 'github', 'linkedin')
        }),
    )
```

### Task 3.2: Skills Admin Enhancement
```python
# apps/skills/admin.py
from django.contrib import admin
from .models import SkillCategory, Skill

class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1
    prepopulated_fields = {'slug': ('name',)}

@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'skill_count']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SkillInline]
    
    def skill_count(self, obj):
        return obj.skills.count()
    skill_count.short_description = 'Skills'

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'years_experience', 'featured', 'order']
    list_filter = ['category', 'featured']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['proficiency', 'featured', 'order']
```

### Task 3.3: Projects Admin Enhancement
```python
# apps/projects/admin.py
from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'featured', 'order', 'created_at', 'updated_at']
    list_filter = ['featured', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['technologies']
    list_editable = ['featured', 'order']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'description', 'long_description')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Links', {
            'fields': ('github_url', 'live_url')
        }),
        ('Technologies', {
            'fields': ('technologies',)
        }),
        ('Settings', {
            'fields': ('featured', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
```

### Task 3.4: Blog Admin Enhancement
```python
# apps/blog/admin.py
from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'published_at', 'created_at', 'tag_list']
    list_filter = ['is_published', 'author', 'tags']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    list_editable = ['is_published']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'excerpt')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Metadata', {
            'fields': ('author', 'tags', 'is_published', 'published_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def tag_list(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()[:3]])
    tag_list.short_description = 'Tags'
    
    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)
```

### Task 3.5: Analytics Admin Enhancement
```python
# apps/analytics/admin.py
from django.contrib import admin
from .models import PageView, Visitor

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ['path', 'ip_address', 'referrer', 'created_at']
    list_filter = ['created_at']
    search_fields = ['path', 'ip_address']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        return False  # Prevent manual creation

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'first_visit', 'last_visit', 'visit_count']
    list_filter = ['first_visit']
    readonly_fields = ['first_visit', 'last_visit']
    date_hierarchy = 'first_visit'
    
    def has_add_permission(self, request):
        return False  # Prevent manual creation
```

### Task 3.6: Admin Site Customization
```python
# config/admin.py
from django.contrib import admin

admin.site.site_header = 'AMW Portfolio Admin'
admin.site.site_title = 'Portfolio Admin'
admin.site.index_title = 'Welcome to Portfolio Admin'

# Custom admin templates
# templates/admin/base_site.html
{% extends "admin/base.html" %}

{% block title %}{{ title }} | Portfolio Admin{% endblock %}

{% block branding %}
<h1 id="site-name">
    <a href="{% url 'admin:index' %}">AMW Portfolio Admin</a>
</h1>
{% endblock %}

{% block nav-global %}{% endblock %}
```

## Verification
- [ ] Admin interface customized
- [ ] All models accessible
- [ ] Search and filters working
- [ ] Inline editing working

## Commands
```bash
# Test admin
python manage.py runserver
# Visit http://localhost:8000/admin/
```

## Next Phase
Phase 4: Blog System
