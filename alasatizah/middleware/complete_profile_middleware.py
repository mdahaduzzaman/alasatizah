from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings


class CompleteProfileMiddleware:
    EXEMPT_PATHS = {
        "/sign-in/",
        "/signup/ustaz/",
        "/signup/organization/",
        "/logout/",
        "/terms-condition/",
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        user = request.user

        # Always allow static, media, admin, and exempt URLs
        if (
            path.startswith(settings.STATIC_URL) or
            path.startswith(settings.MEDIA_URL) or
            path.startswith("/admin") or
            path in self.EXEMPT_PATHS
        ):
            return self.get_response(request)

        if not user.is_authenticated:
            return self.get_response(request)

        # Skip exempt paths
        if path in self.EXEMPT_PATHS:
            return self.get_response(request)

        # Redirect ustaz if profile is not complete
        if user.roles.filter(name="ustaz").exists() and not hasattr(user, 'ustaz'):
            if not path.startswith(reverse("ustaz/complete-profile")):
                return redirect("ustaz/complete-profile")

        # Redirect organization if profile is not complete
        if user.roles.filter(name="organization").exists() and not hasattr(user, 'organization'):
            if not path.startswith(reverse("organization/complete-profile")):
                return redirect("organization/complete-profile")

        return self.get_response(request)
