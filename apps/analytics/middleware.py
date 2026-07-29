import time
from collections import defaultdict

from django.conf import settings
from django.http import HttpResponseTooManyRequests

from .models import PageView, Visitor


class RateLimitMiddleware:
    """Block IPs exceeding request threshold within a time window.

    Uses in-memory tracking (per-process). Configure via settings:
        RATE_LIMIT_REQUESTS  (default: 50)  — max requests per window
        RATE_LIMIT_WINDOW    (default: 60)  — window in seconds
    """

    _requests: dict[str, list[float]] = defaultdict(list)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not self.should_rate_limit(request):
            return self.get_response(request)

        ip = self.get_client_ip(request)
        if ip and self.is_rate_limited(ip):
            return HttpResponseTooManyRequests("429 — Too Many Requests. Slow down.")

        self._track(ip)
        return self.get_response(request)

    def should_rate_limit(self, request):
        if request.path.startswith("/static/"):
            return False
        if (
            hasattr(request, "user")
            and request.user.is_authenticated
            and request.user.is_staff
        ):
            return False
        return True

    def is_rate_limited(self, ip: str) -> bool:
        now = time.time()
        limit = getattr(settings, "RATE_LIMIT_REQUESTS", 50)
        window = getattr(settings, "RATE_LIMIT_WINDOW", 60)

        timestamps = self._requests[ip]
        # Keep only timestamps within the window
        self._requests[ip] = [t for t in timestamps if now - t < window]

        return len(self._requests[ip]) >= limit

    def _track(self, ip: str | None):
        if ip:
            self._requests[ip].append(time.time())

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")


class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not self.should_track(request):
            return self.get_response(request)

        session_key = f"analytics_tracked_{request.path}"
        if not request.session.get(session_key):
            PageView.objects.create(
                path=request.path,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
                referrer=request.META.get("HTTP_REFERER", ""),
            )

            ip_address = self.get_client_ip(request)
            if ip_address:
                visitor, created = Visitor.objects.get_or_create(ip_address=ip_address)
                if not created:
                    visitor.visit_count += 1
                    visitor.save()

            request.session[session_key] = True

        return self.get_response(request)

    def should_track(self, request):
        if request.path.startswith(("/nexus/", "/static/")):
            return False
        if request.headers.get("HX-Request"):
            return False
        if (
            hasattr(request, "user")
            and request.user.is_authenticated
            and request.user.is_staff
        ):
            return False
        return True

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
