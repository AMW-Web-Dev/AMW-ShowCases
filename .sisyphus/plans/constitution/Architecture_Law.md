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
│   │   ├── context_processors.py # current_year, etc.
│   │   └── templates/
│   │       └── core/
│   │           ├── base.html
│   │           ├── homepage.html
│   │           ├── about.html
│   │           ├── contact.html
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
│   │   ├── templatetags/
│   │   │   ├── __init__.py
│   │   │   └── markdown.py
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
│       ├── middleware.py
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
│   │   └── local.py              # Local overrides (never committed)
│   ├── urls.py                    # Main URL conf
│   ├── wsgi.py
│   └── admin.py                   # Admin site customization
├── static/                        # Static files (local)
│   ├── css/
│   │   ├── custom.css
│   │   ├── variables.css
│   │   ├── components/
│   │   │   ├── cards.css
│   │   │   ├── navigation.css
│   │   │   ├── forms.css
│   │   │   └── loading.css
│   ├── js/
│   │   ├── custom.js
│   │   └── components/
│   │       ├── animations.js
│   │       └── forms.js
│   └── images/
│       ├── logo.png
│       ├── favicon.ico
│       └── og-image.png
├── media/                         # Media files (local dev only)
├── templates/                     # Global templates (error pages, etc.)
│   ├── 404.html
│   ├── 500.html
│   └── robots.txt
├── requirements/                  # Requirements split
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── .env.example
├── .gitignore
├── render.yaml
├── README.md
└── manage.py
```

## Naming Conventions Law

### Files
- **views.py** → `{app_name}.py` (e.g., `blog.py`, `humans.py`, `skills.py`, `projects.py`, `core.py`, `analytics.py`)
- **Models**: Singular PascalCase (e.g., `Skill`, `Project`, `BlogPost`, `SkillCategory`)
- **Templates**: `snake_case.html` (e.g., `blog_detail.html`, `skills_list.html`)

### Functions & Classes
- **CBV**: PascalCase with `View` suffix (e.g., `BlogListView`, `ProjectDetailView`, `HomepageView`)
- **Functions**: `snake_case` with `_view` suffix (e.g., `blog_tag_view`, `contact_view`)
- **URL names**: `snake_case` (e.g., `blog:list`, `blog:detail`, `blog:tag`)

### Database
- **Tables**: `snake_case` (e.g., `blog_posts`, `skills_skill`)
- **Fields**: `snake_case` (e.g., `created_at`, `updated_at`, `is_published`)
- **Relations**: Use `related_name` (e.g., `related_name='posts'`, `related_name='projects'`)

## Tech Stack Law

### Backend
- **Django 6.0.7**: Latest stable LTS
- **PostgreSQL**: Neon free tier (512MB, permanent)
- **django-taggit**: Blog tagging
- **django-markdownx**: Markdown rendering with code highlighting
- **Pillow**: Image processing
- **gunicorn**: WSGI server
- **whitenoise**: Static file serving
- **dj-database-url**: Database URL parsing
- **django-storages + boto3**: CloudFlare R2 integration

### Frontend
- **HTMX 1.28.0**: Dynamic interactions via CDN
- **Bootstrap 5.3.0**: CSS framework via CDN
- **Bootstrap Icons 1.11.0**: Icons via CDN
- **Highlight.js 11.9.0**: Code syntax highlighting via CDN
- **Chart.js 4.4.0**: Analytics charts via CDN
- **No React/Vue**: Keep it simple and professional

### Hosting
- **Render**: Free tier for Django app
- **Neon**: Free PostgreSQL (permanent, no credit card)
- **CloudFlare R2**: Free 10GB storage (CV files, images)

## Import Law

```python
# Always use absolute imports from apps
from apps.blog.models import BlogPost
from apps.skills.models import Skill
from apps.projects.models import Project
from apps.humans.models import User

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

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.analytics.middleware.AnalyticsMiddleware',
]

# Split settings
# development.py: DEBUG=True, local database, debug_toolbar
# production.py: DEBUG=False, Neon database, security headers
# local.py: Personal overrides (never committed)
```

## URL Structure Law

```python
# config/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('markdownx/', include('markdownx.urls')),  # Required for markdownx
    path('', include('apps.core.urls')),
    path('auth/', include('apps.humans.urls')),
    path('skills/', include('apps.skills.urls')),
    path('projects/', include('apps.projects.urls')),
    path('blog/', include('apps.blog.urls')),
    path('dashboard/', include('apps.analytics.urls')),
]

# Each app has its own urls.py with namespace
# app_name = 'blog'
```

## Error Handling Law

- Custom 404 page (`templates/404.html`)
- Custom 500 page (`templates/500.html`)
- Graceful fallbacks for missing images
- Never expose sensitive error details in production

## Security Law

- **SECRET_KEY**: Environment variable, never committed
- **DEBUG**: False in production
- **ALLOWED_HOSTS**: Render domain + custom domain
- **CSRF**: Always enabled
- **HTTPS**: Enforced in production
- **File uploads**: Validate and sanitize
- **SECURE_PROXY_SSL_HEADER**: Required for Render proxy

## Performance Law

- **Static files**: CloudFlare R2 (CDN)
- **Database queries**: Use `select_related()` and `prefetch_related()`
- **Caching**: Django cache framework for expensive queries
- **Images**: Optimize before upload, use WebP format
- **Lazy loading**: HTMX for dynamic content
- **Analytics middleware**: Batch writes, not per-request

## Version Control Law

- **Git**: Version control for all code
- **Branches**: `main` (production), `develop` (development), `feature/*` (features)
- **Commits**: Each commit MUST use `git commit -m "Title" -m "Description"` format (separate title and description). Title should be concise (max 72 chars), description provides meaningful context about what was done and why.
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
- **Factories**: Use factory-boy for test data

## Deployment Law

- **render.yaml**: Infrastructure as code
- **Health check endpoint**: `/health/`
- **Auto-deploy**: On push to main branch
- **Migrations**: Run on deploy
- **Collectstatic**: Run on build
- **Superuser**: Create via management command if needed