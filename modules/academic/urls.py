# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from modules.academic import views

urlpatterns = [
   path('', views.index, name='academic'),
   #Pruebas de sprint 2
   path('cursos/', views.cursos, name="cursos"),
   #contenidos AJAX
   path('contenidoProgramas/', views.getContentProgramas, name="contenidoProgramas"),
   path('contenidoProcesos/', views.getContentProcesos, name="contenidoProcesos"),
   path('contenidoUnidades/', views.getContentUnidades, name="contenidoUnidades"),
   path('comboOption/', views.getComboContent, name="contenidoCombo"),
   #modales
   path('modalAddCategoria/', views.getModalCategorias, name="modalAddCategoria"),
   path('modalAddPrograma/', views.getModalProgramas, name="modalAddPrograma"),
   path('modalAddProceso/', views.getModalProcesos, name="modalAddProceso"),
   path('modalAddUnidad/', views.getModalUnidades, name="modalAddUnidad"),
   path('modalAddCurso/', views.getModalCursos, name="modalAddCurso"),
   path('modalAddTopico/', views.getModalTopico, name="modalAddTopico"),
   path('evaluaciones/', views.evaluaciones, name="evaluaciones"),
   #urls serias
   path('<str:programa>/', views.programa, name="programa"),
   path('<str:programa>/<str:proceso>/', views.proceso, name="proceso"),
   path('<str:programa>/<str:proceso>/<str:unidad>/', views.unidad, name="unidad"),
   path('<str:programa>/<str:proceso>/<str:unidad>/<str:topico>/', views.topico, name="topico"),
   path('<str:programa>/<str:proceso>/<str:unidad>/<str:topico>/<int:idActividad>/', views.actividad, name="actividad"),
   #demas paginas
   re_path(r'^.*\.*', views.pages, name='pages'),
]
