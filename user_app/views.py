from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.models import User
from .forms import UserRegisterForm, EmailLoginForm, UserUpdateForm, ProfileUpdateForm



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


class ProfileView(FormView):
    """
        Профиль
    """
    template_name = 'user_app/profile_page.html'
    success_url = reverse_lazy('profile')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'User_form': UserUpdateForm(),
            'Profile_form': ProfileUpdateForm(),
        })

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(request.POST)
        profile_form = ProfileUpdateForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {
            'User_form': user_form,
            'Profile_form': profile_form,
        })

