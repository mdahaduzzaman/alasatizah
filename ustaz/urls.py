from django.urls import path

from ustaz.views import register_ustaz_view


urlpatterns = [
    path("signup/ustaz/", register_ustaz_view, name="signup/ustaz"),
]
