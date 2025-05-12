from django.shortcuts import render

def index(request):
    return render(request, 'core/index.html')

def complete_profile(request):
    return render(request, "core/complete-profile.html")
