# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from django.urls import path  
from modules.professors import views 


urlpatterns = [
    
    # Url para mostrar views de Professors
    path('professors/', views.professors, name="professors"),   
    path('contentProfessors/', views.getContentProf, name="contentProfessors"),
    path('contentCourse/', views.getcontetCourso, name="contentCourse"),

    path('SlProfessors/<int:id>', views.selectProfessors, name="SlProfessors"),

    path('addProfessors/', views.getmodalProf, name="addProfessors"),
    path('addProfessors2/', views.getmodalProf2, name="addProfessors2"),
    path('micombobox/', views.combobox101, name="micombobox"),
    path('save/', views.saveProfessors, name="save"),
]