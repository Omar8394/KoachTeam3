# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from modules.app import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('modalAddSetting/', views.getModalSetting, name="modalAddSetting"),
    path('settings/tables', views.tables, name='system_tables'),

    #Calendar & index settings
    path('settings/', views.indexSettings, name='indexSettings'),

    # Scales
    path('settings/scales', views.scales, name='scales'),
    path('settings/scales/scalesGeAddModal/', views.scalesGeAddModal, name='modalScaleGeAdd'),

    path('components/tabla', views.componentTabla, name='component_tabla'),
    path('components/lista', views.componentLista, name='component_lista'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
