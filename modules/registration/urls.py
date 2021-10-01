# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path

from modules.registration import views



urlpatterns = [
    #views
    #guardar matricula
    path('enrollment/', views.enrollment, name='enrollment'  ),
    #lista de matriculas admin
    path('EnrollmentList/', views.MatriculacionAdmin, name='EnrollmentList'  ),
    # lista publico admin
    path('ManagePersons/', views.PublicoAdmin, name='ManagePersons'  ),
    # Mis matriculas
    path('MyEnrollments/', views.MyEnrollments, name='MyEnrollments'  ),
    #Lista cursos
    path('ManagePrices/', views.ManagePrices, name='MyEnrollments'  ),






    #pagos
    path('Payments/', views.Pay, name='ManagePay'  ),

    

    #metods
    path('enrollment/ComboOptions/', views.ComboOptions, name='ComboOptions'  ),
    path('enrollment/save/', views.save, name='save'  ),

    path('ManagePrices/saveDiscount/', views.saveDiscount, name='saveDiscount'  ),
    path('ManagePrices/savePrices/', views.savePrices, name='savePrices'  ),




    path('ManagePersons/ComboOptions/', views.ComboOptions, name='ComboOptions'  ),
    path('ManagePersons/MatriculacionAddModal/', views.MatriculacionAddModal, name='ModalAdd'  ),
    path('ManagePersons/save/', views.ManagePersonSave, name='ManagePersonSave'  ),



    path('EnrollmentList/MatriculacionAdminModal/', views.MatriculacionAdminModal, name='ModalAdmin'  ),
    path('EnrollmentList/updateEnrollment/', views.updateEnrollment, name='update'  ),

    path('EnrollmentList/ModalPublico/', views.ModalPublico, name='ModalPublico'  ),





    path('MyEnrollments/ModalPay/', views.ModalPay, name='ModalPay'  ),
    path('MyEnrollments/ModalPayDetail/', views.ModalPayDetail, name='ModalPayDetail'  ),
    path('MyEnrollments/ModalPayDetail2/', views.ModalPayDetail2, name='ModalPayDetail2'  ),
    path('MyEnrollments/GetPrice/', views.GetPrice, name='GetPrice'  ),


]
