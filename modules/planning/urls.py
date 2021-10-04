# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
# from .views import hello
from django.urls import path  
from .views import show, showCompetences, edit, destroy, editCompetence, destroyCompetence, showCompetencesAdq, editCompetenceAdq, destroyCompetenceAdq, showProgram, addProgram, editProgram, destroyProgram, validate_username, validate_competence, renderListasPublic
# from .views import edit
# from modules.planning import views

urlpatterns = [

    # path('hello/',  hello, name='hello'),    
  
    path('edit/', edit, name="addProfilage"),  
    path('edit/<int:id>', edit, name="editProfilage"),  
    path('show/', show, name="showProfilage"),  
    path('showCompetence/', showCompetences, name="showCompetence"), 
    path('showCompetenceAdq/', showCompetencesAdq, name="showCompetenceAdq"), 
    path('showProgram/', showProgram, name="showProgram"), 
    path('editCompetence/', editCompetence, name="addCompetence"), 
    path('editCompetence/<int:id>', editCompetence, name="editCompetence"), 
    path('addProgram/', addProgram, name="addProgram"),  
    path('editCompetenceAdq/', editCompetenceAdq, name="addCompetenceAdq"), 
    path('editCompetenceAdq/<int:id>', editCompetenceAdq, name="editCompetenceAdq"),  
    path('editProgram/<int:id>', editProgram, name="editProgram"),  

    
    path('delete/', destroy, name="destroyProfilage"),  
    path('deleteCompetence/', destroyCompetence, name="destroyCompetence"),  
    path('deleteCompetenceAdq/', destroyCompetenceAdq, name="destroyCompetenceAdq"),  
    path('deleteProgram/<int:id>', destroyProgram, name="destroyProgram"),   
    path('validate_username', validate_username, name='validate_username'),
    path('validate_competence', validate_competence, name='validate_competence'),
    path('renderListasPublic', renderListasPublic, name='renderListasPublic')
    
]
