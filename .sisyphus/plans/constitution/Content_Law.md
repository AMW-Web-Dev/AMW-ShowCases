# Content Constitution

## Content Philosophy
- **Professional narrative**: Showcase expertise and journey
- **Clean formatting**: Consistent Markdown structure
- **SEO-friendly**: Proper headings, meta descriptions
- **Easy to update**: Simple admin interface

## Blog Content Law

### Markdown Standards
```markdown
---
title: "Blog Post Title"
description: "Brief description for SEO"
date: 2025-01-15
tags: [django, python, tutorial]
image: /media/blog/post-image.jpg
---

# Introduction

Brief introduction paragraph.

## Section 1

Content with **bold** and *italic* text.

### Code Blocks

```python
def hello_world():
    print("Hello, World!")
```

### Lists

- Item 1
- Item 2
- Item 3

### Links

[Link text](https://example.com)

### Images

![Alt text](/media/blog/image.jpg)

## Conclusion

Summary paragraph.
```

### Tag System
```python
# Tag naming conventions
# - lowercase
# - hyphens for spaces (e.g., "machine-learning")
# - max 30 characters
# - max 10 tags per post

# Tag categories
TAG_CATEGORIES = {
    'technology': ['django', 'python', 'javascript', 'htmx'],
    'topic': ['tutorial', 'guide', 'tips', 'best-practices'],
    'level': ['beginner', 'intermediate', 'advanced'],
}
```

### Blog Post Structure
```markdown
# Title (H1)

Brief introduction (2-3 sentences).

## Problem (H2)

What problem does this solve?

## Solution (H2)

How to solve it.

### Step 1 (H3)

Detailed instructions.

### Step 2 (H3)

More instructions.

## Results (H2)

What was achieved.

## Conclusion (H2)

Key takeaways.

## Further Reading (H2)

- [Link 1](url)
- [Link 2](url)
```

## Skills Content Law

### Skill Categories
```python
SKILL_CATEGORIES = [
    ('devops', 'DevOps & Cloud'),
    ('linux', 'Linux & Systems'),
    ('python', 'Python & Backend'),
    ('data', 'Data & Analytics'),
    ('shopify', 'Shopify & E-commerce'),
    ('django', 'Django & Web'),
    ('frontend', 'Frontend & UI'),
    ('scripting', 'Scripting & Automation'),
]
```

### Skill Format
```python
# Skill entry
{
    'name': 'Django',
    'category': 'django',
    'proficiency': 90,  # 0-100
    'years_experience': 5,
    'description': 'Web framework for Python',
    'icon': 'bi-code-slash',  # Bootstrap Icons class
    'featured': True,
    'order': 1,
}
```

### Skill Grouping
```html
<!-- Skills by category -->
<div class="skill-category">
    <h3>DevOps & Cloud</h3>
    <div class="skill-items">
        <div class="skill-item">
            <span class="skill-name">Docker</span>
            <div class="skill-bar" style="width: 85%"></div>
        </div>
    </div>
</div>
```

## Projects Content Law

### Project Entry Format
```python
{
    'title': 'Project Name',
    'slug': 'project-name',
    'description': 'Brief description',
    'long_description': 'Detailed description in Markdown',
    'image': '/media/projects/project-image.jpg',
    'github_url': 'https://github.com/amw/portfolio',
    'live_url': 'https://portfolio.amw.com',
    'technologies': ['Django', 'HTMX', 'PostgreSQL'],
    'featured': True,
    'order': 1,
    'created_at': '2025-01-15',
}
```

### Project Showcase Structure
```markdown
# Project Name

Brief description (1-2 sentences).

## Features

- Feature 1
- Feature 2
- Feature 3

## Technologies

- Django 6.0.7
- HTMX 1.28.0
- PostgreSQL

## Screenshots

![Screenshot 1](/media/projects/screenshot1.jpg)

## Links

- [GitHub](https://github.com/amw/project)
- [Live Demo](https://project.amw.com)
```

## Images Content Law

### Image Naming
```bash
# Pattern: {type}-{name}-{size}.{ext}
blog-django-tutorial-1200x800.jpg
projects-portfolio-preview-1920x1080.jpg
skills-python-icon-256x256.png
```

### Image Sizes
```python
# Blog images
BLOG_IMAGE_SIZES = {
    'thumbnail': (400, 300),
    'medium': (800, 600),
    'large': (1200, 800),
    'hero': (1920, 1080),
}

# Project images
PROJECT_IMAGE_SIZES = {
    'thumbnail': (400, 300),
    'preview': (800, 600),
    'full': (1920, 1080),
}

# Skill icons (using Bootstrap Icons, not images)
SKILL_ICON_SIZE = (256, 256)  # For favicon/og-image
```

### Image Optimization
```python
# Pillow processing
from PIL import Image

def optimize_image(image_path, max_width=1200):
    """Optimize image for web."""
    img = Image.open(image_path)
    
    # Convert to WebP if not already
    if img.format != 'WEBP':
        img = img.convert('RGB')
    
    # Resize if too wide
    if img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.LANCZOS)
    
    # Save optimized
    img.save(image_path, 'WEBP', optimize=True, quality=85)
```

