from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from alasatizah.decorators.profile_required import anonymous_required, organization_required
from accounts.forms import SignUpForm
from accounts.models import Role, User
from core.forms import AddressForm
from organization.forms import OrganizationForm


@anonymous_required
def register_organization_view(request):
    form = SignUpForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        user: User = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.is_active = True
        user.save()

        organization_role = Role.objects.get(name="organization")
        user.roles.add(organization_role)

        login(request, user)
        messages.success(request, "Successfully created organization user account")

        # redirect to home page
        return redirect("index")

    return render(request, "organization/register.html", {"form": form})


@organization_required
@login_required
def organization_complete_profile_view(request):
    form = OrganizationForm(request.POST or None, request.FILES or None, user=request.user)
    address_form = AddressForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid() and address_form.is_valid():
        address = address_form.save()

        # Set the address before saving
        organization = form.save(address=address, user=request.user)
        
        messages.success(request, "Successfully completed your organization profile")
        # redirect to home page
        return redirect("my_job_posts")

    return render(request, "organization/complete-profile.html", {"form": form, "address_form": address_form})