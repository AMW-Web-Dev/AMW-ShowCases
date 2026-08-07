from django.contrib import admin
from django.contrib.admin import ShowFacets
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    show_facets = ShowFacets.ALWAYS
    list_display = ["username", "email", "first_name", "last_name", "is_staff"]
    list_filter = ["is_staff", "is_superuser", "is_active"]
    search_fields = ["username", "email", "first_name", "last_name"]
    ordering = ["username"]

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Info",
            {"fields": ("bio", "avatar", "website", "github", "linkedin")},
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional Info",
            {"fields": ("bio", "avatar", "website", "github", "linkedin")},
        ),
    )
