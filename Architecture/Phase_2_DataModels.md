# Phase 2: Data Models

## Objective
Create all Django models with proper relationships and validation.

## Duration
3-4 hours

## Dependencies
- Phase 1: Development Setup

## Tasks

### Task 2.1: Custom User Model
```python
# apps/humans/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom user model for portfolio."""
    
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    website = models.URLField(max_length=200, blank=True)
    github = models.URLField(max_length=200, blank=True)
    linkedin = models.URLField(max_length=200, blank=True)
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
    
    def __str__(self):
        return self.username
```

### Task 2.2: Skills Models
```python
# apps/skills/models.py
from django.db import models

class SkillCategory(models.Model):
    """Category for skills."""
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'skill categories'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class Skill(models.Model):
    """Individual skill."""
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    proficiency = models.IntegerField(default=0)  # 0-100
    years_experience = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
```

### Task 2.3: Projects Models
```python
# apps/projects/models.py
from django.db import models
from django.utils.text import slugify

class Project(models.Model):
    """Project showcase."""
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    long_description = models.TextField(blank=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    github_url = models.URLField(max_length=200, blank=True)
    live_url = models.URLField(max_length=200, blank=True)
    technologies = models.ManyToManyField('skills.Skill', blank=True, related_name='projects')
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
```

### Task 2.4: Blog Models
```python
# apps/blog/models.py
from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager

class BlogPost(models.Model):
    """Blog post with Markdown support."""
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    author = models.ForeignKey('humans.User', on_delete=models.CASCADE, related_name='blog_posts')
    tags = TaggableManager(blank=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return f'/blog/{self.slug}/'
```

### Task 2.5: Analytics Models
```python
# apps/analytics/models.py
from django.db import models

class PageView(models.Model):
    """Track page views."""
    
    path = models.CharField(max_length=500)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.path} - {self.created_at}'

class Visitor(models.Model):
    """Track unique visitors."""
    
    ip_address = models.GenericIPAddressField(unique=True)
    first_visit = models.DateTimeField(auto_now_add=True)
    last_visit = models.DateTimeField(auto_now=True)
    visit_count = models.IntegerField(default=1)
    
    class Meta:
        ordering = ['-last_visit']
    
    def __str__(self):
        return self.ip_address
```

### Task 2.6: Admin Configuration
```python
# apps/humans/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('bio', 'avatar', 'website', 'github', 'linkedin')}),
    )

# apps/skills/admin.py
from django.contrib import admin
from .models import SkillCategory, Skill

@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'featured', 'order']
    list_filter = ['category', 'featured']
    prepopulated_fields = {'slug': ('name',)}

# apps/projects/admin.py
from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'featured', 'order', 'created_at']
    list_filter = ['featured']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['technologies']

# apps/blog/admin.py
from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'published_at', 'created_at']
    list_filter = ['is_published', 'author']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    date_hierarchy = 'created_at'

# apps/analytics/admin.py
from django.contrib import admin
from .models import PageView, Visitor

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ['path', 'ip_address', 'created_at']
    list_filter = ['created_at']

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'first_visit', 'last_visit', 'visit_count']
```

## Verification
- [ ] All models created
- [ ] Migrations generated
- [ ] Admin configured
- [ ] Database tables created

## Commands
```bash
# Generate migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Test admin
python manage.py runserver
# Visit http://localhost:8000/admin/
```

## Next Phase
Phase 3: Admin Interface
