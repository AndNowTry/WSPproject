from django.urls import path, re_path
from .views import UserRegisterView, UserLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]