### Image Upload Rules
```python
# File upload validation
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

# Image field settings
image = models.ImageField(
    upload_to='blog/%Y/%m/',
    validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
    max_length=255
)
```

## Professional Summary Law

### Summary Format
```markdown
# Professional Summary

[Role] with [X] years of experience in [technologies/domains].

## Specializations

- **DevOps**: Docker, Kubernetes, CI/CD, Cloud Infrastructure
- **Backend**: Python, Django, PostgreSQL, REST APIs
- **Automation**: Shell scripting, workflow optimization

## Current Focus

- Building scalable web applications
- Automating development workflows
- Contributing to open source projects

## Contact

- Email: amw@example.com
- GitHub: github.com/amw
- LinkedIn: linkedin.com/in/amw
```

## CV/Resume Content Law

### CV Structure
```markdown
# CV Structure

## Header
- Name
- Title
- Contact info

## Summary
- 2-3 sentences
- Key expertise areas

## Experience
- Job title
- Company
- Duration
- Key achievements (bullet points)

## Skills
- Technical skills grouped by category
- Proficiency levels

## Education
- Degree
- Institution
- Year

## Certifications
- Certification name
- Issuing organization
- Date
```

### CV File Format
```python
# CV file storage
CV_FILE_FORMATS = {
    'pdf': 'CV-AMW-2025.pdf',
    'docx': 'CV-AMW-2025.docx',
    'txt': 'CV-AMW-2025.txt',  # Plain text version
}

# CV storage location
CV_UPLOAD_TO = 'cv/%Y/%m/'
```

## SEO Content Law

### Meta Tags
```html
<!-- Blog post meta -->
<meta name="title" content="{{ post.title }}">
<meta name="description" content="{{ post.excerpt|default:post.content|truncatewords:30 }}">
<meta name="keywords" content="{{ post.tags|join:', ' }}">

<!-- Open Graph -->
<meta property="og:title" content="{{ post.title }}">
<meta property="og:description" content="{{ post.excerpt|default:post.content|truncatewords:30 }}">
<meta property="og:image" content="{{ request.scheme }}://{{ request.get_host }}{{ post.image.url }}">
<meta property="og:type" content="article">
<meta property="og:url" content="{{ request.build_absolute_uri }}">

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{{ post.title }}">
<meta name="twitter:description" content="{{ post.excerpt|default:post.content|truncatewords:30 }}">
<meta name="twitter:image" content="{{ request.scheme }}://{{ request.get_host }}{{ post.image.url }}">
```

### URL Structure
```python
# SEO-friendly URLs
urlpatterns = [
    path('blog/', blog.BlogListView.as_view(), name='list'),
    path('blog/create/', blog.BlogCreateView.as_view(), name='create'),
    path('blog/<slug:slug>/', blog.BlogDetailView.as_view(), name='detail'),
    path('blog/<slug:slug>/update/', blog.BlogUpdateView.as_view(), name='update'),
    path('blog/<slug:slug>/delete/', blog.BlogDeleteView.as_view(), name='delete'),
    path('blog/tag/<slug:tag_slug>/', blog.blog_tag_view, name='tag'),
    path('projects/', projects.ProjectsListView.as_view(), name='list'),
    path('projects/<slug:slug>/', projects.ProjectDetailView.as_view(), name='detail'),
]
```

### Schema.org Markup
```html
<!-- Article schema -->
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{{ post.title }}",
    "description": "{{ post.excerpt|default:post.content|truncatewords:30 }}",
    "image": "{{ request.scheme }}://{{ request.get_host }}{{ post.image.url }}",
    "datePublished": "{{ post.published_at|date:'Y-m-d' }}",
    "author": {
        "@type": "Person",
        "name": "AMW"
    }
}
</script>
```

## Content Quality Law

### Writing Standards
- **Clarity**: Write for your audience (technical but accessible)
- **Conciseness**: Get to the point quickly
- **Accuracy**: Test all code examples
- **Consistency**: Follow the same style throughout

### Code Examples
```markdown
<!-- Code block format -->
```python
# Always include language identifier
# Add comments for complex logic
# Keep examples focused and complete
def example_function():
    """Docstring explaining what this does."""
    # Implementation
    return result
```
```

### Content Review Checklist
- [ ] Spelling and grammar check
- [ ] Code examples tested
- [ ] Links verified
- [ ] Images optimized
- [ ] Meta tags complete
- [ ] Mobile responsive
- [ ] Accessibility checked

## Content Update Law

### Update Process
1. **Draft**: Write in admin interface
2. **Preview**: Check rendering
3. **Publish**: Make live
4. **Share**: Social media promotion

### Version Control
```python
# Content versioning
class BlogPost(models.Model):
    # ... fields ...
    version = models.IntegerField(default=1)
    is_published = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.pk:
            self.version += 1
        super().save(*args, **kwargs)
```

### Backup Strategy
```bash
# Regular content backups
python manage.py dumpdata blog --indent 2 > blog_backup.json

# Media file backups
aws s3 sync media/ s3://backup-bucket/media/
```