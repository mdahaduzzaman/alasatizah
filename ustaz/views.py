from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages

from accounts.forms import SignUpForm
from accounts.models import Role, User


def register_ustaz_view(request):
    form = SignUpForm(request.POST or None, request.FILES or None)
    
    if request.method == 'POST' and form.is_valid():
        user: User = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.is_active = True
        user.save()

        ustaz_role = Role.objects.get(name="ustaz")
        user.roles.add(ustaz_role)

        login(request, user)
        messages.success(request, "Successfully created organization user account")
        
        # redirect to home page
        return redirect('index')

    return render(request, "ustaz/register.html", {'form': form})
