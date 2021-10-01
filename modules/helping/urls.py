# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
# from .views import hello
from django.urls import path  
from .views import helpSecurity
# from .views import edit
# from modules.planning import views

urlpatterns = [

    # path('hello/',  hello, name='hello'),    
  
    path('helpSecurity/', helpSecurity, name="helpSecurity"),
    
    #path('emp/', emp, name="addProfilage"),  
    #path('show/', show, name="showProfilage"),  
    #path('showCompetence/', showCompetences, name="showCompetence"), 
    #path('addCompetence/', addCompetence, name="addCompetence"), 
    #path('edit/<int:id>', edit, name="editProfilage"),  
    # path('planning/update/<int:id>', update),  
    # path('planning/delete/<int:id>', destroy),  
    
]