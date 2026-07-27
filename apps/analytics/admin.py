from django.contrib import admin

from .models import PageView, Visitor


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ["path", "ip_address", "referrer", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["path", "ip_address"]
    readonly_fields = ["created_at"]

    def has_add_permission(self, request):
        return False


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ["ip_address", "first_visit", "last_visit", "visit_count"]
    list_filter = ["first_visit"]
    readonly_fields = ["first_visit", "last_visit"]

    def has_add_permission(self, request):
        return False
