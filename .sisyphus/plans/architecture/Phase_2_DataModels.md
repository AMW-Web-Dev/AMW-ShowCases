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
    category = models.ForeignKey(
        SkillCategory, 
        on_delete=models.CASCADE, 
        related_name='skills'
    )
    proficiency = models.IntegerField(default=0)  # 0-100
    years_experience = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)  # Bootstrap Icons class
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
    technologies = models.ManyToManyField(
        'skills.Skill', 
        blank=True, 
        related_name='projects'
    )
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
    author = models.ForeignKey(
        'humans.User', 
        on_delete=models.CASCADE, 
        related_name='blog_posts'
    )
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
    
    @property
    def is_published_now(self):
        from django.utils import timezone
        if self.published_at:
            return self.published_at <= timezone.now()
        return self.is_published
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
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['username']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('bio', 'avatar', 'website', 'github', 'linkedin')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('bio', 'avatar', 'website', 'github', 'linkedin')}),
    )

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

# config/admin.py
from django.contrib import admin

admin.site.site_header = 'AMW Portfolio Admin'
admin.site.site_title = 'Portfolio Admin'
admin.site.index_title = 'Welcome to Portfolio Admin'
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