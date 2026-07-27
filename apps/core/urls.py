from django.urls import path

from . import core

app_name = "core"

urlpatterns = [
    path("", core.HomepageView.as_view(), name="homepage"),
    path("about/", core.about_view, name="about"),
    path("contact/", core.contact_view, name="contact"),
]
