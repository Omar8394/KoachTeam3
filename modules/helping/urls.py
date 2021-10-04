# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from django.urls import path  
from modules.helping import views


urlpatterns = [
    path('helpSecurity/', views.helpSecurity, name="helpSecurity"),   
    path('myHelp/', views.myHelp, name="myHelp"),   
]