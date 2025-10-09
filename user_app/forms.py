from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from difflib import SequenceMatcher


class UserRegisterForm(UserCreationForm):
    # имя и два пароля работают на автомате
    email = forms.EmailField(required=True)

    # Дописать проверку на одинаковых пользоватей

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            return email

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email




class EmailLoginForm(AuthenticationForm):
    # Называем поле всё ещё "username" (чтобы не ломать логику AuthenticationForm),
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"autofocus": True}))
    password = forms.CharField(label="Пароль", strip=False, widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        #Дописать проверку на одинаковых пользоватей
        if email and password:
            user = authenticate(self.request, email=email, password=password)
            if user is None:
                raise forms.ValidationError("Неверный email или пароль")
            self.confirm_login_allowed(user)
            self.user_cache = user

        return self.cleaned_data

    def get_user(self):
        return getattr(self, "user_cache", None)
