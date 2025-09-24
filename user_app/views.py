from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.models import User
from .forms import UserRegisterForm, EmailLoginForm


# Регистрация
class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'user_app/register_page.html'
    success_url = reverse_lazy('home')


# Вход
class UserLoginView(LoginView):
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