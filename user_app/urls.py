from django.urls import path, re_path, include
from .views import UserRegisterView, UserLoginView, UserPasswordResetView, UserPasswordResetDoneView, UserPasswordResetConfirmView, UserPasswordResetCompleteView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password_reset/", UserPasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password_reset/<uidb64>/<token>/", UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password_reset/complete/", UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("auth/", include("social_django.urls", namespace="social")),
]