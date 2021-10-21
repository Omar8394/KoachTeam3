# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from modules.academic import views

urlpatterns = [
   path('', views.index, name='academic'),
   #Pruebas de sprint 2
   path('createQuestions/', views.createQuestions, name="createQuestions"),
   path('createLessons/', views.createLessons, name="createLessons"),
   path('saveQuestions/', views.saveQuestions, name="saveQuestions"),
   path('takeExam/', views.takeExam, name="takeExam"),
   path('contenidoExamen/', views.contenidoExamen, name="contenidoExamen"),
   path('reviewExamen/', views.reviewExamen, name="reviewExamen"),
   path('TestList/', views.TestList, name="TestList"),
   path('SeeTest/', views.SeeTest, name="SeeTest"),
   path('MyTest/', views.MyTest, name="MyTest"),






   #contenidos AJAX
   path('contenidoProgramas/', views.getContentProgramas, name="contenidoProgramas"),
   path('contenidoProcesos/', views.getContentProcesos, name="contenidoProcesos"),
   path('contenidoUnidades/', views.getContentUnidades, name="contenidoUnidades"),
   path('contenidoCursos/', views.getContentCursos, name="contenidoCursos"),
   path('contenidoTopicos/', views.getContentTopicos, name="contenidoTopicos"),
   path('contenidoLecciones/', views.getContentLecciones, name="contenidoLecciones"),
   path('comboOption/', views.getComboContent, name="contenidoCombo"),
   path('previewLeccion/', views.getPreviewLeccion, name="previewLeccion"),
   #modales
   path('GraficaResultados/', views.GraficaResultados, name="GraficaResultados"),
   path('modalResourcesBank/', views.getModalResourcesBank, name="modalResourcesBank"),
   path('modalAddCategoria/', views.getModalCategorias, name="modalAddCategoria"),
   path('modalAddPrograma/', views.getModalProgramas, name="modalAddPrograma"),
   path('modalAddProceso/', views.getModalProcesos, name="modalAddProceso"),
   path('modalAddUnidad/', views.getModalUnidades, name="modalAddUnidad"),
   path('modalAddCurso/', views.getModalCursos, name="modalAddCurso"),
   path('modalAddTopico/', views.getModalTopico, name="modalAddTopico"),
   path('modalAddActividad/', views.getModalActividad, name="modalAddActividad"),
   path('modalAddPagina/', views.getModalPagina, name="modalAddPagina"),
   path('modalChooseActivity/', views.getModalChooseActivities, name="modalChooseActivity"),
   path('modalNewTest/', views.getModalNewTest, name="modalNewTest"),
   path('modalNewLesson/', views.getModalNewLesson, name="modalNewLesson"),
   path('modalNewHomework/', views.getModalNewHomework, name="modalNewHomework"),
   path('modalNewForum/', views.getModalNewForum, name="modalNewForum"),
   path('modalAddQuestion/', views.getModalQuestion, name="modalAddQuestion"),
   path('modalChooseTypeQuestion/', views.getModalChooseTypeQuestion, name="modalTypeQuestion"),
   path('getModalAddInstructions/', views.getModalAddInstructions, name="getModalAddInstructions"),
   path('modalAddBlock/', views.getModalAddBlock, name="getModalAddBlock"),

   path('modalNewExpert/', views.getModalNewExpert, name="getModalNewExpert"),

   

   path('modalNewSimple/', views.getModalNewSimple, name="modalNewSimple"),
   path('modalNewMultiple/', views.getModalNewMultiple, name="modalNewMultiple"),
   path('modalNewCompletion/', views.getModalNewCompletion, name="modalNewCompletion"),
   path('modalNewAssociation/', views.getModalNewAssociation, name="modalNewAssociation"),
   path('modalNewTof/', views.getModalNewTof, name="modalNewTof"),

   #urls serias
   path('<str:programa>/', views.programa, name="programa"),
   path('<str:programa>/<str:proceso>/', views.proceso, name="proceso"),
   path('<str:programa>/<str:proceso>/<str:unidad>/', views.unidad, name="unidad"),
   path('<str:programa>/<str:proceso>/<str:unidad>/<str:curso>/', views.curso, name="curso"),
   path('<str:programa>/<str:proceso>/<str:unidad>/<str:curso>/<str:topico>/<int:idActividad>/', views.actividad, name="actividad"),
   #demas paginas
   re_path(r'^.*\.*', views.pages, name='pages'),
]
