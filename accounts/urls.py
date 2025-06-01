from django.urls import path
from . import views
from django.contrib.auth import views as auth_views # Import Django's built-in authentication views

app_name = 'accounts'

urlpatterns = [
    # User Registration
    # This view handles both full page and HTMX requests for registration.
    path('register/', views.register, name='register'),

    # User Login
    # Using Django's built-in LoginView for robust authentication handling.
    # The template_name points to your full page login template.
    # Your `views.login_view` currently just renders the template, so this handles the form submission.
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),

    # User Logout Confirmation
    # This view handles the logout confirmation and the actual logout action.
    path('logout/', views.logout_confirm, name='logout'),

    # User Profile
    # These views handle displaying and editing the user profile, with HTMX partial support.
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/delete/', views.delete_account, name='delete_account'),

    # Password Change
    # Using your custom CustomPasswordChangeView which inherits from Django's PasswordChangeView.
    path('password_change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    # The 'done' page after a successful password change.
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),

    # Password Reset
    # Using Django's built-in PasswordResetView for the password reset initiation.
    # Ensure you have 'password_reset_email.html' and 'password_reset_subject.txt' templates for the email content.
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html',
                                                                  email_template_name='accounts/password_reset_email.html',
                                                                  subject_template_name='accounts/password_reset_subject.txt'),
         name='password_reset'),
    # The 'done' page after a password reset email has been sent.
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    # The view for users to confirm and set a new password from the email link.
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    # The 'complete' page after a new password has been successfully set.
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
]