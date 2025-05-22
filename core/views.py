from django.shortcuts import render

from alasatizah.decorators.profile_required import anonymous_required


def index(request):
    return render(request, "core/home/index.html")


def terms_condition_view(request):
    return render(request, "core/terms_condition/terms-condition.html")


@anonymous_required
def profile_selection_view(request):
    return render(request, "core/profile-selection.html")
