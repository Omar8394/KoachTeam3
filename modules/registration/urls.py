# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path

from modules.registration import views



urlpatterns = [
    #views
    path('enrollment/', views.enrollment, name='enrollment'  ),
    path('EnrollmentList/', views.MatriculacionAdmin, name='EnrollmentList'  ),
    path('ManagePersons/', views.PublicoAdmin, name='ManagePersons'  ),
    

    #metods
    path('enrollment/ComboOptions/', views.ComboOptions, name='ComboOptions'  ),
    path('ManagePersons/ComboOptions/', views.ComboOptions, name='ComboOptions'  ),

    path('EnrollmentList/MatriculacionAdminModal/', views.MatriculacionAdminModal, name='ModalAdmin'  ),
    path('ManagePersons/MatriculacionAddModal/', views.MatriculacionAddModal, name='ModalAdd'  ),


    path('enrollment/save/', views.save, name='save'  ),
    path('ManagePersons/save/', views.ManagePersonSave, name='ManagePersonSave'  ),

    path('EnrollmentList/updateEnrollment/', views.updateEnrollment, name='update'  ),



]
