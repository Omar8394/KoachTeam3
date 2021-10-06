# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user, forgot_password, lang_page, full_registration
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path('passwordReset/', forgot_password, name="passwordReset"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("landpage/", lang_page, name="land_page"),
    path("fullregistration/", full_registration, name="full_registration")
]
