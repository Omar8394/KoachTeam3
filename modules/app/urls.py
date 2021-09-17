# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from modules.app import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('settings/tables', views.tables, name='system_tables'),
    path('settings/scales', views.scales, name='scales'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
