from decouple import config

from .base import *  # noqa: F403 F405

DEBUG = True
ALLOWED_HOSTS = ["*"]

# Use local database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", default="portfolio_dev"),
        "USER": config("DB_USER", default="postgres"),
        "PASSWORD": config("DB_PASSWORD", default="password"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
    }
}

# Debug toolbar (disabled - uncomment + add debug_toolbar to urls.py to enable)
# INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405
# MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa: F405
# INTERNAL_IPS = ["127.0.0.1"]
