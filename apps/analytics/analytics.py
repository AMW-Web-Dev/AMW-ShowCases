from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.utils import timezone
from django.views.generic import TemplateView

from .models import PageView, Visitor


class AnalyticsDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "analytics/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        thirty_days_ago = timezone.now() - timedelta(days=30)

        context["total_page_views"] = PageView.objects.count()
        context["page_views_30_days"] = PageView.objects.filter(
            created_at__gte=thirty_days_ago
        ).count()

        context["total_visitors"] = Visitor.objects.count()
        context["visitors_30_days"] = Visitor.objects.filter(
            first_visit__gte=thirty_days_ago
        ).count()

        context["top_pages"] = (
            PageView.objects.values("path")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )

        context["recent_views"] = PageView.objects.order_by("-created_at")[:20]

        context["daily_views"] = self.get_daily_views(30)

        return context

    def get_daily_views(self, days):
        daily_views = []
        for i in range(days):
            date = timezone.now() - timedelta(days=i)
            count = PageView.objects.filter(created_at__date=date.date()).count()
            daily_views.append({"date": date.strftime("%Y-%m-%d"), "count": count})
        return list(reversed(daily_views))
