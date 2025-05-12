from django.shortcuts import redirect
from django.urls import reverse

class CompleteProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = str(request.path)
        user = request.user

        EXEMPT_PATHS = [
            '/sign-in/',
            '/sign-up/',
            '/logout/',
            '/complete-profile/',
        ]
        print("path", path)
        print("user", user)

        # if (
        #     user.is_authenticated
        #     and not any(path.endswith(p) for p in EXEMPT_PATHS)
        #     and not hasattr(user, 'tutorprofile')
        #     and not hasattr(user, 'organizationprofile')
        #     and not path.startswith(reverse('complete-profile'))
        #     and not path.startswith('/admin')
        # ):
        #     return redirect('complete-profile')

        response = self.get_response(request)
        return response
