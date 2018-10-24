from django.urls import include, path

urlpatterns = [
    path("", include("apps.sample.urls")),

    # Quickstartup: This url mapping must be the last one
    path("", include("quickstartup.urls")),
]
