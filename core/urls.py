from django.urls import path

from core.views import index, terms_condition_view

urlpatterns = [
    path('', index, name='index'),
    path('terms-condition/', terms_condition_view, name='terms-condition'),
]
