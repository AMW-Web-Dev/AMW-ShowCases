# Phase 9: Production

## Objective
Configure production settings and deploy to Render.

## Duration
2-3 hours

## Dependencies
- Phase 8: Frontend Polish

## Tasks

### Task 9.1: Production Settings
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

### Task 9.2: Render Configuration
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

### Task 9.3: Requirements Production
```txt
# requirements/prod.txt
-r base.txt
gunicorn==21.2.0
whitenoise==6.6.0
dj-database-url==2.1.0
sentry-sdk==1.39.1
boto3==1.34.25
django-storages==1.14.2
psycopg2-binary==2.9.9
```

### Task 9.4: Environment Variables
```bash
# .env.example (updated for production)
DJANGO_SETTINGS_MODULE=config.settings.production
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com

# Database (Neon)
DATABASE_URL=postgres://user:pass@host/dbname?sslmode=require

# CloudFlare R2
R2_ACCESS_KEY_ID=your-r2-access-key
R2_SECRET_ACCESS_KEY=your-r2-secret-key
R2_BUCKET_NAME=your-bucket-name
R2_ENDPOINT_URL=https://your-account.r2.cloudflarestorage.com

# Sentry (optional)
SENTRY_DSN=your-sentry-dsn
```

### Task 9.5: Deployment Steps
```bash
# 1. Push to GitHub
git add .
git commit -m "Production configuration"
git push origin main

# 2. Create Render account
# Visit https://render.com

# 3. Create new web service
# Connect GitHub repository

# 4. Configure environment variables
# Add all variables from .env.example

# 5. Deploy
# Render will auto-deploy on push to main

# 6. Create superuser
# SSH into Render shell
python manage.py createsuperuser

# 7. Run migrations
python manage.py migrate

# 8. Collect static files
python manage.py collectstatic --noinput
```

### Task 9.6: Post-Deployment Verification
```bash
# Test production site
curl -I https://your-app.onrender.com

# Check health endpoint
curl https://your-app.onrender.com/health/

# Verify admin access
# Visit https://your-app.onrender.com/admin/
```

## Verification
- [ ] Production settings configured
- [ ] Render service created
- [ ] Environment variables set
- [ ] Site accessible via HTTPS
- [ ] Admin interface working
- [ ] Static files loading
- [ ] Media files uploading

## Commands
```bash
# Deploy to production
git push origin main

# Monitor deployment
# Visit Render dashboard
```

## Completion
- [ ] All phases complete
- [ ] Portfolio website live
- [ ] Admin interface functional
- [ ] Blog system working
- [ ] Skills and projects displayed
- [ ] Analytics tracking visitors

## Next Steps
1. Add content via admin interface
2. Customize styling further
3. Add more features as needed
4. Monitor analytics
5. Share portfolio with others
