# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
# from .views import hello
from django.urls import path  
from .views import emp, show, showCompetences, addCompetence, edit, destroy, editCompetence, destroyCompetence, showCompetencesAdq, addCompetenceAdq, editCompetenceAdq, destroyCompetenceAdq, showProgram, addProgram, editProgram, destroyProgram
# from .views import edit
# from modules.planning import views

urlpatterns = [

    # path('hello/',  hello, name='hello'),    
  
    path('emp/', emp, name="addProfilage"),  
    path('show/', show, name="showProfilage"),  
    path('showCompetence/', showCompetences, name="showCompetence"), 
    path('showCompetenceAdq/', showCompetencesAdq, name="showCompetenceAdq"), 
    path('showProgram/', showProgram, name="showProgram"), 
    path('addCompetence/', addCompetence, name="addCompetence"), 
    path('addCompetenceAdq/', addCompetenceAdq, name="addCompetenceAdq"), 
    path('addProgram/', addProgram, name="addProgram"), 
    path('edit/<int:id>', edit, name="editProfilage"),  
    path('editCompetence/<int:id>', editCompetence, name="editCompetence"),  
    path('editCompetenceAdq/<int:id>', editCompetenceAdq, name="editCompetenceAdq"),  
    path('editProgram/<int:id>', editProgram, name="editProgram"),  
    path('delete/<int:id>', destroy, name="destroyProfilage"),  
    path('deleteCompetence/<int:id>', destroyCompetence, name="destroyCompetence"),  
    path('deleteCompetenceAdq/<int:id>', destroyCompetenceAdq, name="destroyCompetenceAdq"),  
    path('deleteProgram/<int:id>', destroyProgram, name="destroyProgram"),  
    
]
