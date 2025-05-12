from django.urls import path
from django.contrib.auth import views as auth_views

from accounts.views import signin_view, signup_view, profile_view, complete_profile_view

urlpatterns = [
    path('sign-in/', signin_view, name='signin'),
    path('sign-up/', signup_view, name='signup'),
    path('complete-profile/', complete_profile_view, name='complete-profile'),
    path('profile/', profile_view, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='signin'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('forget-password', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='forget-password'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]
