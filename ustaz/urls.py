from django.urls import path

from ustaz.views import register_ustaz_view, uztaz_complete_profile_view


urlpatterns = [
    path("signup/ustaz/", register_ustaz_view, name="signup/ustaz"),
    path(
        "ustaz/complete-profile/",
        uztaz_complete_profile_view,
        name="ustaz/complete-profile",
    ),
]
