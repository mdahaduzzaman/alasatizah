from django.shortcuts import render

def index(request):
    return render(request, 'core/home/index.html')

def terms_condition_view(request):
    return render(request, "core/terms_condition/terms-condition.html")
