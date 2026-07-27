from .models import PageView, Visitor


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
        if request.path.startswith("/admin/") or request.path.startswith("/static/"):
            return False
        if request.headers.get("HX-Request"):
            return False
        return True

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
