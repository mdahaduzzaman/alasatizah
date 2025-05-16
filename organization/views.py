from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages

from alasatizah.decorators.profile_required import anonymous_required
from accounts.forms import SignUpForm
from accounts.models import Role, User


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
