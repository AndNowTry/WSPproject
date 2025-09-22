from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LogoutView, LoginView
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