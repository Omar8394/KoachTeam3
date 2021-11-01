# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
# from .views import hello
from django.urls import path  
from .views import show, showCompetences, destroy, destroyCompetence, showCompetencesAdq, destroyCompetenceAdq, \
showProgram, editProgram, validate_username, validate_competence, renderListasPublic, paginar, renderListasCombos, renderCompetencesPublic, \
saveProgram, managePublic, lockPublic, unlockPublic, modalForm, createProfile, createCompetence, createCompetenceAdq, preRequirements, requirements,\
listaRol, setRole
# from .views import edit
# from modules.planning import views

urlpatterns = [

    # path('hello/',  hello, name='hello'),    
  
    path('show/', show, name="showProfilage"),  
    path('showCompetence/', showCompetences, name="showCompetence"), 
    path('showCompetenceAdq/', showCompetencesAdq, name="showCompetenceAdq"), 
    path('showProgram/', showProgram, name="showProgram"), 
    path('editProgram/<int:id>', editProgram, name="editProgram"),
    path("managePublic/", managePublic, name='managePublic'),
    path('createProfile/', createProfile, name="createProfile"),  
    path('createCompetence/', createCompetence, name="createCompetence"),  
    path('createCompetenceAdq/', createCompetenceAdq, name="createCompetenceAdq"), 
    path('preRequirements/', preRequirements, name="preRequirements"), 
    path('requirements/', requirements, name="requirements"), 

    
    path('delete/', destroy, name="destroyProfilage"),  
    path('deleteCompetence/', destroyCompetence, name="destroyCompetence"),  
    path('deleteCompetenceAdq/', destroyCompetenceAdq, name="destroyCompetenceAdq"),  
    path('validate_username', validate_username, name='validate_username'),
    path('validate_competence', validate_competence, name='validate_competence'),
    path('renderListasPublic', renderListasPublic, name='renderListasPublic'),
    path('paginar', paginar, name='paginar'),
    path('renderListasCombos', renderListasCombos, name='renderListasCombos'),
    path('renderCompetencesPublic', renderCompetencesPublic, name='renderCompetencesPublic'),
    path('saveProgram', saveProgram, name='saveProgram'),
    path('lockPublic', lockPublic, name='lockPublic'),
    path('unlockPublic', unlockPublic, name='unlockPublic'),
    path('modalForm', modalForm, name='modalForm'),
    path('listaRol', listaRol, name='listaRol'),
    path('setRole', setRole, name='setRole'),
    
]
