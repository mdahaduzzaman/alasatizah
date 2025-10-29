from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from alasatizah.decorators.profile_required import anonymous_required, ustaz_required
from accounts.forms import SignUpForm
from accounts.models import Role, User
from core.forms import AddressForm
from ustaz.forms import UstazForm
from ustaz.models import (
    Ustaz,
    EducationalQualification,
    TrainingCertificate,
    AchievementCertificate,
    OrganizationTestimonial,
)


@anonymous_required
def register_ustaz_view(request):
    form = SignUpForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        user: User = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.is_active = True
        user.save()

        ustaz_role = Role.objects.get(name="ustaz")
        user.roles.add(ustaz_role)

        login(request, user)
        messages.success(request, "Successfully created ustaz user account")

        # redirect to home page
        return redirect("index")

    return render(request, "ustaz/register.html", {"form": form})


@ustaz_required
@login_required
def uztaz_complete_profile_view(request):
    instance = Ustaz.objects.filter(user=request.user).first()

    form = UstazForm(
        request.POST or None,
        request.FILES or None,
        user=request.user,
        instance=instance,
    )
    address_form = AddressForm(
        request.POST or None,
        request.FILES or None,
        instance=instance.address if instance else None,
    )

    if request.method == "POST" and form.is_valid() and address_form.is_valid():
        address = address_form.save()

        if instance:
            messages.success(request, "Successfully updated your ustaz profile")
        else:
            messages.success(request, "Successfully created your ustaz profile")

        # Set the address before saving
        form.save(address=address, user=request.user)

        # redirect to home page
        return redirect("my_job_requests")

    education_files = EducationalQualification.objects.filter(ustaz=instance)
    training_files = TrainingCertificate.objects.filter(ustaz=instance)
    achievement_files = AchievementCertificate.objects.filter(ustaz=instance)
    testimonial_files = OrganizationTestimonial.objects.filter(ustaz=instance)
    return render(
        request,
        "ustaz/complete-profile.html",
        {
            "form": form,
            "address_form": address_form,
            "education_files": education_files,
            "training_files": training_files,
            "achievement_files": achievement_files,
            "testimonial_files": testimonial_files,
        },
    )
