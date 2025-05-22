from django.urls import path


from guardian.views import register_guardian_view, guardian_complete_profile_view

urlpatterns = [
    path("signup/guardian/", register_guardian_view, name="signup/guardian"),
    path("guardian/complete-profile/", guardian_complete_profile_view, name="guardian/complete-profile"),
]