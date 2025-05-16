from django.urls import path
from django.contrib.auth import views as auth_views

from accounts.views import signin_view, profile_view

urlpatterns = [
    path('sign-in/', signin_view, name='signin'),
    path('profile/', profile_view, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='signin'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="accounts/password-forget.html"), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password-forget-done.html"), name='password_reset_done'),
    path('password-forget/', auth_views.PasswordResetView.as_view(template_name="accounts/password-forget.html"), name='password-forget'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password-reset.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/reset-done.html"), name='password_reset_complete'),
]
