from django.urls import path

from . import core

app_name = "Core"

urlpatterns = [
    path("", core.HomepageView.as_view(), name="Homepage"),
    path("about/", core.about_view, name="About"),
    path("contact/", core.contact_view, name="Contact"),
]
