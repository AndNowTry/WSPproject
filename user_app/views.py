from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.models import User
from .forms import UserRegisterForm, EmailLoginForm
from django.core.exceptions import ObjectDoesNotExist

from .models import Profiles


class UserRegisterView(CreateView):
    """
        Регистрация
    """
    model = User
    form_class = UserRegisterForm
    template_name = 'user_app/register_page.html'
    success_url = reverse_lazy('home')



class UserLoginView(LoginView):
    """
        Вход
    """
    template_name = 'user_app/login_page.html'
    authentication_form = EmailLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')



# Выход
# Вписан в путь



# Восстановление по почте инициализация
class UserPasswordResetView(PasswordResetView):
    template_name = 'user_app/password_reset_page.html'
    email_template_name = 'user_app/password_reset_email_page.html'
    success_url = reverse_lazy("user_app:password_reset_done_page")



# Восстановление по почте успех
class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'user_app/password_reset_done_page.html'



# Восстановление по почте изменение
class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'user_app/password_reset_confirm_page.html'
    success_url = reverse_lazy("user_app:password_reset_complete_page")



# Восстановление по почте изменение успех
class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'user_app/password_reset_complete_page.html'


class ProfileView(TemplateView):
    """
        Профиль
    """
    template_name = 'user_app/profile_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile, created = Profiles.objects.get_or_create(
            user=self.request.user,
            defaults={
                'avatar': 'avatars/not_found.png'
            }
        )

        context['profile'] = profile
        return context

    def post(self, request):
        avatar = request.FILES.get('avatar')
        if avatar:
            print(avatar)
            profile = request.user.user_profiles
            profile.avatar = avatar
            profile.save()
            return redirect('profile')

        username = request.POST.get('username')
        about_user = request.POST.get('about_user')

        if username and about_user:
            if not User.objects.filter(username=username).exists():
                request.user.username = username
                request.user.save()

            request.user.user_profiles.about_user = about_user
            request.user.user_profiles.save()
            return redirect('profile')

        if username:
            if not User.objects.filter(username=username).exists():
                request.user.username = username
                request.user.save()
            return redirect('profile')

        if about_user:
            request.user.user_profiles.about_user = about_user
            request.user.user_profiles.save()
            return redirect('profile')

        return redirect('profile')

