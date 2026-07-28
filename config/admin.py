from django.contrib import admin
from django.utils.text import capfirst


class OrderedAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        ordering = {
            "analytics": 1,
            "contact": 2,
            "blog": 3,
            "core": 4,
            "humans": 5,
            "projects": 6,
            "skills": 7,
            "taggit": 8,
            "auth": 9,
        }
        app_list.sort(key=lambda app: ordering.get(app["app_label"], 99))
        return app_list


admin.site.__class__ = OrderedAdminSite
admin.site.site_header = "AMW Portfolio Admin"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Welcome to Portfolio Admin"
