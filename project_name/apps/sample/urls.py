from django.urls import path

from .views import home

app_name = "app"

urlpatterns = [
    path("app", home, name="index"),
]
