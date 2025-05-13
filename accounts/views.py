from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from alasatizah.decorators.profile_required import anonymous_required
from accounts.forms import ProfileForm, SignInForm, SignUpForm


@anonymous_required
def signup_view(request):
    form = SignUpForm(request.POST or None, request.FILES or None)
    
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.is_active = True
        user.save()

        login(request, user)
        
        # redirect to home page
        return redirect('index')

    return render(request, 'accounts/signup.html', {'form': form})


@anonymous_required
def signin_view(request):
    form = SignInForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        remember_me = form.cleaned_data['remember_me']

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)

            # If remember_me is not checked, set session to expire when browser closes
            if remember_me:
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)  # Session expires on browser close

            # redirect to home page
            messages.success(request, "Successfully logged in")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password")
            form.add_error(None, 'Invalid username or password')

    return render(request, 'accounts/signin.html', {'form': form})


@login_required
def profile_view(request):
    user = request.user
    form = ProfileForm(request.POST or None, request.FILES or None, instance=user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('profile')

    return render(request, "accounts/profile.html", {'form': form})


def complete_profile_view(request):
    return render(request, "accounts/complete-profile.html")