# Phase 1: Development Setup

## Objective
Set up the Django project with proper structure, configuration, and database.

## Duration
2-3 hours

## Dependencies
- Python 3.11+
- PostgreSQL (Neon)
- Git

## Tasks

### Task 1.1: Project Initialization
```bash
# Create project structure
mkdir -p AMWPortfolio
cd AMWPortfolio

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install Django
pip install django==6.0.7

# Create Django project
django-admin startproject config .

# Create apps directory
mkdir -p apps

# Create individual apps
python manage.py startapp core apps/core
python manage.py startapp humans apps/humans
python manage.py startapp skills apps/skills
python manage.py startapp projects apps/projects
python manage.py startapp blog apps/blog
python manage.py startapp analytics apps/analytics
```

### Task 1.2: Settings Configuration
```python
# config/settings/base.py
import os
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Security
SECRET_KEY = config('SECRET_KEY', default='unsafe-secret-key')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())

# Application definition
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
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='portfolio'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default='password'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'humans.User'

# Login URLs
LOGIN_URL = 'humans:login'
LOGIN_REDIRECT_URL = 'core:homepage'
LOGOUT_REDIRECT_URL = 'core:homepage'
```

### Task 1.3: Database Configuration
```python
# config/settings/development.py
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

# Use local database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='portfolio_dev'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default='password'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Debug toolbar
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']
```

### Task 1.4: Requirements Setup
```txt
# requirements/base.txt
django==6.0.7
psycopg2-binary==2.9.9
python-decouple==3.8
Pillow==10.2.0
django-taggit==5.0.1
django-markdownx==4.0.7
gunicorn==21.2.0
whitenoise==6.6.0
boto3==1.34.25
django-storages==1.14.2
dj-database-url==2.1.0

# requirements/dev.txt
-r base.txt
django-debug-toolbar==4.2.0
pytest==7.4.3
pytest-django==4.5.2
pytest-cov==4.1.0
factory-boy==3.3.0
faker==20.1.0

# requirements/prod.txt
-r base.txt
sentry-sdk==1.39.1
```

### Task 1.5: Git Setup
```bash
# Initialize git
git init

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
*.egg-info/
dist/
build/

# Django
*.log
local_settings.py
db.sqlite3
media/
staticfiles/

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF

# Create .env.example
cat > .env.example << 'EOF'
DJANGO_SETTINGS_MODULE=config.settings.development
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=*

# Database
DB_NAME=portfolio_dev
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
EOF

# Initial commit
git add .
git commit -m "Initial project setup"
```

## Verification
- [ ] Project structure created
- [ ] Settings configured
- [ ] Database connected
- [ ] Requirements installed
- [ ] Git initialized

## Next Phase
Phase 2: Data Models
