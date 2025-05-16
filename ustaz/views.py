from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from alasatizah.decorators.profile_required import anonymous_required, ustaz_required
from accounts.forms import SignUpForm
from accounts.models import Role, User
from core.forms import AddressForm
from ustaz.forms import UstazForm


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
        messages.success(request, "Successfully created organization user account")

        # redirect to home page
        return redirect("index")

    return render(request, "ustaz/register.html", {"form": form})


@ustaz_required
@login_required
def uztaz_complete_profile_view(request):
    form = UstazForm(request.POST or None, request.FILES or None, user=request.user)
    address_form = AddressForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid() and address_form.is_valid():
        address = address_form.save()

        # Set the address before saving
        ustaz = form.save(address=address, user=request.user)

        messages.success(request, "Successfully completed your ustaz profile")

        # redirect to home page
        return redirect("index")

    return render(request, "ustaz/complete-profile.html", {"form": form, "address_form": address_form})
