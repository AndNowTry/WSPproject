from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserRegisterForm(UserCreationForm):
    # имя и два пароля работают на автомате
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class EmailLoginForm(AuthenticationForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)  # вызов кастомного backend

        if user is None:
            raise forms.ValidationError("Неверный email или пароль")

        self.user = user
        return self.cleaned_data
