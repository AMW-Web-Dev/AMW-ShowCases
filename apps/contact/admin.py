from django.contrib import admin
from django.contrib.admin import ShowFacets

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    show_facets = ShowFacets.ALWAYS
    list_display = ["name", "email", "subject", "created_at", "is_read"]
    list_filter = ["is_read", "created_at"]
    search_fields = ["name", "email", "subject", "message"]
    list_editable = ["is_read"]
    date_hierarchy = "created_at"
    readonly_fields = ["name", "email", "subject", "message", "created_at"]
