from django.urls import path

from organization.views import (
    register_organization_view,
    organization_complete_profile_view,
)


urlpatterns = [
    path(
        "signup/organization/", register_organization_view, name="signup/organization"
    ),
    path(
        "organization/complete-profile/",
        organization_complete_profile_view,
        name="organization/complete-profile",
    ),
]
