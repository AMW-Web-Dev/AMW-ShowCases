from django.contrib import admin

from .models import Skill, SkillCategory


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1
    prepopulated_fields = {"slug": ("name",)}


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "order", "skill_count"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [SkillInline]

    def skill_count(self, obj):
        return obj.skills.count()

    skill_count.short_description = "Skills"


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "proficiency",
        "years_experience",
        "featured",
        "order",
    ]
    list_filter = ["category", "featured"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ["proficiency", "featured", "order"]
