# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from modules.academic import views

urlpatterns = [
   path('', views.index, name='academic'),
   re_path(r'^.*\.*', views.pages, name='pages'),
]
