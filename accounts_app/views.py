# from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from rest_framework_simplejwt.tokens import RefreshToken

from .forms import SignUpForm, LoginForm, UserUpdateForm, CustomPasswordChangeForm
from .models import CustomUser

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    LogoutView
)


class CustomPasswordResetView(PasswordResetView):
    template_name = 'account_app/password_reset_form.html'
    email_template_name = 'account_app/password_reset_email.html'
    success_url = reverse_lazy('accounts_app:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'account_app/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'account_app/password_reset_confirm.html'
    success_url = reverse_lazy('accounts_app:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'account_app/password_reset_complete.html'


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались и вошли в систему!')
            return redirect('main')
    else:
        form = SignUpForm()
    return render(request, 'account_app/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему!')
            return redirect('main')
    else:
        form = LoginForm()
    return render(request, 'account_app/login.html', {'form': form})


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('main')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Вы успешно вышли из системы!')
        return super().dispatch(request, *args, **kwargs)


@login_required
def profile_view(request, username=None):
    if username and username == request.user.username:
        return redirect('accounts_app:profile')

    if username is None:
        profile_user = request.user
        # Получаем токен для текущего пользователя
        refresh = RefreshToken.for_user(request.user)
        token = str(refresh.access_token)

        if request.method == 'POST':
            form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Профиль успешно обновлен!')
                return redirect('accounts_app:profile')
        else:
            form = UserUpdateForm(instance=request.user)
            password_form = CustomPasswordChangeForm(request.user)
        return render(request, 'account_app/profile.html', {
            'form': form,
            'password_form': password_form,
            'profile_user': profile_user,
            'token': token
        })
    else:
        profile_user = get_object_or_404(CustomUser, username=username)
        return render(request, 'account_app/profile.html', {
            'profile_user': profile_user
        })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Обновляем сессию, чтобы пользователь не вылетел
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успешно изменен!')
            return redirect('accounts_app:profile')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки.')
    return redirect('accounts_app:profile')
