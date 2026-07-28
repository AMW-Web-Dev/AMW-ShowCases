from django.urls import path
from django.views.generic import RedirectView

app_name = "Humans"

urlpatterns = [
    path(
        "",
        RedirectView.as_view(pattern_name="Core:Homepage", permanent=False),
        name="Index",
    ),
]
