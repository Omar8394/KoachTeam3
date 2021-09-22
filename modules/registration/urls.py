# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path

from modules.registration import views



urlpatterns = [
    path('enrollment/', views.enrollment, name='enrollment'  ),
    

    
    path('enrollment/ComboOptions/', views.ComboOptions, name='ComboOptions'  ),
    path('enrollment/save/', views.save, name='save'  ),


]
