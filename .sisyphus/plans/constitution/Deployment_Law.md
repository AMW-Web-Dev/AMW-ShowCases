# Deployment Constitution

## Deployment Philosophy
- **Free hosting only**: No AWS, no credit cards
- **Production-ready**: Proper configuration from day one
- **Automated**: CI/CD for deployments
- **Secure**: Environment variables, HTTPS, proper secrets

## Hosting Law

### Render (Free Tier)
```yaml
# render.yaml
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
```

### Neon (Free PostgreSQL)
```python
# config/settings/production.py
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True,
    )
}
```

### CloudFlare R2 (Free Storage)
```python
# CloudFlare R2 configuration
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
# R2-specific settings
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_ADDRESSING_STYLE = 'virtual'
```

## Environment Variables Law

### Required Variables
```bash
# .env.example
DJANGO_SETTINGS_MODULE=config.settings.production
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com

# Database (Neon)
DATABASE_URL=postgres://user:pass@host/dbname?sslmode=require

# CloudFlare R2
R2_ACCESS_KEY_ID=your-r2-access-key
R2_SECRET_ACCESS_KEY=your-r2-secret-key
R2_BUCKET_NAME=your-bucket-name
R2_ENDPOINT_URL=https://your-account.r2.cloudflarestorage.com

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Environment Loading
```python
# config/settings/base.py
import os
from pathlib import Path

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Use python-decouple for environment variables
from decouple import config, Csv

SECRET_KEY = config('SECRET_KEY', default='unsafe-secret-key')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())
```

## Security Law

### Django Security Settings
```python
# config/settings/production.py
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
```

### Secret Key Management
```python
# Generate new secret key for production
from django.core.management.utils import get_random_secret_key

SECRET_KEY = config('SECRET_KEY', default=get_random_secret_key())
```

### CORS Configuration
```python
# config/settings/base.py
INSTALLED_APPS = [
    ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    'https://your-app.onrender.com',
    'https://your-custom-domain.com',
]
```

## Static Files Law

### WhiteNoise Configuration
```python
# config/settings/production.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    ...
]

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Static Files Collection
```bash
# Build command for Render
python manage.py collectstatic --noinput
python manage.py compress --force
```

### CloudFlare R2 for Media
```python
# Media files storage
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Media URL
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.{AWS_S3_ENDPOINT_URL}/media/'
```

## Database Law

### Migration Strategy
```bash
# Run migrations on deploy
python manage.py migrate --noinput

# Create superuser if needed
python manage.py createsuperuser --noinput
```

### Database Backups
```bash
# Neon automatic backups (built-in)
# Manual backup
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Restore
psql $DATABASE_URL < backup_20250115.sql
```

### Connection Pooling
```python
# config/settings/production.py
DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,  # 10 minutes
        conn_health_checks=True,
        ssl_require=True,
    )
}
```

## CI/CD Law

### GitHub Actions Workflow
```yaml
# .github/workflows/deploy.yml
name: Deploy to Render

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements/prod.txt
      
      - name: Run tests
        run: |
          python manage.py test
      
      - name: Collect static files
        run: |
          python manage.py collectstatic --noinput

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Render
        uses: johnbeynon/render-deploy-action@v1.0.0
        with:
          service-id: ${{ secrets.RENDER_SERVICE_ID }}
          api-key: ${{ secrets.RENDER_API_KEY }}
```

### Render Auto-Deploy
```yaml
# render.yaml (already defined above)
services:
  - type: web
    name: amw-portfolio
    autoDeploy: true
    branch: main
```

## Monitoring Law

### Health Check Endpoint
```python
# apps/core/core.py
from django.http import JsonResponse

def health_check(request):
    """Health check endpoint for monitoring."""
    return JsonResponse({'status': 'healthy'})
```

### Error Tracking
```python
# config/settings/production.py
# Sentry integration (optional)
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
    send_default_pii=True,
)
```

### Logging
```python
# config/settings/production.py
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
```

## Performance Law

### Caching Configuration
```python
# config/settings/production.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Cache timeouts
CACHE_MIDDLEWARE_SECONDS = 300  # 5 minutes
CACHE_MIDDLEWARE_KEY_PREFIX = 'portfolio'
```

### Database Optimization
```python
# Use select_related and prefetch_related
posts = BlogPost.objects.select_related('author').prefetch_related('tags')

# Pagination
from django.core.paginator import Paginator

paginator = Paginator(posts, 10)
page = request.GET.get('page')
posts = paginator.get_page(page)
```

## Custom Domain Law

### Domain Configuration
```yaml
# render.yaml
services:
  - type: web
    name: amw-portfolio
    domains:
      - amw.com
      - www.amw.com
```

### SSL Certificate
```bash
# Render provides free SSL certificates
# No manual configuration needed
```

## Rollback Law

### Render Rollback
```bash
# Via dashboard
# 1. Go to service dashboard
# 2. Click "Manual Deploy"
# 3. Select previous version
# 4. Deploy

# Via CLI
render rollback <service-id> <version>
```

### Database Rollback
```bash
# Restore from backup
psql $DATABASE_URL < backup_20250115.sql

# Or use Neon point-in-time recovery
```

## Troubleshooting Law

### Common Issues
```bash
# 1. Static files not loading
python manage.py collectstatic --noinput
python manage.py compress --force

# 2. Database connection errors
# Check DATABASE_URL environment variable
# Verify Neon credentials

# 3. 500 errors
# Check Render logs
# Verify environment variables
# Check Django settings

# 4. Media files not uploading
# Verify CloudFlare R2 credentials
# Check bucket permissions
```

### Debug Mode (Development Only)
```python
# config/settings/development.py
DEBUG = True
ALLOWED_HOSTS = ['*']

# Debug toolbar
INSTALLED_APPS = [
    ...
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    ...
]

INTERNAL_IPS = ['127.0.0.1']
```

## Backup Strategy Law

### Automated Backups
```bash
# Database backups (Neon handles this automatically)
# Media files backup to CloudFlare R2
# Code backup via Git

# Manual backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump $DATABASE_URL > "backups/db_$DATE.sql"
# CloudFlare R2 sync (using rclone or s3cmd compatible tool)
rclone sync media/ r2:your-bucket/media/
```

### Recovery Procedures
```bash
# 1. Database recovery
psql $DATABASE_URL < backups/db_20250115_120000.sql

# 2. Media recovery
rclone sync r2:your-bucket/media/ media/

# 3. Code recovery
git checkout <commit-hash>
```

## Compliance Law

### GDPR Compliance
```python
# Cookie consent (if using analytics)
# Privacy policy page
# Data retention policy
# Right to be forgotten
```

### Accessibility Compliance
```html
<!-- WCAG 2.1 AA compliance -->
<!-- Proper headings structure -->
<!-- Alt text for images -->
<!-- Keyboard navigation -->
<!-- Screen reader support -->
```