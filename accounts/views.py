from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, EditProfileForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import logout
from django.urls import reverse_lazy

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
            return redirect('tasks:task_list') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    return render(request, 'accounts/login.html')

def logout_confirm(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:login')
    return render(request, 'accounts/logout_confirm.html')

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    return render(request, 'accounts/profile.html', {'user': request.user})

def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})


def delete_account(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    if request.method == 'POST':
        request.user.delete()
        return redirect('accounts:login')  
    return render(request, 'accounts/delete_account.html', {'user': request.user})

def password_reset(request):
    from django.contrib.auth.views import PasswordResetView
    return PasswordResetView.as_view(template_name='accounts/password_reset.html')(request)

def password_reset_done(request):
    from django.contrib.auth.views import PasswordResetDoneView
    return PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html')(request)


