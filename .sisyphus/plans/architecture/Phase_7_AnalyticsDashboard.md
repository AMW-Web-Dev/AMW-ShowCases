# Phase 7: Analytics Dashboard

## Objective
Create an analytics dashboard for tracking page views and visitors.

## Duration
2-3 hours

## Dependencies
- Phase 2: Data Models
- Phase 3: Admin Interface

## Tasks

### Task 7.1: Analytics Views
```python
# apps/analytics/analytics.py
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .models import PageView, Visitor

class AnalyticsDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        # Page views
        context['total_page_views'] = PageView.objects.count()
        context['page_views_30_days'] = PageView.objects.filter(
            created_at__gte=thirty_days_ago
        ).count()
        
        # Unique visitors
        context['total_visitors'] = Visitor.objects.count()
        context['visitors_30_days'] = Visitor.objects.filter(
            first_visit__gte=thirty_days_ago
        ).count()
        
        # Top pages
        context['top_pages'] = PageView.objects.values('path').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        # Recent page views
        context['recent_views'] = PageView.objects.order_by('-created_at')[:20]
        
        # Daily views for chart
        context['daily_views'] = self.get_daily_views(30)
        
        return context
    
    def get_daily_views(self, days):
        """Get daily view counts for chart."""
        daily_views = []
        for i in range(days):
            date = timezone.now() - timedelta(days=i)
            count = PageView.objects.filter(
                created_at__date=date.date()
            ).count()
            daily_views.append({
                'date': date.strftime('%Y-%m-%d'),
                'count': count
            })
        return list(reversed(daily_views))
```

### Task 7.2: Analytics URLs
```python
# apps/analytics/urls.py
from django.urls import path
from . import analytics

app_name = 'analytics'

urlpatterns = [
    path('', analytics.AnalyticsDashboardView.as_view(), name='dashboard'),
]
```

### Task 7.3: Analytics Templates
```html
<!-- templates/analytics/dashboard.html -->
{% extends 'base.html' %}

{% block title %}Analytics Dashboard - AMW Portfolio{% endblock %}

{% block content %}
<div class="container py-4">
    <h1 class="mb-4">Analytics Dashboard</h1>
    
    <!-- Stats Cards -->
    <div class="row mb-4">
        <div class="col-md-3 mb-3">
            <div class="card bg-primary text-white">
                <div class="card-body">
                    <h5 class="card-title">Total Page Views</h5>
                    <p class="display-6">{{ total_page_views }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3 mb-3">
            <div class="card bg-success text-white">
                <div class="card-body">
                    <h5 class="card-title">Views (30 Days)</h5>
                    <p class="display-6">{{ page_views_30_days }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3 mb-3">
            <div class="card bg-info text-white">
                <div class="card-body">
                    <h5 class="card-title">Total Visitors</h5>
                    <p class="display-6">{{ total_visitors }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3 mb-3">
            <div class="card bg-warning text-white">
                <div class="card-body">
                    <h5 class="card-title">Visitors (30 Days)</h5>
                    <p class="display-6">{{ visitors_30_days }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Charts -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Daily Page Views (Last 30 Days)</h5>
                </div>
                <div class="card-body">
                    <canvas id="dailyViewsChart" height="300"></canvas>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Top Pages -->
    <div class="row">
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Top Pages</h5>
                </div>
                <div class="card-body">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Page</th>
                                <th>Views</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for page in top_pages %}
                            <tr>
                                <td>{{ page.path }}</td>
                                <td>{{ page.count }}</td>
                            </tr>
                            {% empty %}
                            <tr>
                                <td colspan="2">No data available</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Recent Views</h5>
                </div>
                <div class="card-body">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Path</th>
                                <th>Time</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for view in recent_views %}
                            <tr>
                                <td>{{ view.path }}</td>
                                <td>{{ view.created_at|timesince }} ago</td>
                            </tr>
                            {% empty %}
                            <tr>
                                <td colspan="2">No data available</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    // Daily Views Chart
    const ctx = document.getElementById('dailyViewsChart').getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [{% for day in daily_views %}'{{ day.date }}'{% if not forloop.last %},{% endif %}{% endfor %}],
            datasets: [{
                label: 'Page Views',
                data: [{% for day in daily_views %}{{ day.count }}{% if not forloop.last %},{% endif %}{% endfor %}],
                borderColor: '#2563eb',
                backgroundColor: 'rgba(37, 99, 235, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
</script>
{% endblock %}
```

### Task 7.4: Analytics Middleware (Optimized)
```python
# apps/analytics/middleware.py
from .models import PageView, Visitor

class AnalyticsMiddleware:
    """Track page views and visitors."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Track page view
        if not self.should_track(request):
            response = self.get_response(request)
            return response
        
        # Use session to avoid duplicate tracking
        session_key = f'analytics_tracked_{request.path}'
        if not request.session.get(session_key):
            PageView.objects.create(
                path=request.path,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                referrer=request.META.get('HTTP_REFERER', ''),
            )
            
            # Track visitor
            ip_address = self.get_client_ip(request)
            if ip_address:
                visitor, created = Visitor.objects.get_or_create(
                    ip_address=ip_address
                )
                if not created:
                    visitor.visit_count += 1
                    visitor.save()
            
            request.session[session_key] = True
        
        response = self.get_response(request)
        return response
    
    def should_track(self, request):
        """Check if we should track this request."""
        # Skip admin and static files
        if request.path.startswith('/admin/') or request.path.startswith('/static/'):
            return False
        # Skip AJAX/HTMX requests for partial content
        if request.headers.get('HX-Request'):
            return False
        return True
    
    def get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
```

### Task 7.5: Register Middleware
```python
# config/settings/base.py
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
```

## Verification
- [ ] Dashboard accessible to staff only
- [ ] Page views tracked correctly
- [ ] Visitors tracked correctly
- [ ] Charts displaying data

## Commands
```bash
python manage.py runserver
# Visit http://localhost:8000/dashboard/
# Login with staff account
```

## Next Phase
Phase 8: Frontend Polish