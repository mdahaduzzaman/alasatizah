from django.shortcuts import render

from alasatizah.decorators.profile_required import anonymous_required

from core.models import JobType, Testimonial, JobCategory


def index(request):
    job_types = JobType.objects.all().order_by("ordering")
    ustaz_testimonials = Testimonial.objects.filter(
        type=Testimonial.TypeChoices.USTAZ
    ).order_by("ordering")
    others_testimonials = Testimonial.objects.exclude(
        type=Testimonial.TypeChoices.USTAZ
    ).order_by("ordering")
    categories = JobCategory.objects.all().order_by("ordering")

    context = {
        "job_types": job_types,
        "ustaz_testimonials": ustaz_testimonials,
        "others_testimonials": others_testimonials,
        "categories": categories,
    }
    return render(request, "core/home/index.html", context)


def terms_condition_view(request):
    return render(request, "core/terms_condition/terms-condition.html")


@anonymous_required
def profile_selection_view(request):
    return render(request, "core/profile-selection.html")
