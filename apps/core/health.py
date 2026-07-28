import os

from django.conf import settings
from django.core.files.storage import default_storage
from django.http import JsonResponse


def health_check(request):
    # Debug storage info
    storage_class = type(default_storage).__name__
    r2_key = bool(os.environ.get("R2_ACCESS_KEY_ID"))
    r2_secret = bool(os.environ.get("R2_SECRET_ACCESS_KEY"))
    r2_bucket = os.environ.get("R2_BUCKET_NAME", "")
    r2_endpoint = os.environ.get("R2_ENDPOINT_URL", "")

    return JsonResponse({
        "status": "healthy",
        "service": "AMW Portfolio",
        "debug": {
            "storage": storage_class,
            "default_file_storage": settings.DEFAULT_FILE_STORAGE,
            "custom_domain": getattr(settings, "AWS_S3_CUSTOM_DOMAIN", None),
            "r2_key_set": r2_key,
            "r2_secret_set": r2_secret,
            "r2_bucket": r2_bucket,
            "r2_endpoint": r2_endpoint,
            "r2_endpoint_set": bool(r2_endpoint),
            "media_url": settings.MEDIA_URL,
            "debug_mode": settings.DEBUG,
        },
    })
