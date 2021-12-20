# -*- encoding: utf-8 -*-
from django.urls import path
from itez.authentication.views import login_view, register_user, create_user
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/", create_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
