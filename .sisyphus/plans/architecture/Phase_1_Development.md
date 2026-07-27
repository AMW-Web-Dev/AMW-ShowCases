# Phase 1: Development Setup

## Objective
Set up the Django project with proper structure, configuration, and database.

## Duration
2-3 hours

## Dependencies
- Python 3.11+
- PostgreSQL (Neon) - or local PostgreSQL for development
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
    'apps.analytics.middleware.AnalyticsMiddleware',
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

# Markdownx
MARKDOWNX_URLS_PATH = '/markdownx/markdownify/'
MARKDOWNX_UPLOAD_URLS_PATH = '/markdownx/upload/'
MARKDOWNX_EDITOR_RESIZABLE = True
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

```python
# config/settings/production.py
import os
from .base import *
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True,
    )
}

# Security
SECURITY_BROWSER_XSS_FILTER = True
SECURITY_CONTENT_TYPE_NOSNIFF = True
SECURITY_HSTS_SECONDS = 31536000
SECURITY_HSTS_INCLUDE_SUBDOMAINS = True
SECURITY_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# CloudFlare R2 for media
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.environ.get('R2_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('R2_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('R2_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = os.environ.get('R2_ENDPOINT_URL')
AWS_S3_REGION_NAME = 'auto'
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_ADDRESSING_STYLE = 'virtual'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Sentry (optional)
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
    send_default_pii=True,
)
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

# Create render.yaml
cat > render.yaml << 'EOF'
services:
  - type: web
    name: amw-portfolio
    env: python
    buildCommand: pip install -r requirements/prod.txt && python manage.py collectstatic --noinput
    startCommand: gunicorn config.wsgi:application
    autoDeploy: true
    branch: main
    envVars:
      - key: DJANGO_SETTINGS_MODULE
        value: config.settings.production
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: amw-portfolio-db
          property: connectionString
      - key: R2_ACCESS_KEY_ID
        sync: false
      - key: R2_SECRET_ACCESS_KEY
        sync: false
      - key: R2_BUCKET_NAME
        sync: false
      - key: R2_ENDPOINT_URL
        sync: false

databases:
  - name: amw-portfolio-db
    plan: free
    databaseName: portfolio
EOF

# Initial commit
git add .
git commit -m "Initial project setup"
```

## Verification
- [ ] Project structure created
- [ ] Settings configured (base, development, production)
- [ ] Database connected
- [ ] Requirements installed
- [ ] Git initialized
- [ ] render.yaml created

## Next Phase
Phase 2: Data Models