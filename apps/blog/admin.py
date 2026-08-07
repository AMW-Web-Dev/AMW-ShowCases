from django.contrib import admin

from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "read_count",
        "is_published",
        "published_at",
        "created_at",
        "tag_list",
    ]
    list_filter = ["is_published", "author", "tags"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ["is_published"]
    date_hierarchy = "created_at"
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        ("Content", {"fields": ("title", "slug", "content", "excerpt")}),
        ("Media", {"fields": ("image",)}),
        ("Metadata", {"fields": ("author", "tags", "is_published", "published_at")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def tag_list(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()[:3]])

    tag_list.short_description = "Tags"

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)
