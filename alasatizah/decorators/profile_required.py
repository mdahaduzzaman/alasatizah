from functools import wraps
from django.shortcuts import redirect


def anonymous_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("profile")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def ustaz_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.roles.filter(name="ustaz").exists():
            return view_func(request, *args, **kwargs)
        return redirect("index")

    return _wrapped_view


def organization_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.roles.filter(name="organization").exists():
            return view_func(request, *args, **kwargs)
        return redirect("index")

    return _wrapped_view
