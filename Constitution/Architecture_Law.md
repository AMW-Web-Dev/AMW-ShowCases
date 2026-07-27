# Architecture Constitution

## Project Identity
- **Name**: AMW Portfolio Showcase
- **Purpose**: Professional portfolio website showcasing skills, projects, and technical expertise
- **Tech Stack**: Django 6.0.7 + HTMX 1.28.0 + PostgreSQL (Neon) + CloudFlare R2
- **Hosting**: Render (app) + Neon (database) + CloudFlare R2 (static files/CV)

## Project Structure Law

```
AMWPortfolio/
├── apps/                          # All Django apps
│   ├── core/                      # Core app (homepage, shared utilities)
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── core.py               # views (renamed from views.py)
│   │   ├── urls.py
│   │   └── templates/
│   │       └── core/
│   │           ├── base.html
│   │           ├── homepage.html
│   │           └── components/
│   ├── humans/                    # Authentication (renamed from accounts)
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── humans.py             # views (renamed from views.py)
│   │   ├── urls.py
│   │   ├── forms.py
│   │   └── templates/
│   │       └── humans/
│   │           ├── login.html
│   │           ├── register.html
│   │           └── profile.html
│   ├── skills/                    # Skills management
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── skills.py             # views (renamed from views.py)
│   │   ├── urls.py
│   │   └── templates/
│   │       └── skills/
│   │           ├── skills_list.html
│   │           └── components/
│   ├── projects/                  # Project showcase
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── projects.py           # views (renamed from views.py)
│   │   ├── urls.py
│   │   └── templates/
│   │       └── projects/
│   │           ├── projects_list.html
│   │           ├── project_detail.html
│   │           └── components/
│   ├── blog/                      # Blog with Markdown/tags
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── blog.py               # views (renamed from views.py)
│   │   ├── urls.py
│   │   ├── forms.py
│   │   └── templates/
│   │       └── blog/
│   │           ├── blog_list.html
│   │           ├── blog_detail.html
│   │           ├── blog_tag.html
│   │           └── components/
│   └── analytics/                 # Analytics dashboard
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── analytics.py           # views (renamed from views.py)
│       ├── urls.py
│       └── templates/
│           └── analytics/
│               ├── dashboard.html
│               └── components/
├── config/                        # Configuration
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py               # Shared settings
│   │   ├── development.py         # Development settings
│   │   ├── production.py          # Production settings
│   │   └── local.py              # Local overrides
│   ├── urls.py                    # Main URL conf
│   └── wsgi.py
├── static/                        # Static files (local)
│   ├── css/
│   ├── js/
│   └── images/
├── media/                         # Media files (local)
├── templates/                     # Global templates
│   └── base.html
├── requirements/                  # Requirements split
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── .env.example
├── .gitignore
└── README.md
```

## Naming Conventions Law

### Files
- **views.py** → `{app_name}.py` (e.g., `blog.py`, `humans.py`, `skills.py`)
- **Models**: Singular PascalCase (e.g., `Skill`, `Project`, `BlogPost`)
- **Templates**: `snake_case.html` (e.g., `blog_detail.html`, `skills_list.html`)

### Functions & Classes
- **CBV**: PascalCase with `View` suffix (e.g., `BlogListView`, `ProjectDetailView`)
- **Functions**: `snake_case` with `_view` suffix (e.g., `blog_list_view`, `project_detail_view`)
- **URL names**: `snake_case` (e.g., `blog:list`, `blog:detail`)

### Database
- **Tables**: `snake_case` (e.g., `blog_posts`, `skills_skill`)
- **Fields**: `snake_case` (e.g., `created_at`, `updated_at`)
- **Relations**: Use `related_name` (e.g., `related_name='posts'`)

## Tech Stack Law

### Backend
- **Django 6.0.7**: Latest stable LTS
- **PostgreSQL**: Neon free tier (512MB, permanent)
- **django-taggit**: Blog tagging
- **django-markdownx**: Markdown rendering
- **Pillow**: Image processing

### Frontend
- **HTMX 1.28.0**: Dynamic interactions
- **Bootstrap 5.3.0**: CSS framework (via CDN)
- **Highlight.js**: Code syntax highlighting
- **No React/Vue**: Keep it simple and professional

### Hosting
- **Render**: Free tier for Django app
- **Neon**: Free PostgreSQL (permanent, no credit card)
- **CloudFlare R2**: Free 10GB storage (CV files, images)

## Import Law

```python
# Always use absolute imports
from apps.blog.models import BlogPost
from apps.skills.models import Skill

# Never use relative imports
# from .models import BlogPost  # FORBIDDEN
```

## Settings Law

```python
# config/settings/base.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party
    'taggit',
    'markdownx',
    # Local apps
    'apps.core',
    'apps.humans',
    'apps.skills',
    'apps.projects',
    'apps.blog',
    'apps.analytics',
]

# Split settings
# development.py: DEBUG=True, local database
# production.py: DEBUG=False, Neon database
# local.py: Personal overrides (never committed)
```

## URL Structure Law

```python
# config/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('auth/', include('apps.humans.urls')),
    path('skills/', include('apps.skills.urls')),
    path('projects/', include('apps.projects.urls')),
    path('blog/', include('apps.blog.urls')),
    path('dashboard/', include('apps.analytics.urls')),
]

# Each app has its own urls.py
# Use namespaces: app_name = 'blog'
```

## Error Handling Law

```python
# Custom 404 page
# Custom 500 page
# Graceful fallbacks for missing images
# Never expose sensitive error details in production
```

## Security Law

- **SECRET_KEY**: Environment variable, never committed
- **DEBUG**: False in production
- **ALLOWED_HOSTS**: Render domain + custom domain
- **CSRF**: Always enabled
- **HTTPS**: Enforced in production
- **File uploads**: Validate and sanitize

## Performance Law

- **Static files**: CloudFlare R2 (CDN)
- **Database queries**: Use `select_related()` and `prefetch_related()`
- **Caching**: Django cache framework for expensive queries
- **Images**: Optimize before upload, use WebP format
- **Lazy loading**: HTMX for dynamic content

## Version Control Law

- **Git**: Version control for all code
- **Branches**: `main` (production), `develop` (development), `feature/*` (features)
- **Commits**: Conventional commits format
- **.env**: Never committed, use `.env.example`
- **media/**: Never committed (user uploads)
- **staticfiles/**: Never committed (generated)

## Documentation Law

- **README.md**: Setup, usage, deployment
- **No docs/ directory**: Everything in README.md
- **Code comments**: Explain WHY, not WHAT
- **Docstrings**: For public functions and classes

## Testing Law

- **Framework**: Django TestCase + pytest-django
- **Coverage**: Minimum 80% for new code
- **Types**: Unit tests, integration tests, model tests
- **No frontend tests**: Keep it simple for portfolio
