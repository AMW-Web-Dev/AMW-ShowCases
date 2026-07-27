from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "featured", "order", "created_at", "updated_at"]
    list_filter = ["featured", "created_at"]
    search_fields = ["title", "description"]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["technologies"]
    list_editable = ["featured", "order"]
    date_hierarchy = "created_at"
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("title", "slug", "description", "long_description")},
        ),
        ("Media", {"fields": ("image",)}),
        ("Links", {"fields": ("github_url", "live_url")}),
        ("Technologies", {"fields": ("technologies",)}),
        ("Settings", {"fields": ("featured", "order")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
