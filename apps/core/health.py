import os

from django.conf import settings
from django.core.files.storage import default_storage
from django.http import JsonResponse


def health_check(request):
    # Debug storage info
    storage_class = type(default_storage).__name__
    wrapped = getattr(default_storage, "_wrapped", None)
    wrapped_class = type(wrapped).__name__ if wrapped else "not_wrapped"
    r2_key = bool(os.environ.get("R2_ACCESS_ID"))
    r2_secret = bool(os.environ.get("R2_SECRET_ACCESS_KEY"))
    r2_bucket = os.environ.get("R2_BUCKET_NAME", "")
    r2_endpoint = os.environ.get("R2_ENDPOINT_URL", "")

    # Generate a test URL
    test_url = None
    try:
        if wrapped:
            test_url = wrapped.url("projects/PulseFeed.png")
        else:
            test_url = default_storage.url("projects/PulseFeed.png")
    except Exception as e:
        test_url = f"ERROR: {e}"

    return JsonResponse({
        "status": "healthy",
        "service": "AMW Portfolio",
        "debug": {
            "storage": storage_class,
            "wrapped_class": wrapped_class,
            "default_file_storage": settings.DEFAULT_FILE_STORAGE,
            "custom_domain": getattr(settings, "AWS_S3_CUSTOM_DOMAIN", None),
            "r2_key_set": r2_key,
            "r2_secret_set": r2_secret,
            "r2_bucket": r2_bucket,
            "r2_endpoint": r2_endpoint,
            "r2_endpoint_set": bool(r2_endpoint),
            "media_url": settings.MEDIA_URL,
            "debug_mode": settings.DEBUG,
            "test_url": test_url,
        },
    })
