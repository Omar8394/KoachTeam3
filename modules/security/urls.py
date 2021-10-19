# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user, register_user_new, forgot_password, lang_page, full_registration,\
    recovery_method, emailrecovery, recovery_method_question,verificationaccount, editProfile, images, rootImages,\
    configadmin
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path('register_new/<str:activation_key>/<str:registertype>/<str:id>/', register_user_new, name="register_new"),
    path('passwordReset/', forgot_password, name="passwordReset"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("landpage/", lang_page, name="land_page"),
    path("fullregistration/", full_registration, name="full_registration"),
    path("recoverymethod/", recovery_method, name="recovery_method"),
    path("emailrecovery/<str:activation_key>/", emailrecovery, name="recovery_method_email"),
    path("recoverymethodquestion/", recovery_method_question, name="recovery_method_question"),
    path("verificationaccount/<str:activation_key>/", verificationaccount, name="verification_account"),
    path("editProfile/", editProfile, name='editProfile'),
    path("images/", images, name='images'),
    path("rootImages/", rootImages, name='rootImages'),
    path("configadmin/", configadmin, name='configadmin')

]
