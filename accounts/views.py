from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, EditProfileForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.http import HttpResponse

def is_htmx(request):
    return request.headers.get('HX-Request') == 'true'

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        response = super().form_valid(form)
        logout(self.request)
        return response

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if is_htmx(request):
                return HttpResponse("<div class='alert alert-success'>Registration successful. Redirecting...</div>")
            return redirect('tasks:task_list')
    else:
        form = CustomUserCreationForm()
    template = 'accounts/partials/register_form.html' if is_htmx(request) else 'accounts/register.html'
    return render(request, template, {'form': form})

def login_view(request):
    template = 'accounts/partials/login_form.html' if is_htmx(request) else 'accounts/login.html'
    return render(request, template)

def logout_confirm(request):
    if request.method == 'POST':
        logout(request)
        if is_htmx(request):
            return HttpResponse("<div class='alert alert-info'>Logged out successfully.</div>")
        return redirect('accounts:login')
    template = 'accounts/partials/logout_confirm.html' if is_htmx(request) else 'accounts/logout_confirm.html'
    return render(request, template)

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    template = 'accounts/partials/profile.html' if is_htmx(request) else 'accounts/profile.html'
    return render(request, template, {'user': request.user})

def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            if is_htmx(request):
                return render(request, 'accounts/partials/profile.html', {'user': request.user})
            return redirect('accounts:profile')
    else:
        form = EditProfileForm(instance=request.user)
    template = 'accounts/partials/edit_profile_form.html' if is_htmx(request) else 'accounts/edit_profile.html'
    return render(request, template, {'form': form})

def delete_account(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    if request.method == 'POST':
        request.user.delete()
        if is_htmx(request):
            return HttpResponse("<div class='alert alert-warning'>Account deleted. Goodbye!</div>")
        return redirect('accounts:login')
    template = 'accounts/partials/delete_account_confirm.html' if is_htmx(request) else 'accounts/delete_account.html'
    return render(request, template, {'user': request.user})

def password_reset(request):
    from django.contrib.auth.views import PasswordResetView
    return PasswordResetView.as_view(template_name='accounts/password_reset.html')(request)

def password_reset_done(request):
    from django.contrib.auth.views import PasswordResetDoneView
    return PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html')(request)
