from django.urls import path

from organization.views import register_organization_view


urlpatterns = [
    path("signup/organization/", register_organization_view, name="signup/organization"),
]
