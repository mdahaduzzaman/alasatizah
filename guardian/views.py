from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.forms import SignUpForm
from accounts.models import Role, User
from alasatizah.decorators.profile_required import guardian_required
from core.forms import AddressForm
from guardian.models import Guardian



def register_guardian_view(request):
    form = SignUpForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        user: User = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.is_active = True
        user.save()

        ustaz_role = Role.objects.get(name="guardian")
        user.roles.add(ustaz_role)

        login(request, user)
        messages.success(request, "Successfully created guardian or student user account")

        # redirect to home page
        return redirect("index")

    return render(request, "guardian/register.html", {"form": form})


@guardian_required
@login_required
def guardian_complete_profile_view(request):
    address_form = AddressForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and address_form.is_valid():
        address = address_form.save()

        # Set the address before saving
        guardian = Guardian.objects.create(address=address, user=request.user)

        messages.success(request, "Successfully completed your guardian or student profile")

        # redirect to home page
        return redirect("index")

    return render(request, "guardian/complete-profile.html", {"address_form": address_form})