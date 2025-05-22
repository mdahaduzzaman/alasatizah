from django.urls import path

from core.views import index, terms_condition_view, profile_selection_view

urlpatterns = [
    path('', index, name='index'),
    path('profile-selection', profile_selection_view, name='profile-selection'),
    path('terms-condition/', terms_condition_view, name='terms-condition'),
]
