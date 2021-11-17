from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.db.models import query
from django.db.models.aggregates import Count
from django.http.response import Http404
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django import template
from modules.app import Methods
from core import settings
from pathlib import Path
import uuid
import base64
import datetime
from django.core.paginator import Paginator
from django.db.models import Max

from django.utils.dateparse import parse_datetime
from django.utils import timezone
import mimetypes
import json
from django.core.files.storage import FileSystemStorage
import os
from django.db.models import F

from ..app.models import HistoricoUser, TablasConfiguracion, Estructuraprograma, Publico


from ..security.models import ExtensionUsuario
from modules.registration.models import MatriculaAlumnos, PreciosFormacion
from .models import ActividadEvaluaciones, Cursos, ActividadConferencia, ActividadLeccion, ActividadTarea, EscalaCalificacion, EscalaEvaluacion, EvaluacionesPreguntas, EvaluacionesBloques, Paginas, PreguntasOpciones, ExamenActividad,ExamenRespuestas,ExamenResultados, ProgramaProfesores, Recurso, RecursoPaginas, Tag, TagRecurso,EvaluacionInstrucciones,SugerenciasBloques
from modules.app import models

# Create your views here.
@login_required(login_url="/login/")
def index(request):
    
    user = request.user.extensionusuario
    rol = user.CtaUsuario.fk_rol_usuario.desc_elemento
    publico = user.Publico
    context = {}
    context['segment'] = 'academic'
    context['rol'] = rol
    context['user'] = publico
    if rol == "Admin" or rol == "Student" or rol == "Teacher":
        html_template = (loader.get_template('academic/gestor.html'))
    else:
        return HttpResponseForbidden()
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def createLessons(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            try:
                if request.body:
                    data = json.load(request)
                    if data["method"] == "Delete":
                        pagina = Paginas.objects.get(pk=data["id"])
                        leccion = pagina.fk_estructura_programa
                        pagina.delete()
                        #update order
                        paginas = leccion.paginas_set.all().order_by('ordenamiento')
                        for idx, value in enumerate(paginas, start=1):
                            value.ordenamiento = idx
                            value.save()
                        return JsonResponse({"message":"Deleted"})
                    elif data["method"] == "Sort":
                        for item in data["order"]:
                            tempPage = Paginas.objects.get(pk=item["pk"])
                            tempPage.ordenamiento = item["order"]
                            tempPage.save()
                        return JsonResponse({"message":"Perfect"})
                    elif data["method"] == "Update":
                        pass
                    elif data["method"] == "Create":
                        leccion = ActividadLeccion.objects.get(pk=data["id"]).fk_estructura_programa
                        paginas = leccion.paginas_set.all().order_by('ordenamiento')
                        ordenamiento = paginas.count()
                        for idx, value in enumerate(paginas, start=1):
                            value.ordenamiento = idx
                            value.save()
                        pagina = Paginas()
                        pagina.titulo = ""
                        pagina.contenido = ""
                        pagina.ordenamiento = ordenamiento + 1
                        pagina.fk_estructura_programa = leccion
                    pagina.save()
                    return JsonResponse({"message":"Perfect"})
                else:
                    html_template = (loader.get_template('academic/createLessons.html'))
                    return HttpResponse(html_template.render(context, request))
            except:
                return JsonResponse({"message":"error"}, status=500)
    lessonId=request.GET.get('id')
    context = {}
    user = request.user.extensionusuario
    publico = user.Publico
    rol = user.CtaUsuario.fk_rol_usuario.desc_elemento
    leccion=ActividadLeccion.objects.get(fk_estructura_programa=lessonId)
    if rol == "Teacher":
        actividad=leccion.fk_estructura_programa
        curso=actividad.fk_estructura_padre.fk_estructura_padre
        today = timezone.now().date()
        activo = ProgramaProfesores.objects.filter(fk_publico=publico, fecha_retiro__gt=today, fk_estructura_programa=curso)
        if activo.exists():
            context['segment'] = 'academic'
            context['lesson'] = leccion
            return render(request, 'academic/createLessons.html', context)
        else:
            return HttpResponseForbidden()
    elif rol == "Admin":
        context['segment'] = 'academic'
        context['lesson'] = leccion
        return render(request, 'academic/createLessons.html', context)
    else:
        return HttpResponseForbidden()
        

@login_required(login_url="/login/")
def createQuestions(request):
    cta=ExtensionUsuario.objects.get(user=request.user).CtaUsuario.fk_rol_usuario.valor_elemento 
    if cta== 'rol_student':
      return HttpResponseForbidden()
    

    preguntaId=request.GET.get('id')
    #la modificacion es para que los busque por el id de estructuras programa (me facilita la vida)
    pregunta=ActividadEvaluaciones.objects.get(fk_estructura_programa=preguntaId)
    escalas = EscalaEvaluacion.objects.all()
    
    escalaEvaluacion=pregunta.fk_escala_evaluacion
    escalaBloque=pregunta.fk_escala_bloque

    escalaBloque=pregunta.fk_escala_bloque
    listaExamenes=ExamenActividad.objects.filter(fk_Actividad=pregunta).count()

    listaPreguntas=None
    boque=None

    if(Estructuraprograma.objects.get(pk=preguntaId).fk_categoria.valor_elemento=='activityExpert'):
     bloque=EvaluacionesBloques.objects.filter(fk_actividad_evaluaciones=pregunta.idactividad_evaluaciones).order_by('orden')
     
    else:
     bloque=EvaluacionesBloques.objects.get(fk_actividad_evaluaciones=pregunta.idactividad_evaluaciones)
     listaPreguntas=EvaluacionesPreguntas.objects.filter(fk_evaluaciones_bloque=bloque).order_by('orden')



     

    
    context = {
        'pregunta':pregunta,
        "tipoPreguntas" : TablasConfiguracion.obtenerHijos('PregEvalua'),   
        'modelo':pregunta , 
        'escalas':escalas,
        'bloque':bloque,
        'escalaEvaluacion':escalaEvaluacion,
        'listaPreguntas':listaPreguntas,
        'escalaBloque':escalaBloque,
        'listaExamenes':listaExamenes

    }
    context['segment'] = 'academic'
    if(Estructuraprograma.objects.get(pk=preguntaId).fk_categoria.valor_elemento=='activityExpert'):
     return render(request, 'academic/createExpert.html', context)

    return render(request, 'academic/createQuestions.html', context)

@login_required(login_url="/login/")
def reviewExamen(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            
            
                context = {}
                data = json.load(request)["data"]

                
                if data["method"] == "Show":
                        examen=ExamenActividad.objects.get(pk=data['testId'])
                        resultados=ExamenResultados.objects.filter(fk_Examen=examen.pk)
                        respuestas=ExamenRespuestas.objects.filter(fk_Examen=examen.pk)
                        actividad=ActividadEvaluaciones.objects.annotate(num_child=Count('bloque_actividad', distinct=True) ).get(pk=data['ActivityId'])
                        
                        
                        context = {
                        'examen':examen,
                        'resultados':resultados,
                        'respuestas':respuestas,
                        'actividad':actividad,

                        }
                        html_template = (loader.get_template('academic/ExamenRespuestas.html'))
                        return HttpResponse(html_template.render(context, request))
                   
def getCurrentTime(request):
    if request.method == "POST":
        currentTime=datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")

        return HttpResponse(currentTime) 

@login_required(login_url="/login/")
def contenidoExamen(request):
    cta=ExtensionUsuario.objects.get(user=request.user).CtaUsuario.fk_rol_usuario.valor_elemento 
    if cta!= 'rol_student':
      return HttpResponseForbidden()
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            
            
                context = {}
                data = json.load(request)["data"]

                
                if data["method"] == "Show":
                        actividad=ActividadEvaluaciones.objects.annotate(num_child=Count('bloque_actividad', distinct=True) ).get(pk=data['ActivityId'])
                        Examen=ExamenActividad.objects.get(pk=data['idExamen'])
                        time=None
                        if actividad.duracion != None:
                         time=Examen.fechaInicio+ datetime.timedelta(0,(actividad.duracion*60))

                        
                        context = {
                        'actividad':actividad,
                        'time':time

                        }
                        html_template = (loader.get_template('academic/contenidoExamen.html'))
                        return HttpResponse(html_template.render(context, request))
                   
                if data["method"] == "Get":
                        actividad=ActividadEvaluaciones.objects.annotate(num_child=Count('bloque_actividad', distinct=True) ).get(pk=data['ActivityId'])
                        BloquesPreguntas=actividad.bloque_actividad.all()
                        findpregunta = list(BloquesPreguntas.values())
                        
                         
                        # pregunta=EvaluacionesPreguntas.objects.filter(pk=data["idFind"])
                        # findpregunta = list(pregunta.values())
                        # childs = PreguntasOpciones.objects.filter(fk_evaluacion_pregunta=data["idFind"])
                        # listaChilds = list(childs.values())
                        return JsonResponse({"data":findpregunta}, safe=False)
                     

                if data["method"] == "Update":
                    bloque=EvaluacionesBloques.objects.get(pk=int(data["idViejo"]))
                    
                    bloque.comentario=data['textoBloque']
                    bloque.titulo_bloque=data['tituloBloque']
                    bloque.save()
                if data["method"] == "Retake":
                    print('ssssssssss')
                    Examen=ExamenActividad.objects.get(pk=data['idExamen'])
                    actividad=Examen.fk_Actividad
                    print('ss')

                    
                    Examen.estadoExamen=2
                    Examen.nro_repeticiones=Examen.nro_repeticiones+1
                    Examen.fechaInicio=datetime.datetime.now() 
                    Examen.fechaTermino=None
                    Examen.PuntuacionFinal=0
                    resultados=ExamenResultados.objects.filter(fk_Examen=Examen)
                    opciones=ExamenRespuestas.objects.filter(fk_Examen=Examen)
                    resultados.delete()
                    opciones.delete()
                    Examen.save()
                    logUserBackEnd(Examen.usuario.pk, Examen.fk_Actividad.fk_estructura_programa.pk, False, True)
                    time=None
                    if actividad.duracion != None:
                       
                            time=Examen.fechaInicio+ datetime.timedelta(0,(actividad.duracion*60))
                            time=time.strftime("%b %d %Y %H:%M:%S")

                    return JsonResponse({"id": Examen.pk, 'inicio':time})  



                if data["method"] == "Create":
                    actividad=ActividadEvaluaciones.objects.annotate(num_child=Count('bloque_actividad', distinct=True) ).get(pk=data['ActivityId'])
                    Examen=ExamenActividad.objects.create()

                    Examen.usuario=ExtensionUsuario.objects.get(user=request.user).Publico
                    Examen.estadoExamen=2
                    Examen.nro_repeticiones=1
                    Examen.fechaInicio=datetime.datetime.now() 
                    Examen.fk_Actividad=actividad
                    time=None
                    if actividad.duracion != None:
                       
                            time=Examen.fechaInicio+ datetime.timedelta(0,(actividad.duracion*60))
                            time=time.strftime("%b %d %Y %H:%M:%S")
                 


                    Examen.save()
                    logUserBackEnd(Examen.usuario.pk, Examen.fk_Actividad.fk_estructura_programa.pk, False, False)

                    return JsonResponse({"id": Examen.pk, 'inicio':time})     


                if data["method"] == "Save":
                   respuestas=data["respuestas"] 

                   if respuestas:
                        total=0
                        examen=ExamenActividad.objects.get(pk=data['examenId'])
                        actividad=ActividadEvaluaciones.objects.get(pk=data['ActivityId'])

                        for block in actividad.bloque_actividad.all():
                            resultado=ExamenResultados()
                            resultado.bloque=block
                            resultado.puntuacionBloques=float(0.00)
                            resultado.fk_Examen=examen
                            resultado.save()

                        for resp in respuestas:
                            opcionRespuesta=ExamenRespuestas.objects.create()
                            opcion=PreguntasOpciones.objects.get(pk=resp['opcionID'])
                            opcionRespuesta.fk_Opcion=opcion
                            opcionRespuesta.fk_Examen=examen
                            pregunta=EvaluacionesPreguntas.objects.get(pk=resp['idPregunta'])

                            opcionRespuesta.fk_pregunta=pregunta

                            if(resp['tipoPregunta']==5):
                                opcionRespuesta.respuetaCorrecta=resp['isCorrect']
                            if(resp['tipoPregunta']==4):
                                opcionRelacionada=PreguntasOpciones.objects.get(pk=resp['idRelacional'])
                                opcionRespuesta.fk_OpcionRelacionada=opcionRelacionada
                            opcionRespuesta.save()

                            resultado=ExamenResultados.objects.filter(fk_Examen=examen).get(bloque__pk=resp['bloques'])
                            if(resp['tipoPregunta']==1):
                                if(opcion.respuetaCorrecta):
                                 resultado.puntuacionBloques= resultado.puntuacionBloques+pregunta.puntos_pregunta
                                 examen.PuntuacionFinal=examen.PuntuacionFinal+pregunta.puntos_pregunta

                            if(resp['tipoPregunta']==2):
                             resultado.puntuacionBloques= resultado.puntuacionBloques+opcion.puntos_porc
                             examen.PuntuacionFinal=examen.PuntuacionFinal+opcion.puntos_porc

                            if(resp['tipoPregunta']==3):
                                if(opcion.respuetaCorrecta):
                                    resultado.puntuacionBloques= resultado.puntuacionBloques+pregunta.puntos_pregunta
                                    examen.PuntuacionFinal=examen.PuntuacionFinal+pregunta.puntos_pregunta

                            if(resp['tipoPregunta']==4):
                                opcionRelacionada=PreguntasOpciones.objects.get(pk=resp['idRelacional'])
                                if(opcionRelacionada.indiceAsociacion==opcion.indiceAsociacion):
                                    resultado.puntuacionBloques= resultado.puntuacionBloques+opcion.puntos_porc
                                    examen.PuntuacionFinal=examen.PuntuacionFinal+opcion.puntos_porc

                            if(resp['tipoPregunta']==5):
                             if(opcion.respuetaCorrecta):
                                 resultado.puntuacionBloques= resultado.puntuacionBloques+opcion.puntos_porc
                                 examen.PuntuacionFinal=examen.PuntuacionFinal+opcion.puntos_porc

                            if(resp['tipoPregunta']==6):
                             print(opcion)   
                             print(resultado)   

                             resultado.puntuacionBloques= resultado.puntuacionBloques+opcion.puntos_porc
                             examen.PuntuacionFinal=examen.PuntuacionFinal+opcion.puntos_porc
                            resultado.save()
                            examen.save()
                        
                   examen.estadoExamen=3
                   examen.fechaTermino=datetime.datetime.now() 
                  # examen.nro_repeticiones=examen.nro_repeticiones+1
                   examen.save()
                   estado=False
                   print('aquitoy')
                   if examen.fk_Actividad.fk_estructura_programa.fk_categoria.valor_elemento!='activityExpert':
                    if examen.PuntuacionFinal>=examen.fk_Actividad.calificacion_aprobar:
                       estado=True
                   else:
                       estado=True
                   logUserBackEnd(examen.usuario.pk, examen.fk_Actividad.fk_estructura_programa.pk, estado, True)




             
                return JsonResponse({"message": "Perfect"})     
           
           
    context = {}
    html_template = (loader.get_template('academic/contenidoExamen.html'))
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def takeExam(request):
    cta=ExtensionUsuario.objects.get(user=request.user).CtaUsuario
    if cta.fk_rol_usuario.valor_elemento != 'rol_student':
      return HttpResponseForbidden()
    preguntaId=request.GET.get('id')
    #la modificacion es para que los busque por el id de estructuras programa (me facilita la vida)
    pregunta=ActividadEvaluaciones.objects.get(fk_estructura_programa=preguntaId)
    user=ExtensionUsuario.objects.get(user=request.user)



    curso=pregunta.fk_estructura_programa.fk_estructura_padre.fk_estructura_padre
    unidad=curso.fk_estructura_padre
    proceso=unidad.fk_estructura_padre
    programa=proceso.fk_estructura_padre

    print(curso)
    print(unidad)
    print(proceso)
    print(programa)

    matriculas= MatriculaAlumnos.objects.annotate(estado=F('fk_status_matricula__valor_elemento')).filter(fk_publico=user.user.pk)

    isRegistred=False

    if matriculas.filter(fk_estruc_programa=curso).filter(estado='EstatusAprovado').count()>0:
        isRegistred=True

    if isRegistred==False:
     if matriculas.filter(fk_estruc_programa=unidad).filter(estado='EstatusAprovado').count()>0:
        isRegistred=True

    if isRegistred==False:
     if matriculas.filter(fk_estruc_programa=proceso).filter(estado='EstatusAprovado').count()>0:
        isRegistred=True

    if isRegistred==False:
     if matriculas.filter(fk_estruc_programa=programa).filter(estado='EstatusAprovado').count()>0:
        isRegistred=True

    if isRegistred==False:
        return HttpResponseForbidden()
    escalas = EscalaEvaluacion.objects.all()


    examen=ExamenActividad.objects.filter(fk_Actividad=pregunta).filter(usuario=user.Publico)
  

    instruciones=None
    instruciones=EvaluacionInstrucciones.objects.filter(fk_actividad_evaluaciones=pregunta)
    if instruciones.count()>0:
        instruciones=instruciones[0]
    else:
        instruciones=None

    
    escalaEvaluacion=pregunta.fk_escala_evaluacion
    escalaBloque=pregunta.fk_escala_bloque

    escalaBloque=pregunta.fk_escala_bloque

    listaPreguntas=None
    boque=None

    if(Estructuraprograma.objects.get(pk=preguntaId).fk_categoria.valor_elemento=='activityExpert'):
     bloque=EvaluacionesBloques.objects.filter(fk_actividad_evaluaciones=pregunta.idactividad_evaluaciones)
     
    else:
     bloque=EvaluacionesBloques.objects.get(fk_actividad_evaluaciones=pregunta.idactividad_evaluaciones)
     listaPreguntas=EvaluacionesPreguntas.objects.filter(fk_evaluaciones_bloque=bloque).order_by('orden')


    manejaTiempo=0
    time=None
    
    if examen.estadoExamen==2:
  
        if pregunta.duracion != None:
            manejaTiempo=1
            if examen.count()> 0:
             time=examen[0].fechaInicio+ datetime.timedelta(0,(pregunta.duracion*60))
            if time.replace(tzinfo=None)  <= datetime.datetime.now():
                print('aqui')
                test=ExamenActividad.objects.get(pk=examen[0].pk)
                test.fechaTermino=time
                test.estadoExamen=4
                test.save()
                
             
            else:
             time=time.strftime("%b %d %Y %H:%M:%S")

    
    context = {
        'pregunta':pregunta,
        "tipoPreguntas" : TablasConfiguracion.obtenerHijos('PregEvalua'),   
        'modelo':pregunta , 
        'escalas':escalas,
        'bloque':bloque,
        'escalaEvaluacion':escalaEvaluacion,
        'listaPreguntas':listaPreguntas,
        'escalaBloque':escalaBloque,
        'examen':examen,
        'instrucciones':instruciones,
        'time':time,
        'manejaTiempo':manejaTiempo

    }
    context['segment'] = 'academic'
    if(Estructuraprograma.objects.get(pk=preguntaId).fk_categoria.valor_elemento=='activityExpert'):
     return render(request, 'academic/takeExam.html', context)

    return render(request, 'academic/takeExam.html', context)

@login_required(login_url="/login/")
def SeeTest(request):
    cta=ExtensionUsuario.objects.get(user=request.user).CtaUsuario.fk_rol_usuario.valor_elemento 
    usuario=ExtensionUsuario.objects.get(user=request.user).Publico
    
    Id=request.GET.get('id')
    examen=ExamenActividad.objects.get(pk=Id)
    if cta =='rol_student':
      if examen.usuario!= usuario:
        return HttpResponseForbidden()

    
    
    pregunta=ActividadEvaluaciones.objects.get(pk=examen.fk_Actividad.pk)
    escalas = EscalaEvaluacion.objects.all()
    user=ExtensionUsuario.objects.get(user=request.user)
   # if cta== 'rol_student':
    #  if examen.usuario !=user:
     #     return HttpResponseForbidden()


    print(examen)
    instruciones=None
    
    instruciones=EvaluacionInstrucciones.objects.filter(fk_actividad_evaluaciones=pregunta)
    if instruciones.count()>0:
        instruciones=instruciones[0]
    else:
        instruciones=None
    print(instruciones)
    
    escalaEvaluacion=pregunta.fk_escala_evaluacion
    escalaBloque=pregunta.fk_escala_bloque

    escalaBloque=pregunta.fk_escala_bloque

    listaPreguntas=None
    boque=None

    if(Estructuraprograma.objects.get(pk=pregunta.fk_estructura_programa.pk).fk_categoria.valor_elemento=='activityExpert'):
     bloque=EvaluacionesBloques.objects.filter(fk_actividad_evaluaciones=pregunta.idactividad_evaluaciones)
     
    else:
     bloque=EvaluacionesBloques.objects.get(fk_actividad_evaluaciones=pregunta.idactividad_evaluaciones)
     listaPreguntas=EvaluacionesPreguntas.objects.filter(fk_evaluaciones_bloque=bloque).order_by('orden')

    if examen.estadoExamen==2:
        if pregunta.duracion != None:
            
        # if examen.count()> 0:
            time=examen.fechaInicio+ datetime.timedelta(0,(pregunta.duracion*60))
            if time.replace(tzinfo=None)  <= datetime.datetime.now():
                print('aqui')
                test=ExamenActividad.objects.get(pk=examen.pk)
                test.fechaTermino=time
                test.estadoExamen=4
                test.save()
     

    
    context = {
        'pregunta':pregunta,
        "tipoPreguntas" : TablasConfiguracion.obtenerHijos('PregEvalua'),   
        'modelo':pregunta , 
        'escalas':escalas,
        'bloque':bloque,
        'escalaEvaluacion':escalaEvaluacion,
        'listaPreguntas':listaPreguntas,
        'escalaBloque':escalaBloque,
        'examen':examen,
        'instrucciones':instruciones

    }
    context['segment'] = 'academic'
    if(Estructuraprograma.objects.get(pk=pregunta.fk_estructura_programa.pk).fk_categoria.valor_elemento=='activityExpert'):
     return render(request, 'academic/SeeTest.html', context)

    return render(request, 'academic/SeeTest.html', context)

    


#    if "delete" in data:
#                     question = EvaluacionesPreguntas.objects.get(pk=data["id"])
#                     question.delete()
#                     return JsonResponse({"message": "Deleted"})
#                 elif "idFind" in data:
#                     question = EvaluacionesPreguntas.objects.filter(pk=data["idFind"])
#                     findQuestion = list(question.values())
#                     return JsonResponse({"data":findQuestion[0]}, safe=False)
#                 elif "idViejo" in data:
#                     question = EvaluacionesPreguntas.objects.get(pk=data["idViejo"])
#                 else:
#                     question = EvaluacionesPreguntas()
#                 question.texto_pregunta.data = data["textoPregunta"]
#                 question.puntos_pregunta.data = data["puntosPregunta"]
#                 question.fk_actividad_evaluaciones.data = data["fk_actividad_evaluaciones"]
#                 question. fk_tipo_pregunta_evaluacion.data = data["tipoPregunta"]
#                 question.save()


@login_required(login_url="/login/")
def TestList(request):
    cta=ExtensionUsuario.objects.get(user=request.user).CtaUsuario.fk_rol_usuario.valor_elemento 
    if cta!= 'rol_admin':
      return HttpResponseForbidden()

    examenes=ExamenActividad.objects.annotate(tipoTest=F('fk_Actividad__fk_estructura_programa__fk_categoria__valor_elemento')).all()
     
    fechaFinalExamen=None
    fechaInicialExamen=None
    tipoExamen=None
    soloListos=None
    PersonIdExamen=None
 

    personaBuscarNombre=None


    is_cookie_set = 0
   
    if 'fechaInicialExamen' in request.session or 'fechaFinalExamen' in request.session or 'tipoExamen' in request.session or 'soloListos' in request.session or 'PersonIdExamen' in request.session  : 
        fechaFinalExamen = request.session['fechaFinalExamen'] if 'fechaFinalExamen' in request.session else None
        fechaInicialExamen = request.session['fechaInicialExamen'] if 'fechaInicialExamen' in request.session else None
        soloListos=request.session['soloListos'] if 'soloListos' in request.session else None
        tipoExamen=request.session['tipoExamen'] if 'tipoExamen' in request.session else None
        PersonIdExamen=request.session['PersonIdExamen'] if 'PersonIdExamen' in request.session else None


        
        is_cookie_set = 1
    
    if request.method == "GET":
      

      if request.GET.get('page')==None:
        is_cookie_set = 0
        request.session['fechaInicialExamen']=None
        request.session['fechaFinalExamen']=None
        request.session['PersonIdExamen']=None
        request.session['tipoExamen']=None
        request.session['idOrigen']=None

        request.session['soloListos']=None
        fechaFinalExamen=None
        fechaInicialExamen=None
        tipoExamen=None
        soloListos=None
        PersonIdExamen=None
        personaBuscarNombre=None

      
      if (is_cookie_set == 1): 
          if fechaInicialExamen!=None and fechaInicialExamen!="":

           dateI=parse_datetime(fechaInicialExamen+' 00:00:00-00')
          
         
           examenes=examenes.filter(fechaInicio__gte=dateI)
          if fechaFinalExamen!=None  and fechaFinalExamen!="":

           dateF=parse_datetime(fechaFinalExamen+' 00:00:00-00')
          
          
           examenes=examenes.filter(fechaInicio__lte=dateF)
          
          if PersonIdExamen!=None and PersonIdExamen!="":
           examenes=examenes.filter(usuario=PersonIdExamen)

   
          if tipoExamen!=None and tipoExamen!="":
              if tipoExamen==2:
                 examenes=examenes.filter(tipoTest='activityExpert')
              else:
                 examenes=examenes.filter(tipoTest='activityTest')


          if soloListos!=None and soloListos!="":
           examenes=examenes.filter(estadoExamen=3)





    if request.method == "POST":
        
        if (is_cookie_set == 1): 
          
          request.session['fechaFinalExamen']=None
          request.session['fechaInicialExamen']=None
          request.session['idPersona']=None
          request.session['soloListos']=None
          request.session['tipoExamen']=None
          request.session['PersonIdExamen']=None


       

        fechaInicialExamen=request.POST.get('fechaInicialExamen') 
        

        print(request.POST)
       
        fechaFinalExamen=request.POST.get('fechaFinalExamen') 
        PersonIdExamen=request.POST.get('PersonIdExamen') 
        soloListos=request.POST.get('soloListos') 
        tipoExamen=request.POST.get('tipoExamen') 
     

        
     
        if soloListos!= None and soloListos!="":
         examenes=examenes.filter(estadoExamen=3)

         request.session['soloListos'] = soloListos
    

        print("request.POST")

        if tipoExamen != None and tipoExamen!="":
         tipoExamen=int(tipoExamen)
         if tipoExamen==2:
                 examenes=examenes.filter(tipoTest='activityExpert')
         else:
                 examenes=examenes.filter(tipoTest='activityTest')

         request.session['tipoExamen'] = tipoExamen
        if PersonIdExamen != None and PersonIdExamen!="" :
        
         examenes=examenes.filter(usuario=PersonIdExamen)
         request.session['PersonIdExamen'] = PersonIdExamen

        
        if fechaInicialExamen != None and fechaInicialExamen!="":
          dateI=parse_datetime(fechaInicialExamen+' 00:00:00-00')
          fechaI=fechaInicialExamen
          request.session['fechaInicialExamen'] = fechaI
          
          examenes=examenes.filter(fechaInicio__gte=dateI)

        if fechaFinalExamen != None and fechaFinalExamen!="":
          dateF=parse_datetime(fechaFinalExamen+' 00:00:00-00')
          fechaF=fechaFinalExamen
          request.session['fechaFinalExamen'] = fechaF
          
          examenes=examenes.filter(fechaInicio__lte=dateF)
          


    paginator = Paginator(examenes, 10)
    msg=None
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
  
  
    if tipoExamen!=None and tipoExamen!="":
     tipoExamen=int(tipoExamen)

    if PersonIdExamen!=None and PersonIdExamen!="" :
     personaBuscarNombre=Publico.objects.get(pk=PersonIdExamen)
    else:
      personaBuscarNombre=""
      PersonIdExamen=""
            
    context = { 'msg':msg,
     'ExamenList':page_obj ,
     'isAdmin':True,
     'tipoExamen':tipoExamen,
     'fechaInicialExamen':fechaInicialExamen,
    'fechaFinalExamen':fechaFinalExamen,
    'personaBuscarNombre':personaBuscarNombre,
    'soloListos':soloListos,
     'PersonIdExamen':PersonIdExamen,

     
    }
    context['segment'] = 'academic'

    
    return render(request, 'academic/TestList.html', context)

def getChilds(estructura):
    
    struct=Estructuraprograma.objects.get(pk=estructura)
    if struct.valor_elemento=='Course':
        return



    return 0

def setTimeOuts(request):
    cta=ExtensionUsuario.objects.get(user=request.user).CtaUsuario.fk_rol_usuario.valor_elemento 
    if cta!= 'rol_admin':
      return HttpResponseForbidden()

    examenes=ExamenActividad.objects.annotate(tipoTest=F('fk_Actividad__fk_estructura_programa__fk_categoria__valor_elemento'), actividad=F('fk_Actividad__fk_estructura_programa__fk_estructura_padre__fk_estructura_padre')).all()
    if cta== 'rol_teacher':
     user=ExtensionUsuario.objects.get(user=request.user).Publico
     programasProfes=ProgramaProfesores.objects.filter(fk_publico=user)
     if programasProfes.count()<1:
        print('examenes')

        examenes=examenes.filter(pk=-1)
     else:
      for item in programasProfes: 
        examenes=examenes.filter(actividad=item.fk_estructura_programa.idestructuraprogrmas)

    for item in examenes:
        actividad=item.fk_Actividad
        if item.estadoExamen==2:
            if actividad.duracion != None:
             time=item.fechaInicio+ datetime.timedelta(0,(actividad.duracion*60))
            if time >= datetime.datetime.now():
                item.fechaTermino=time
                item.estadoExamen=4
                item.save()
                logUserBackEnd(item.usuario.pk, item.fk_Actividad.fk_estructura_programa.pk, False, True)


    return HttpResponse('OK')

@login_required(login_url="/login/")
def TeacherTests(request):
    cta=ExtensionUsuario.objects.get(user=request.user).CtaUsuario.fk_rol_usuario.valor_elemento 
    if cta!= 'rol_teacher':
      return HttpResponseForbidden()

    examenes=ExamenActividad.objects.annotate(tipoTest=F('fk_Actividad__fk_estructura_programa__fk_categoria__valor_elemento'), actividad=F('fk_Actividad__fk_estructura_programa__fk_estructura_padre__fk_estructura_padre')).all()
    user=ExtensionUsuario.objects.get(user=request.user).Publico
    programasProfes=ProgramaProfesores.objects.filter(fk_publico=user)

    if programasProfes.count()<1:
        print('examenes')

        examenes=examenes.filter(pk=-1)
    else:
     for item in programasProfes: 
        examenes=examenes.filter(actividad=item.fk_estructura_programa.idestructuraprogrmas)

   






     
    fechaFinalExamen=None
    fechaInicialExamen=None
    tipoExamen=None
    soloListos=None
    PersonIdExamen=None
 

    personaBuscarNombre=None


    is_cookie_set = 0
   
    if 'fechaInicialExamen' in request.session or 'fechaFinalExamen' in request.session or 'tipoExamen' in request.session or 'soloListos' in request.session or 'PersonIdExamen' in request.session  : 
        fechaFinalExamen = request.session['fechaFinalExamen'] if 'fechaFinalExamen' in request.session else None
        fechaInicialExamen = request.session['fechaInicialExamen'] if 'fechaInicialExamen' in request.session else None
        soloListos=request.session['soloListos'] if 'soloListos' in request.session else None
        tipoExamen=request.session['tipoExamen'] if 'tipoExamen' in request.session else None
        PersonIdExamen=request.session['PersonIdExamen'] if 'PersonIdExamen' in request.session else None


        
        is_cookie_set = 1
    
    if request.method == "GET":
      

      if request.GET.get('page')==None:
        is_cookie_set = 0
        request.session['fechaInicialExamen']=None
        request.session['fechaFinalExamen']=None
        request.session['PersonIdExamen']=None
        request.session['tipoExamen']=None
        request.session['idOrigen']=None

        request.session['soloListos']=None
        fechaFinalExamen=None
        fechaInicialExamen=None
        tipoExamen=None
        soloListos=None
        PersonIdExamen=None
        personaBuscarNombre=None

      
      if (is_cookie_set == 1): 
          if fechaInicialExamen!=None and fechaInicialExamen!="":

           dateI=parse_datetime(fechaInicialExamen+' 00:00:00-00')
          
         
           examenes=examenes.filter(fechaInicio__gte=dateI)
          if fechaFinalExamen!=None  and fechaFinalExamen!="":

           dateF=parse_datetime(fechaFinalExamen+' 00:00:00-00')
          
          
           examenes=examenes.filter(fechaInicio__lte=dateF)
          
          if PersonIdExamen!=None and PersonIdExamen!="":
           examenes=examenes.filter(usuario=PersonIdExamen)

   
          if tipoExamen!=None and tipoExamen!="":
              if tipoExamen==2:
                 examenes=examenes.filter(tipoTest='activityExpert')
              else:
                 examenes=examenes.filter(tipoTest='activityTest')


          if soloListos!=None and soloListos!="":
           examenes=examenes.filter(estadoExamen=3)





    if request.method == "POST":
        
        if (is_cookie_set == 1): 
          
          request.session['fechaFinalExamen']=None
          request.session['fechaInicialExamen']=None
          request.session['idPersona']=None
          request.session['soloListos']=None
          request.session['tipoExamen']=None
          request.session['PersonIdExamen']=None


       

        fechaInicialExamen=request.POST.get('fechaInicialExamen') 
        

        print(request.POST)
       
        fechaFinalExamen=request.POST.get('fechaFinalExamen') 
        PersonIdExamen=request.POST.get('PersonIdExamen') 
        soloListos=request.POST.get('soloListos') 
        tipoExamen=request.POST.get('tipoExamen') 
     

        
     
        if soloListos!= None and soloListos!="":
         examenes=examenes.filter(estadoExamen=3)

         request.session['soloListos'] = soloListos
    

        print("request.POST")

        if tipoExamen != None and tipoExamen!="":
         tipoExamen=int(tipoExamen)
         if tipoExamen==2:
                 examenes=examenes.filter(tipoTest='activityExpert')
         else:
                 examenes=examenes.filter(tipoTest='activityTest')

         request.session['tipoExamen'] = tipoExamen
        if PersonIdExamen != None and PersonIdExamen!="" :
        
         examenes=examenes.filter(usuario=PersonIdExamen)
         request.session['PersonIdExamen'] = PersonIdExamen

        
        if fechaInicialExamen != None and fechaInicialExamen!="":
          dateI=parse_datetime(fechaInicialExamen+' 00:00:00-00')
          fechaI=fechaInicialExamen
          request.session['fechaInicialExamen'] = fechaI
          
          examenes=examenes.filter(fechaInicio__gte=dateI)

        if fechaFinalExamen != None and fechaFinalExamen!="":
          dateF=parse_datetime(fechaFinalExamen+' 00:00:00-00')
          fechaF=fechaFinalExamen
          request.session['fechaFinalExamen'] = fechaF
          
          examenes=examenes.filter(fechaInicio__lte=dateF)
          


    paginator = Paginator(examenes, 10)
    msg=None
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
  
  
    if tipoExamen!=None and tipoExamen!="":
     tipoExamen=int(tipoExamen)

    if PersonIdExamen!=None and PersonIdExamen!="" :
     personaBuscarNombre=Publico.objects.get(pk=PersonIdExamen)
    else:
      personaBuscarNombre=""
      PersonIdExamen=""
            
    context = { 'msg':msg,
     'ExamenList':page_obj ,
     'isAdmin':True,
     'tipoExamen':tipoExamen,
     'fechaInicialExamen':fechaInicialExamen,
    'fechaFinalExamen':fechaFinalExamen,
    'personaBuscarNombre':personaBuscarNombre,
    'soloListos':soloListos,
     'PersonIdExamen':PersonIdExamen,

     
    }
    context['segment'] = 'academic'

    
    return render(request, 'academic/TestList.html', context)

@login_required(login_url="/login/")
def saveMatricula(request):

     if request.method == "POST":
     
      try:
        idEstruct=request.POST.get('id')



        
       # publico=Publico.objects.get(user=request.user)


        
        publico=ExtensionUsuario.objects.get(user=request.user).Publico
        print(idEstruct)

        struct=Estructuraprograma.objects.get(idestructuraprogrmas=idEstruct)
        print(struct)

        padre=struct.fk_estructura_padre
        matriculaAlumno=MatriculaAlumnos.objects.filter(fk_publico=publico)

        if matriculaAlumno.filter(fk_estruc_programa=struct)!=None:
          for matricula in matriculaAlumno.filter(fk_estruc_programa=struct):
            if matricula.fk_status_matricula.valor_elemento!='EstatusCancelado':
              return HttpResponse(2)
        count =0
        while padre !=None:
          print(count)
          if matriculaAlumno.filter(fk_estruc_programa=padre)!=None:
            for matricula in matriculaAlumno.filter(fk_estruc_programa=padre):
              if matricula.fk_status_matricula.valor_elemento!='EstatusCancelado':
                return HttpResponse(2)
          padre=padre.fk_estructura_padre
          count=count+1

      

        statusDB=TablasConfiguracion.objects.get(valor_elemento='EstatusRevision')
       


        
        matricula=MatriculaAlumnos.objects.create(fk_publico=publico,fk_estruc_programa=struct, fecha_matricula=datetime.date.today(),fk_status_matricula=statusDB,fecha_aprobada=None, origenSolicitud=4  )
        matricula.save()
        return HttpResponse(1)

      except:
        return HttpResponse("Error, try again later")
@login_required(login_url="/login/")
def GraficaResultados(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            
            
                context = {}
                data = json.load(request)["data"]

                if data["method"] == "Show":
                        Examen=ExamenActividad.objects.get(pk=data["id"])
                        resultados=ExamenResultados.objects.annotate(bloque_respuesta=F('bloque__titulo_bloque'),escala=F('bloque__titulo_bloque')).filter(fk_Examen=Examen)
                        dataResults=[]
                        escalaBloques=Examen.fk_Actividad.fk_escala_bloque.escalaMenor.all().order_by("puntos_maximo")
                        escalaTotal=Examen.fk_Actividad.fk_escala_evaluacion.escalaMenor.all()
                        for res in resultados:
                            for item in escalaBloques:
                                print(item.puntos_maximo)
                                if res.puntuacionBloques<=item.puntos_maximo:
                                    sugerencia=SugerenciasBloques.objects.filter(fk_bloque=res.bloque).filter(escalaOpcion=item)
                                    if sugerencia.count()>0:
                                     dataResults.append(sugerencia[0])
                                   

                                    break
                        
                        rol=ExtensionUsuario.objects.get(user=request.user).CtaUsuario.fk_rol_usuario
                        publico=ExtensionUsuario.objects.get(user=request.user).Publico
                        context={
                                'dataResults':dataResults,
                                'rol':rol,
                                'publico':publico,
                                'Examen':Examen
                        }
                        html_template = (loader.get_template('components/modalSeeResults.html'))
                        return HttpResponse(html_template.render(context, request))

                if data["method"] == "Set":
                        Examen=ExamenActividad.objects.get(pk=data["id"])
                        resultados=ExamenResultados.objects.annotate(bloque_respuesta=F('bloque__titulo_bloque'),escala=F('bloque__titulo_bloque')).filter(fk_Examen=Examen)
                        dataSet=[]
                        
                        dataSet.append(' ')
                        escalaBloques=Examen.fk_Actividad.fk_escala_bloque.escalaMenor.all().order_by("puntos_maximo")
                        escalaTotal=Examen.fk_Actividad.fk_escala_evaluacion.escalaMenor.all()
                        for res in resultados:
                            for item in escalaBloques:
                                print(item.puntos_maximo)
                                if res.puntuacionBloques<=item.puntos_maximo:
                                    dataSet.append(item.desc_calificacion)
                                    

                                    break

                        print(dataSet)
                        dataSet.append(' ')

                        resultadosJson = list(resultados.values())
                        
                        escalaBloquesJson = list(escalaBloques.values())
                        escalaTotalJson = list(escalaTotal.values())

                        return JsonResponse({"resultadosJson":resultadosJson, "escalaBloquesJson":escalaBloquesJson,'escalaTotalJson':escalaTotalJson, 'dataSet':dataSet, }, safe=False)
               
    
        


@login_required(login_url="/login/")
def MyTest(request):
    cta=ExtensionUsuario.objects.get(user=request.user).CtaUsuario.fk_rol_usuario.valor_elemento 
    if cta!= 'rol_student':
      return HttpResponseForbidden()

    examenes=ExamenActividad.objects.annotate(tipoTest=F('fk_Actividad__fk_estructura_programa__fk_categoria__valor_elemento')).all()

    examenes.filter(usuario=ExtensionUsuario.objects.get(user=request.user).Publico)

    fechaFinalExamen=None
    fechaInicialExamen=None
    tipoExamen=None
    soloListos=None
    PersonIdExamen=None
 

    personaBuscarNombre=None


    is_cookie_set = 0
   
    if 'fechaInicialExamen' in request.session or 'fechaFinalExamen' in request.session or 'tipoExamen' in request.session or 'soloListos' in request.session or 'PersonIdExamen' in request.session  : 
        fechaFinalExamen = request.session['fechaFinalExamen'] if 'fechaFinalExamen' in request.session else None
        fechaInicialExamen = request.session['fechaInicialExamen'] if 'fechaInicialExamen' in request.session else None
        soloListos=request.session['soloListos'] if 'soloListos' in request.session else None
        tipoExamen=request.session['tipoExamen'] if 'tipoExamen' in request.session else None
        PersonIdExamen=request.session['PersonIdExamen'] if 'PersonIdExamen' in request.session else None


        
        is_cookie_set = 1
    
    if request.method == "GET":
      

      if request.GET.get('page')==None:
        is_cookie_set = 0
        request.session['fechaInicialExamen']=None
        request.session['fechaFinalExamen']=None
        request.session['PersonIdExamen']=None
        request.session['tipoExamen']=None
        request.session['idOrigen']=None

        request.session['soloListos']=None
        fechaFinalExamen=None
        fechaInicialExamen=None
        tipoExamen=None
        soloListos=None
        PersonIdExamen=None
        personaBuscarNombre=None

      
      if (is_cookie_set == 1): 
          if fechaInicialExamen!=None and fechaInicialExamen!="":

           dateI=parse_datetime(fechaInicialExamen+' 00:00:00-00')
          
         
           examenes=examenes.filter(fechaInicio__gte=dateI)
          if fechaFinalExamen!=None  and fechaFinalExamen!="":

           dateF=parse_datetime(fechaFinalExamen+' 00:00:00-00')
          
          
           examenes=examenes.filter(fechaInicio__lte=dateF)
          
          if PersonIdExamen!=None and PersonIdExamen!="":
           examenes=examenes.filter(usuario=PersonIdExamen)

   
          if tipoExamen!=None and tipoExamen!="":
              if tipoExamen==2:
                 examenes=examenes.filter(tipoTest='activityExpert')
              else:
                 examenes=examenes.filter(tipoTest='activityTest')


          if soloListos!=None and soloListos!="":
           examenes=examenes.filter(estadoExamen=3)





    if request.method == "POST":
        
        if (is_cookie_set == 1): 
          
          request.session['fechaFinalExamen']=None
          request.session['fechaInicialExamen']=None
          request.session['idPersona']=None
          request.session['soloListos']=None
          request.session['tipoExamen']=None
          request.session['PersonIdExamen']=None


       

        fechaInicialExamen=request.POST.get('fechaInicialExamen') 
        

        print(request.POST)
       
        fechaFinalExamen=request.POST.get('fechaFinalExamen') 
        PersonIdExamen=request.POST.get('PersonIdExamen') 
        soloListos=request.POST.get('soloListos') 
        tipoExamen=request.POST.get('tipoExamen') 
     

        
     
        if soloListos!= None and soloListos!="":
         examenes=examenes.filter(estadoExamen=3)

         request.session['soloListos'] = soloListos
    

        print("request.POST")

        if tipoExamen != None and tipoExamen!="":
         tipoExamen=int(tipoExamen)
         if tipoExamen==2:
                 examenes=examenes.filter(tipoTest='activityExpert')
         else:
                 examenes=examenes.filter(tipoTest='activityTest')

         request.session['tipoExamen'] = tipoExamen
        if PersonIdExamen != None and PersonIdExamen!="" :
        
         examenes=examenes.filter(usuario=PersonIdExamen)
         request.session['PersonIdExamen'] = PersonIdExamen

        
        if fechaInicialExamen != None and fechaInicialExamen!="":
          dateI=parse_datetime(fechaInicialExamen+' 00:00:00-00')
          fechaI=fechaInicialExamen
          request.session['fechaInicialExamen'] = fechaI
          
          examenes=examenes.filter(fechaInicio__gte=dateI)

        if fechaFinalExamen != None and fechaFinalExamen!="":
          dateF=parse_datetime(fechaFinalExamen+' 00:00:00-00')
          fechaF=fechaFinalExamen
          request.session['fechaFinalExamen'] = fechaF
          
          examenes=examenes.filter(fechaInicio__lte=dateF)
          


     
    paginator = Paginator(examenes, 10)
    
    msg=None
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if tipoExamen!=None and tipoExamen!="":
     tipoExamen=int(tipoExamen)

    if PersonIdExamen!=None and PersonIdExamen!="" :
     personaBuscarNombre=Publico.objects.get(pk=PersonIdExamen)
    else:
      personaBuscarNombre=""
      PersonIdExamen=""


            
    context = { 'msg':msg,
     'ExamenList':page_obj ,
     'isAdmin':False,
      'tipoExamen':tipoExamen,
     'fechaInicialExamen':fechaInicialExamen,
    'fechaFinalExamen':fechaFinalExamen,
    'personaBuscarNombre':personaBuscarNombre,
    'soloListos':soloListos,
     'PersonIdExamen':PersonIdExamen,
    }
    context['segment'] = 'academic'

    
    return render(request, 'academic/TestList.html', context)


@login_required(login_url="/login/")
def saveQuestions(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                context = {}
                data = json.load(request)["data"]
                
                if data['tipoPregunta']==1:
                 pregunta=EvaluacionesPreguntas.objects.create()
                 bloque=EvaluacionesBloques.objects.get(pk=data['fatherId'])
                 pregunta.fk_evaluaciones_bloque=bloque
                 pregunta.texto_pregunta=data['textoPregunta']
                 pregunta.puntos_pregunta=data['puntosPregunta']
                 pregunta.fk_tipo_pregunta_evaluacion=data['tipoPregunta']
                 pregunta.save

                 hijos = data["hijos"]
                 if hijos:
                     print('jeje')
                        # if "idViejo" in data:
                        #     childs = EscalaCalificacion.objects.filter(fk_escala_evaluacion=newScaleGe)
                        #     childs.delete()
                        # for newScalePa in hijos:
                        #     newSP = EscalaCalificacion()
                        #     newSP.desc_calificacion=newScalePa["descriptionCalif"]
                        #     newSP.puntos_maximo=newScalePa["max_points"] 
                        #     newSP.fk_calificacion_id=newScalePa["quack"]
                        #     newSP.fk_escala_evaluacion= newScaleGe
                        #     newSP.save()    

             
                return JsonResponse({"message": "Perfect"})      
            except:
                return JsonResponse({"message": "Error"})
                
    context = {}
    html_template = (loader.get_template('academic/createQuestions.html'))
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def getContentProgramas(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            user = request.user.extensionusuario
            rol = user.CtaUsuario.fk_rol_usuario.desc_elemento
            publico = user.Publico
            if request.body:
                data = json.load(request)    
                lista = {}
                edit=False
                delete=False
                categorias = TablasConfiguracion.obtenerHijos("CatPrograma")
                if rol == "Admin":
                    edit=True
                    delete=True
                    if data["query"] == "" or data["query"] == None:
                        for categoria in categorias:
                            lista[categoria.desc_elemento]=categoria.estructuraprograma_set.all().filter(valor_elemento="Program")
                    else:
                        for categoria in categorias:
                            lista[categoria.desc_elemento]=categoria.estructuraprograma_set.all().filter(valor_elemento="Program", descripcion__icontains=data["query"])
                elif rol == "Teacher":
                    today = timezone.now().date()
                    cursos = ProgramaProfesores.objects.filter(fk_publico=publico, fecha_retiro__gt=today).filter(fk_estructura_programa__valor_elemento="Course")
                    if cursos.exists():
                        edit=True
                        delete=False
                        if data["query"] == "" or data["query"] == None:
                            for categoria in categorias:
                                programas = cursos.filter(fk_estructura_programa__fk_categoria=categoria)
                                lista[categoria.desc_elemento] = []
                                for programa in programas:
                                    lista[categoria.desc_elemento].append(programa.fk_estructura_programa)
                        else:
                            for categoria in categorias:
                                programas = cursos.filter(fk_estructura_programa__fk_categoria=categoria, fk_estructura_programa__descripcion__icontains=data["query"])
                                lista[categoria.desc_elemento] = []
                                for programa in programas:
                                    lista[categoria.desc_elemento].append(programa.fk_estructura_programa)
                elif rol == "Student":
                    estatus = TablasConfiguracion.obtenerHijos("EstMatricula").get(valor_elemento="EstatusAprovado")
                    cursos = MatriculaAlumnos.objects.filter(fk_publico=publico, fk_status_matricula=estatus)
                    if cursos.exists():
                        if data["query"] == "" or data["query"] == None:
                            for categoria in categorias:
                                programas = list(cursos.filter(fk_estruc_programa__fk_categoria=categoria))
                                lista[categoria.desc_elemento] = []
                                for programa in programas:
                                    lista[categoria.desc_elemento].append(programa.fk_estruc_programa)
                        else:
                            for categoria in categorias:
                                programas = list(cursos.filter(fk_estruc_programa__fk_categoria=categoria, fk_estruc_programa__descripcion__icontains=data["query"]))
                                lista[categoria.desc_elemento] = []
                                for programa in programas:
                                    lista[categoria.desc_elemento].append(programa.fk_estruc_programa)
                else:
                    return HttpResponseForbidden()
                context = {"data" : lista, "edit": edit, "delete":delete, "query":data["query"], "rol":rol}
                html_template = (loader.get_template('academic/contenidoProgramas.html'))
                return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def getContentProcesos(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            user = request.user.extensionusuario
            rol = user.CtaUsuario.fk_rol_usuario.desc_elemento
            if request.body:
                data = json.load(request)
                edit=False
                delete=False
                programa=Estructuraprograma.objects.get(valor_elemento="Program", url=data["url"])
                if data["query"] == "" or data["query"] == None:
                    lista = programa.estructuraprograma_set.all()
                else:
                    lista = programa.estructuraprograma_set.all().filter(valor_elemento="Process", descripcion__icontains=data["query"])
                if rol == "Admin":
                    edit=True
                    delete=True
                elif rol == "Teacher":
                    edit=False
                    delete=False
                elif rol == "Student":
                    edit=False
                    delete=False
                else:
                    return HttpResponseForbidden()
                context = {"data":lista, "programa":programa, "edit": edit, "delete":delete, "query":data["query"]}
                html_template = (loader.get_template('academic/contenidoProcesos.html'))
                return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def getContentUnidades(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            user = request.user.extensionusuario
            rol = user.CtaUsuario.fk_rol_usuario.desc_elemento
            if request.body:
                data = json.load(request)    
                edit=False
                delete=False
                programa=Estructuraprograma.objects.get(valor_elemento="Program", url=data["url"])
                proceso=Estructuraprograma.objects.get(valor_elemento="Process", url=data["urlProceso"])
                if data["query"] == "" or data["query"] == None:
                    lista = proceso.estructuraprograma_set.all()
                else:
                    lista = proceso.estructuraprograma_set.all().filter(valor_elemento="Unit", descripcion__icontains=data["query"])
                if rol == "Admin":
                    edit=True
                    delete=True
                elif rol == "Teacher":
                    edit=False
                    delete=False
                elif rol == "Student":
                    edit=False
                    delete=False
                else:
                    return HttpResponseForbidden()
                context = {"data":lista, "programa":programa, "proceso":proceso ,"edit": edit, "delete":delete, "query":data["query"]}
                html_template = (loader.get_template('academic/contenidoUnidades.html'))
                return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def getContentCursos(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            user = request.user.extensionusuario
            publico = user.Publico
            rol = user.CtaUsuario.fk_rol_usuario.desc_elemento
            if request.body:
                data = json.load(request)    
                edit=False
                delete=False
                programa=Estructuraprograma.objects.get(valor_elemento="Program", url=data["url"])
                proceso=Estructuraprograma.objects.get(valor_elemento="Process", url=data["urlProceso"])
                unidad=Estructuraprograma.objects.get(valor_elemento="Unit", url=data["urlUnidad"])
                if data["query"] == "" or data["query"] == None:
                    lista = unidad.estructuraprograma_set.all()
                else:
                    lista = unidad.estructuraprograma_set.all().filter(valor_elemento="Course", descripcion__icontains=data["query"])
                if rol == "Admin":
                    edit=True
                    delete=True
                elif rol == "Teacher":
                    edit=False
                    delete=False
                elif rol == "Student":
                    edit=False
                    delete=False
                else:
                    return HttpResponseForbidden()
                context = {"data":lista, "user":publico, "rol":rol, "programa":programa, "proceso":proceso, "unidad":unidad ,"edit": edit, "delete":delete, "query":data["query"]}
                html_template = (loader.get_template('academic/contenidoCursos.html'))
                return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def getContentTopicos(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            user = request.user.extensionusuario
            publico = user.Publico
            rol = user.CtaUsuario.fk_rol_usuario.desc_elemento
            if request.body:
                data = json.load(request)    
                take=False
                go=False
                add=False
                edit=False
                delete=False
                see=False
                programa=Estructuraprograma.objects.get(valor_elemento="Program", url=data["url"])
                proceso=Estructuraprograma.objects.get(valor_elemento="Process", url=data["urlProceso"])
                unidad=Estructuraprograma.objects.get(valor_elemento="Unit", url=data["urlUnidad"])
                curso=Estructuraprograma.objects.get(valor_elemento="Course", url=data["urlCurso"])
                if data["query"] == "" or data["query"] == None:
                    lista = curso.estructuraprograma_set.all().order_by("orden_presentacion")
                else:
                    lista = curso.estructuraprograma_set.all().filter(valor_elemento="Topic", descripcion__icontains=data["query"]).order_by("orden_presentacion")
                if rol == "Admin":
                    edit=True
                    delete=True
                    go=True
                    add=True
                elif rol == "Teacher":
                    today = timezone.now().date()
                    activo = ProgramaProfesores.objects.filter(fk_publico=publico, fecha_retiro__gt=today, fk_estructura_programa=curso)
                    if activo.exists():
                        edit=True
                        delete=True
                        go=True
                        add=True
                elif rol == "Student":
                    edit=False
                    delete=False
                    take=True
                    go=False
                    add=False
                else:
                    return HttpResponseForbidden()
                context = {"data":lista, "programa":programa, "proceso":proceso, "unidad":unidad, "curso":curso ,"add":add,"edit": edit,"take": take,"see": see, "delete":delete, "go":go, "query":data["query"]}
                html_template = (loader.get_template('academic/contenidoTopicos.html'))
                return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def getContentLecciones(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            if request.body:
                data = json.load(request)    
                take=True
                go=True
                see=True
                edit=True
                add=True
                delete=True
                leccionId = data["id"]
                leccion = ActividadLeccion.objects.get(pk=leccionId)
                actividad = leccion.fk_estructura_programa
                if data["query"] == "" or data["query"] == None:
                    lista = actividad.paginas_set.all().order_by("ordenamiento")
                else:
                    lista = actividad.paginas_set.all().filter(titulo__icontains=data["query"]).order_by("ordenamiento")
                context = {"data":lista, "lesson":leccion ,"add":add,"edit": edit,"take": take,"see": see, "delete":delete, "go":go, "query":data["query"]}
                html_template = (loader.get_template('academic/contenidoLecciones.html'))
                return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def getContentRecursos(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            if request.body:
                data = json.load(request)
                if data["show"] == "tags":
                    if data["query"] == "" or data["query"] == None:
                        lista = Tag.objects.all().order_by("desc_tag")
                    else:
                        lista = Tag.objects.filter(desc_tag__icontains=data["query"]).order_by("desc_tag")
                if data["show"] == "resources":
                    tag = Tag.objects.get(pk=data["tag"])
                    lista = TagRecurso.objects.filter(fk_tag=tag)
                context = {"data":lista, "show":data["show"]}
                html_template = (loader.get_template('academic/contenidoRecursos.html'))
                return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def getModalCategorias(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            try:
                if request.body:
                    data = json.load(request)
                    config = TablasConfiguracion.objects.filter(valor_elemento="CatPrograma")
                    padre = list(config.values())[0]
                    if data["method"] == "Delete":
                        category = TablasConfiguracion.objects.get(id_tabla=data["id"])
                        category.delete()
                        return JsonResponse({"message":"Deleted"})
                    elif data["method"] == "Update":
                        category = TablasConfiguracion.objects.get(id_tabla=data["id"])
                    elif data["method"] == "Create":
                        category = TablasConfiguracion()
                        category.tipo_elemento=0 
                        category.permite_cambios=1
                        category.valor_elemento=None
                        category.mostrar_en_combos=1
                        category.maneja_lista=0
                        category.fk_tabla_padre_id=padre["id_tabla"]
                    category.desc_elemento = data["data"]["descriptionCat"]
                    category.save()
                    return JsonResponse({"message":"Perfect"})
                else:
                    html_template = (loader.get_template('components/modalAddCategoria.html'))
                    return HttpResponse(html_template.render(context, request))
            except:
                return JsonResponse({"message":"error"}, status=500)

@login_required(login_url="/login/")
def getModalProgramas(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            modelo = {}
            try:
                if request.body:
                    data = json.load(request)
                    if data["method"] == "Find":
                        modelo = Estructuraprograma.objects.get(pk=data["id"])    
                        categorias = TablasConfiguracion.obtenerHijos(valor="CatPrograma")
                        context = {"categorias": categorias, "modelo": modelo}
                        html_template = (loader.get_template('components/modalAddPrograma.html'))
                        return HttpResponse(html_template.render(context, request))
                    elif data["method"] == "Delete":
                        programa = Estructuraprograma.objects.get(pk=data["id"])
                        programa.delete()
                        return JsonResponse({"message":"Deleted"})
                    elif data["method"] == "Update":
                        programa = Estructuraprograma.objects.get(pk=data["id"])
                    elif data["method"] == "Create":
                        programa = Estructuraprograma()
                        programa.valor_elemento = "Program"
                        programa.fk_estructura_padre_id=None
                    programa.descripcion = data["data"]["descriptionProgram"]
                    programa.resumen = data["data"]["resumenProgram"]
                    programa.url = data["data"]["urlProgram"]
                    programa.fk_categoria_id = data["data"]["categoryProgram"]
                    programa.peso_creditos = data["data"]["creditos"]
                    programa.save()
                    precios = PreciosFormacion.objects.filter(fk_estruc_programa=programa)
                    if not precios.exists():
                        precio = PreciosFormacion(fecha_registro=timezone.now(),fk_estruc_programa=programa)
                        precio.save()
                    return JsonResponse({"message":"Perfect"})
                else:
                    categorias = TablasConfiguracion.obtenerHijos(valor="CatPrograma")
                    context = {"categorias": categorias, "modelo": modelo}
                    html_template = (loader.get_template('components/modalAddPrograma.html'))
                    return HttpResponse(html_template.render(context, request))
            except:
                return JsonResponse({"message":"error"}, status=500)

@login_required(login_url="/login/")
def getModalProcesos(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            modelo = {}
            try:
                if request.body:
                    data = json.load(request)
                    if data["method"] == "Find":
                        modelo = Estructuraprograma.objects.get(pk=data["id"])    
                        programs = Estructuraprograma.objects.filter(valor_elemento="Program")
                        context = {"programs": programs, "modelo": modelo}
                        html_template = (loader.get_template('components/modalAddProceso.html'))
                        return HttpResponse(html_template.render(context, request))
                    elif data["method"] == "Delete":
                        proceso = Estructuraprograma.objects.get(pk=data["id"])
                        proceso.delete()
                        return JsonResponse({"message":"Deleted"})
                    elif data["method"] == "Update":
                        proceso = Estructuraprograma.objects.get(pk=data["id"])
                    elif data["method"] == "Create":
                        proceso = Estructuraprograma()
                        proceso.valor_elemento = "Process"
                    proceso.fk_estructura_padre_id=data["data"]["padreProcess"]
                    proceso.descripcion = data["data"]["descriptionProcess"]
                    proceso.resumen = data["data"]["resumenProcess"]
                    proceso.url = data["data"]["urlProcess"]
                    proceso.fk_categoria_id = Estructuraprograma.objects.get(pk=data["data"]["padreProcess"]).fk_categoria_id
                    proceso.peso_creditos = data["data"]["creditos"]
                    proceso.save()
                    precios = PreciosFormacion.objects.filter(fk_estruc_programa=proceso)
                    if not precios.exists():
                        precio = PreciosFormacion(fecha_registro=timezone.now(),fk_estruc_programa=proceso)
                        precio.save()
                    return JsonResponse({"message":"Perfect"})
                else:
                    programs = Estructuraprograma.objects.filter(valor_elemento="Program")
                    context = {"programs": programs, "modelo": modelo}
                    html_template = (loader.get_template('components/modalAddProceso.html'))
                    return HttpResponse(html_template.render(context, request))
            except:
                return JsonResponse({"message":"error"}, status=500)

@login_required(login_url="/login/")
def getModalUnidades(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            modelo = {}
            try:
                if request.body:
                    data = json.load(request)
                    if data["method"] == "Find":
                        modelo = Estructuraprograma.objects.get(pk=data["id"])
                        modeloPadre = Estructuraprograma.objects.get(pk=modelo.fk_estructura_padre_id)
                        programs = Estructuraprograma.objects.filter(valor_elemento="Program")
                        processes = Estructuraprograma.objects.filter(valor_elemento="Process")
                        context = {"programs": programs, "processes":processes, "modelo": modelo, "modeloPadre": modeloPadre}
                        html_template = (loader.get_template('components/modalAddUnidad.html'))
                        return HttpResponse(html_template.render(context, request))
                    elif data["method"] == "Delete":
                        unidad = Estructuraprograma.objects.get(pk=data["id"])
                        unidad.delete()
                        return JsonResponse({"message":"Deleted"})
                    elif data["method"] == "Update":
                        unidad = Estructuraprograma.objects.get(pk=data["id"])
                    elif data["method"] == "Create":
                        unidad = Estructuraprograma()
                        unidad.valor_elemento = "Unit"
                    unidad.fk_estructura_padre_id=data["data"]["padreUnit"]
                    unidad.descripcion = data["data"]["descriptionUnit"]
                    unidad.resumen = data["data"]["resumenUnit"]
                    unidad.url = data["data"]["urlUnit"]
                    unidad.fk_categoria_id = Estructuraprograma.objects.get(pk=data["data"]["padreUnit"]).fk_categoria_id
                    unidad.peso_creditos = data["data"]["creditos"]
                    unidad.save()
                    precios = PreciosFormacion.objects.filter(fk_estruc_programa=unidad)
                    if not precios.exists():
                        precio = PreciosFormacion(fecha_registro=timezone.now(),fk_estruc_programa=unidad)
                        precio.save()
                    return JsonResponse({"message":"Perfect"})
                else:
                    programs = Estructuraprograma.objects.filter(valor_elemento="Program")
                    processes = Estructuraprograma.objects.filter(valor_elemento="Process")
                    context = {"programs": programs, "processes":processes, "modelo": modelo}
                    html_template = (loader.get_template('components/modalAddUnidad.html'))
                    return HttpResponse(html_template.render(context, request))
            except:
                return JsonResponse({"message":"error"}, status=500)

@login_required(login_url="/login/")
def getModalCursos(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            modelo = {}
            try:
                if request.body:
                    data = json.load(request)
                    if data["method"] == "Show":
                        modelo = Estructuraprograma.objects.get(pk=data["id"])
                        units = Estructuraprograma.objects.filter(valor_elemento="Unit",fk_estructura_padre_id=modelo.fk_estructura_padre_id)
                        tipoDuracion = TablasConfiguracion.obtenerHijos(valor="Duracion")
                        status = TablasConfiguracion.obtenerHijos(valor="EstCurso")
                        
                        context = {"units":units,"tipoDuracion":tipoDuracion, "status":status}
                        html_template = (loader.get_template('components/modalAddCurso.html'))
                        return HttpResponse(html_template.render(context, request))
                    elif data["method"] == "Find":
                        modeloCurso = Cursos.objects.get(fk_estruc_programa=data["id"])
                        modelo = Estructuraprograma.objects.get(pk=data["id"])
                        modeloPadre = Estructuraprograma.objects.get(pk=modelo.fk_estructura_padre_id)
                        units = Estructuraprograma.objects.filter(valor_elemento="Unit",fk_estructura_padre=modeloPadre.fk_estructura_padre)
                        tipoDuracion = TablasConfiguracion.obtenerHijos(valor="Duracion")
                        status = TablasConfiguracion.obtenerHijos(valor="EstCurso")
                        context = {"units":units, "modeloCurso":modeloCurso, "modelo": modelo, "tipoDuracion":tipoDuracion, "status":status}
                        html_template = (loader.get_template('components/modalAddCurso.html'))
                        return HttpResponse(html_template.render(context, request))
                    elif data["method"] == "Delete":
                        curso = Estructuraprograma.objects.get(pk=data["id"])
                        curso.delete()
                        return JsonResponse({"message":"Deleted"})
                    elif data["method"] == "Update":
                        curso = Estructuraprograma.objects.get(pk=data["id"])
                        curso_char = curso.cursos
                    elif data["method"] == "Create":
                        curso = Estructuraprograma()
                        curso_char = Cursos()
                        curso.valor_elemento = "Course"
                    curso.fk_estructura_padre_id=data["data"]["padreCourse"]
                    curso.descripcion = data["data"]["titleCourse"]
                    curso.resumen = data["data"]["resumenCourse"]
                    curso.url = data["data"]["urlCourse"]
                    curso.fk_categoria_id = Estructuraprograma.objects.get(pk=data["data"]["padreCourse"]).fk_categoria_id
                    curso.peso_creditos = data["data"]["creditos"]
                    curso_char.abrev_curso = data["data"]["urlCourse"]
                    curso_char.codigo_curso = data["data"]["codeCourse"]
                    curso_char.disponible_desde = data["data"]["disponibleCourse"]
                    curso_char.fk_estatus_curso_id = data["data"]["statusCourse"]
                    curso_char.tipo_evaluacion = False
                    if "checkExpertCB" in data["data"]:
                        curso_char.tipo_evaluacion = True
                    if "durationCourse" in data["data"]:
                        curso_char.duracion = data["data"]["durationCourse"]
                    else:
                        curso_char.duracion = None
                    if "timeCourse" in data["data"]:
                        curso_char.fk_tipo_duracion_id = data["data"]["timeCourse"]
                    else:
                        curso_char.fk_tipo_duracion_id = None
                    curso.save()
                    curso_char.fk_estruc_programa = curso
                    curso_char.save()
                    precios = PreciosFormacion.objects.filter(fk_estruc_programa=curso)
                    if not precios.exists():
                        precio = PreciosFormacion(fecha_registro=timezone.now(),fk_estruc_programa=curso)
                        precio.save()
                    return JsonResponse({"message":"Perfect"})
            except:
                return JsonResponse({"message":"error"}, status=500)


@login_required(login_url="/login/")
def getModalTopico(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            modelo = {}
            try:
                if request.body:
                    data = json.load(request)
                    if data["method"] == "Show":
                        modelo = Estructuraprograma.objects.get(pk=data["id"])
                        courses = Estructuraprograma.objects.filter(valor_elemento="Course",fk_estructura_padre_id=modelo.fk_estructura_padre_id)
                        context = {"courses":courses}
                        html_template = (loader.get_template('components/modalAddTopico.html'))
                        return HttpResponse(html_template.render(context, request))
                    elif data["method"] == "Find":
                        modelo = Estructuraprograma.objects.get(pk=data["id"])
                        modeloPadre = Estructuraprograma.objects.get(pk=modelo.fk_estructura_padre_id)
                        courses = Estructuraprograma.objects.filter(valor_elemento="Course",fk_estructura_padre=modeloPadre.fk_estructura_padre)
                        context = {"courses": courses, "modelo": modelo}
                        html_template = (loader.get_template('components/modalAddTopico.html'))
                        return HttpResponse(html_template.render(context, request))
                    elif data["method"] == "Sort":
                        for item in data["order"]:
                            topico = Estructuraprograma.objects.get(pk=item["pk"])
                            topico.orden_presentacion = item["order"]
                            topico.save()
                        return JsonResponse({"message":"Perfect"})
                    elif data["method"] == "Delete":
                        topico = Estructuraprograma.objects.get(pk=data["id"])
                        topico.delete()
                        return JsonResponse({"message":"Deleted"})
                    elif data["method"] == "Update":
                        topico = Estructuraprograma.objects.get(pk=data["id"])
                    elif data["method"] == "Create":
                        topico = Estructuraprograma()
                        topico.valor_elemento = "Topic"
                    topico.fk_estructura_padre_id=data["data"]["padreTopic"]
                    topico.descripcion = data["data"]["descriptionTopic"]
                    topico.resumen = data["data"]["resumenTopic"]
                    topico.url = data["data"]["urlTopic"]
                    topico.fk_categoria_id = Estructuraprograma.objects.get(pk=data["data"]["padreTopic"]).fk_categoria_id
                    topico.peso_creditos = None
                    topico.save()
                    return JsonResponse({"message":"Perfect"})
            except:
                return JsonResponse({"message":"error"}, status=500)

@login_required(login_url="/login/")
def getModalActividad(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            modelo = {}
            try:
                if request.body:
                    data = json.load(request)
                    if data["method"] == "Show":
                        html_template = (loader.get_template('components/modalAddActividad.html'))
                        return HttpResponse(html_template.render(context, request))
                    elif data["method"] == "Find":
                        modelo = Estructuraprograma.objects.get(pk=data["id"])
                        context = {"modelo": modelo}
                        html_template = (loader.get_template('components/modalAddActividad.html'))
                        return HttpResponse(html_template.render(context, request))
                    elif data["method"] == "Sort":
                        for item in data["order"]:
                            actividad = Estructuraprograma.objects.get(pk=item["pk"])
                            actividad.orden_presentacion = item["order"]
                            actividad.save()
                        return JsonResponse({"message":"Perfect"})
                    elif data["method"] == "Delete":
                        actividad = Estructuraprograma.objects.get(pk=data["id"])
                        actividad.delete()
                        return JsonResponse({"message":"Deleted"})
                    elif data["method"] == "Update":
                        actividad = Estructuraprograma.objects.get(pk=data["id"])
                    elif data["method"] == "Create":
                        actividad = Estructuraprograma()
                        actividad.valor_elemento = "Activity"
                        actividad.orden_presentacion = len(Estructuraprograma.objects.filter(fk_estructura_padre=data["padreActivity"]))
                    actividad.fk_estructura_padre_id=data["padreActivity"]
                    actividad.descripcion = data["data"]["descriptionActivity"]
                    actividad.resumen = data["data"]["resumenActivity"]
                    actividad.url = data["data"]["urlActivity"]
                    actividad.fk_categoria_id = TablasConfiguracion.obtenerHijos(valor="Tipo Actividad").filter(desc_elemento=data["tipoActividad"])[0].pk
                    actividad.peso_creditos = None
                    actividad.save()
                    return JsonResponse({"message":"Perfect"})
            except:
                return JsonResponse({"message":"error"}, status=500)

@login_required(login_url="/login/")
def getModalPagina(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            modelo = {}
            try:
                if request.body:
                    data = json.load(request)
                    if data["method"] == "Show":
                        html_template = (loader.get_template('components/modalAddPagina.html'))
                        return HttpResponse(html_template.render(context, request))
                    elif data["method"] == "Find":
                        modelo = Paginas.objects.get(pk=data["id"])
                        context = {"modelo": modelo}
                        html_template = (loader.get_template('components/modalAddPagina.html'))
                        return HttpResponse(html_template.render(context, request))
                    elif data["method"] == "Delete":
                        pagina = Paginas.objects.get(pk=data["id"])
                        pagina.delete()
                        return JsonResponse({"message":"Deleted"})
                    elif data["method"] == "Update":
                        pagina = Paginas.objects.get(pk=data["id"])
                    elif data["method"] == "Create":
                        pagina = Paginas()
                    pagina.titulo = data["data"]["titlePage"]
                    pagina.contenido=None
                    if data["data"]["summernote"] != "<p><br></p>":
                        pagina.contenido = data["data"]["summernote"]
                    pagina.save()
                    recursos = data["data"]["recursos"]
                    oldResources = RecursoPaginas.objects.filter(fk_pagina=pagina.pk)
                    oldResources.delete()
                    for recurso in recursos:
                        resource = Recurso.objects.get(pk=recurso["id"])
                        newResource = RecursoPaginas()
                        newResource.fk_pagina = pagina
                        newResource.fk_recurso = resource
                        newResource.save()
                    return JsonResponse({"message":"Perfect"})
            except:
                return JsonResponse({"message":"error"}, status=500)

@login_required(login_url="/login/")
def getPreviewLeccion(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            modelo = {}
            try:
                if request.body:
                    data = json.load(request)
                    if data["method"] == "Find":
                        modelo = Paginas.objects.get(pk=data["id"])
                        context = {"modelo":modelo.contenido}
                        html_template = (loader.get_template('academic/previewLeccion.html'))
                        return HttpResponse(html_template.render(context, request))
                    return JsonResponse({"message":"Perfect"})
            except:
                return JsonResponse({"message":"error"}, status=500)

@login_required(login_url="/login/")
def getModalResourcesBank(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            modelo = {}
            # try:
            if request.headers.get("idPagina"):
                #Handle the files upload
                idPagina = request.headers.get('idPagina')
                myfiles = list(request.FILES.values())
                fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                recursos = []
                for file in myfiles:
                    resourceType = mimetypes.guess_type(file.name)[0]
                    nombreImagen = str(uuid.uuid4())
                    extensionFile=Path(file.name).suffix
                    nombreImagen="res_"+nombreImagen+extensionFile
                    Ruta=settings.MEDIA_ROOT
                    # folder = request.path.replace("/", "_")
                    try:
                        os.mkdir(os.path.join(Ruta))
                    except:
                        pass
                    #save file
                    fs.save(Ruta+'/'+nombreImagen, file)
                    #after save file lets go to save on BBDD
                    newRecurso = Recurso()
                    newRecurso.titulo = file.name
                    newRecurso.path = nombreImagen
                    newRecurso.tipo_path = 0
                    newRecurso.compartido = False
                    if request.POST.get("checkSharedCB"):
                        newRecurso.compartido = True
                    if "application/pdf" in resourceType:
                        resourceType = "Recurso_pdf"
                    if "image/" in resourceType:
                        resourceType = "Recurso_image"
                    if "audio/" in resourceType:
                        resourceType = "Recurso_audio"
                    newRecurso.fk_tipo_recurso = TablasConfiguracion.obtenerHijos("Recurso").get(valor_elemento=resourceType)
                    newRecurso.fk_publico_autor = request.user.extensionusuario.Publico
                    tags = request.POST.get("tagResource")
                    if "," in tags:
                        tags = tags.split(",")
                    else:
                        tags = [tags]
                    newRecurso.save()
                    for newtag in tags:
                        tag = Tag.objects.filter(desc_tag=newtag)
                        if tag.exists():
                            tag_recurso = TagRecurso(fk_tag=tag[0], fk_recurso=newRecurso)
                            tag_recurso.save()
                        else:
                            tag = Tag(desc_tag=newtag)
                            tag.save()
                            tag_recurso = TagRecurso(fk_tag=tag, fk_recurso=newRecurso)
                            tag_recurso.save()
                    #add resources
                    recursos.append({"id":newRecurso.pk, "path":newRecurso.path, "type":resourceType})
                return JsonResponse({"message":"Perfect", "recursos":recursos})
            else:
                data = json.load(request)
                if data["method"] == "Show":
                    #nananananananana batmannnn
                    recursos = Recurso.objects.filter(fk_publico_autor=request.user.extensionusuario.Publico) | Recurso.objects.filter(compartido=True)
                    recursos = recursos.order_by('-id_recurso')[:10]
                    tags = Tag.objects.all().order_by('desc_tag')
                    context["recursos"] = recursos
                    context["tags"] = tags
                    html_template = (loader.get_template('components/modalBancoRecursos.html'))
                    return HttpResponse(html_template.render(context, request))
                elif data["method"] == "Find":
                    modelo = Paginas.objects.get(pk=data["id"])
                    context = {"modelo": modelo}
                    html_template = (loader.get_template('components/modalAddPagina.html'))
                    return HttpResponse(html_template.render(context, request))
                elif data["method"] == "Create":
                    recurso = Recurso.objects.filter(path=data["data"]["path"])
                    if recurso.exists():
                        return JsonResponse({"message":"Already exists", "id":recurso[0].pk, "path":recurso[0].path})
                    else:
                        newRecurso = Recurso()
                        newRecurso.titulo = data["data"]["titulo"]
                        newRecurso.path = data["data"]["path"]
                        newRecurso.tipo_path = data["data"]["tipo_path"]
                        newRecurso.compartido = data["data"]["compartido"]
                        newRecurso.fk_tipo_recurso = TablasConfiguracion.obtenerHijos("Recurso").get(valor_elemento=data["data"]["tipo_recurso"])
                        newRecurso.fk_publico_autor = request.user.extensionusuario.Publico
                        tags = data["data"]["tags"]
                        if "," in tags:
                            tags = tags.split(",")
                        else:
                            tags = [tags]
                        newRecurso.save()
                        for newtag in tags:
                            tag = Tag.objects.filter(desc_tag=newtag)
                            if tag.exists():
                                tag_recurso = TagRecurso(fk_tag=tag[0], fk_recurso=newRecurso)
                                tag_recurso.save()
                            else:
                                tag = Tag(desc_tag=newtag)
                                tag.save()
                                tag_recurso = TagRecurso(fk_tag=tag, fk_recurso=newRecurso)
                                tag_recurso.save()
                        return JsonResponse({"message":"Perfect", "id":newRecurso.pk, "path":newRecurso.path, "type":"Recurso_video"})
                
            # except:
            #     return JsonResponse({"message":"error"}, status=500)
    

@login_required(login_url="/login/")
def getModalChooseActivities(request):
    context = {}
    html_template = (loader.get_template('components/modalEscogerActividad.html'))
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def getModalChooseTypeQuestion(request):
    context = {}
    html_template = (loader.get_template('components/modalTypeQuestion.html'))
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def sortPreguntas(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                context = {}
                data = json.load(request)["data"]

                if data["method"] == "Sort":
                        print(data["order"])
                        for item in data["order"]:
                            pregunta = EvaluacionesPreguntas.objects.get(pk=item["pk"])
                            print(pregunta)
                            pregunta.orden= item["order"]
                            pregunta.save()

                
                return JsonResponse({"message": "Perfect"})     
            except:
                return JsonResponse({"message": "Error"}) 

@login_required(login_url="/login/")
def getModalAddRespuestas(request):
     if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                context = {}
                data = json.load(request)["data"]
                

                if data["method"] == "Get":
                        
                    sugerencias=SugerenciasBloques.objects.annotate(nombreEscala=F('escalaOpcion__desc_calificacion'), nombreEstructura=F('fk_estructura_programa__descripcion') ).filter(fk_bloque=data['idBlock'])
                    listaChilds = list(sugerencias.values())
                    
                    return JsonResponse({"childs":listaChilds}, safe=False)
                
                if data["method"] == "Show":
                        structurasAll=Estructuraprograma.objects.all()
                        structurasAll=structurasAll.annotate(precio=F('prize__precio'), fechaIngreso=F('prize__fecha_registro'), id=F('prize__idprograma_precios'), descuento=F('prize__PorcentajeDescuento'), max=Max('prize__idprograma_precios'), amountDiscount=Max('prize__idprograma_precios')  ).filter(id=Max('prize__idprograma_precios')  )

                        structurasAll=structurasAll.exclude(precio=None)

                        bloque=EvaluacionesBloques.objects.get(pk=data['idBlock'])
                        escalaBloque=bloque.fk_actividad_evaluaciones.fk_escala_bloque.escalaMenor.all()

                        context={
                            'structurasAll':structurasAll,
                            'scale':escalaBloque

                        }
                            

                        html_template = (loader.get_template('components/modalAddRespuestas.html'))
                        return HttpResponse(html_template.render(context, request))
                        return JsonResponse({"message": "Perfect"})     

                if data["method"] == "Save":
                     sugerencias=SugerenciasBloques.objects.filter(fk_bloque=data['idBlock'])
                     sugerencias.delete()
                     bloque=EvaluacionesBloques.objects.get(pk=data['idBlock'])
                     hijos = data["hijos"]
                     if hijos:   
                                for newOpcion in hijos:
                                    
                                    newSugerencia=SugerenciasBloques()
                                    newSugerencia.fk_bloque=bloque
                                    newSugerencia.comentario=newOpcion['Comment']
                                    scale=EscalaCalificacion.objects.get(pk=newOpcion['scale'])
                                    newSugerencia.escalaOpcion=scale

                                    if newOpcion['structura'] and newOpcion['structura']!='' and newOpcion['structura']!=' ':
                                        estructura=Estructuraprograma.objects.get(pk=newOpcion['structura'])
                                        newSugerencia.fk_estructura_programa=estructura
                                    
                                   
                                    newSugerencia.save()
                     return JsonResponse({"message": "Saved"})
            except:
                return JsonResponse({"message": "Error"}) 

@login_required(login_url="/login/")
def getModalAddBlock(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
            
                context = {}
                data = json.load(request)["data"]
                
                if "delete" in data:
                    print('sss')
                    bloque=EvaluacionesBloques.objects.get(pk=data["id"])
                    actividad = bloque.fk_actividad_evaluaciones

                    actividad.pointUse=actividad.pointUse-actividad.fk_escala_bloque.maxima_puntuacion
                    actividad.save()

                    bloque.delete()
                     #update order
                    bloques = actividad.bloque_actividad.order_by('orden')
                    for idx, value in enumerate(bloques, start=1):
                        value.orden = idx
                        value.save()
                    return JsonResponse({"message": "Deleted"})
                if data["method"] == "Sort":
                        print(data["order"])
                        for item in data["order"]:
                            bloque = EvaluacionesBloques.objects.get(pk=item["pk"])
                            print(bloque)
                            bloque.orden= item["order"]
                            bloque.save()
                if data["method"] == "get":
                    
                    bloque=EvaluacionesBloques.objects.filter(pk=data["idFind"])
                    findBloque = list(bloque.values())
                    
                    return JsonResponse({"data":findBloque[0]}, safe=False)
                
                if data["method"] == "Show":
                        context = {}
                        html_template = (loader.get_template('components/modalAddBlock.html'))
                        return HttpResponse(html_template.render(context, request))

                if data["method"] == "Update":
                    bloque=EvaluacionesBloques.objects.get(pk=int(data["idViejo"]))
                    
                    bloque.comentario=data['textoBloque']
                    bloque.titulo_bloque=data['tituloBloque']
                    bloque.save()



                if data["method"] == "Create":
                    actividad=ActividadEvaluaciones.objects.annotate(num_child=Count('bloque_actividad', distinct=True) ).get(pk=data['ActivityId'])
                    actividad.pointUse=actividad.pointUse+actividad.fk_escala_bloque.maxima_puntuacion
                    actividad.save()
                    bloque=EvaluacionesBloques.objects.create()

                    newOrden=actividad.num_child+1
                    bloque.orden=newOrden
                    print('aquitoy')

                    bloque.fk_actividad_evaluaciones=actividad
                    bloque.comentario=data['textoBloque']
                    bloque.titulo_bloque=data['tituloBloque']
                    print('eeeee')

                    bloque.save()


             
                return JsonResponse({"message": "Perfect"})     
            except:
                return JsonResponse({"message": "Error"}) 
           
    context = {}
    html_template = (loader.get_template('components/modalAddBlock.html'))
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def getModalAddInstructions(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
            
                context = {}
                data = json.load(request)["data"]

                if data["method"] == "delete":
                     instrucciones=None
                     instrucciones=EvaluacionInstrucciones.objects.filter(fk_actividad_evaluaciones=data["ActivityId"])
                     if instrucciones.count()>0:
                                instrucciones=instrucciones[0]
                                instrucciones.delete()
                     return JsonResponse({"message": "Deleted"})
                
                if data["method"] == "Show":
                        instrucciones=None
                        if "idTest" in data:
                            instrucciones=EvaluacionInstrucciones.objects.filter(fk_actividad_evaluaciones=data["idTest"])
                            if instrucciones.count()>0:
                                instrucciones=instrucciones[0]

                        context = {
                            'instrucciones':instrucciones

                        }
                        html_template = (loader.get_template('components/modalAddInstrucciones.html'))
                        return HttpResponse(html_template.render(context, request))

                if data["method"] == "Add":
                     instrucciones=None
                     instrucciones=EvaluacionInstrucciones.objects.filter(fk_actividad_evaluaciones=data["ActivityId"])
                     if instrucciones.count()>0:
                                instrucciones=instrucciones[0]
                                instrucciones.delete()
                     actividad=ActividadEvaluaciones.objects.get(pk=data["ActivityId"])
                     nuevaInstruccion=EvaluacionInstrucciones.objects.create( texto_instrucciones=data["texto"], fk_actividad_evaluaciones=actividad)
                     nuevaInstruccion.save()
                     return JsonResponse({"message": "Saved"})

                    
                return JsonResponse({"message": "Perfect"})     
            except:
                return JsonResponse({"message": "Error"}) 
           
    context = {}
    html_template = (loader.get_template('components/modalAddBlock.html'))
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def getModalNewTest(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            modelo = {}
            try:
                if request.body:
                        data = json.load(request)
                        tipoDuracion = TablasConfiguracion.obtenerHijos(valor="Duracion")
                        escalas = EscalaEvaluacion.objects.all()
                        if data["method"] == "Show":
                            context = {"escalas":escalas, "tipoDuracion":tipoDuracion}
                            html_template = (loader.get_template('components/modalAddTest.html'))
                            return HttpResponse(html_template.render(context, request))
                        elif data["method"] == "Find":
                            modelo = ActividadEvaluaciones.objects.get(fk_estructura_programa=data["id"])
                            context = {"modelo": modelo, "escalas":escalas, "tipoDuracion":tipoDuracion}
                            html_template = (loader.get_template('components/modalAddTest.html'))
                            return HttpResponse(html_template.render(context, request))
                        elif data["method"] == "Delete":
                            actividad = Estructuraprograma.objects.get(pk=data["id"])
                            actividad.delete()
                            return JsonResponse({"message":"Deleted"})
                        elif data["method"] == "Update":
                            actividad = Estructuraprograma.objects.get(pk=data["id"])
                            test = ActividadEvaluaciones.objects.get(fk_estructura_programa=data["id"])
                        elif data["method"] == "Create":
                            actividad = Estructuraprograma()
                            test = ActividadEvaluaciones()
                            actividad.valor_elemento = "Activity"
                            actividad.pointUsed = 0
                            actividad.fk_estructura_padre_id=data["padreActivity"]
                            actividad.orden_presentacion = len(Estructuraprograma.objects.filter(fk_estructura_padre=data["padreActivity"]))
                        actividad.descripcion = data["data"]["descriptionActivity"]
                        actividad.resumen = data["data"]["resumenActivity"]
                        actividad.url = data["data"]["urlActivity"]
                        actividad.peso_creditos = None
                        actividad.fk_categoria_id = TablasConfiguracion.obtenerHijos(valor="Tipo Actividad").get(valor_elemento="activityTest").pk
                        if "checkExpertCB" in data["data"]:
                            actividad.fk_categoria_id = TablasConfiguracion.obtenerHijos(valor="Tipo Actividad").get(valor_elemento="activityExpert test").pk
                            scale=EscalaEvaluacion.objects.get(pk=int(data["data"]["Blockqualification"]))
                            test.fk_escala_bloque = scale
                        else:   
                            test.nro_repeticiones = data["data"]["repeats"]
                            test.calificacion_aprobar = data["data"]["minApp"]
                            test.fk_tipo_duracion_id=TablasConfiguracion.objects.get(valor_elemento='duracionMinutes').pk

                        if "durationActivity" in data["data"]:
                            test.duracion = data["data"]["durationActivity"]

                        else:
                            test.duracion = None
                   #     if "timeActivity" in data["data"]:
                    #        test.fk_tipo_duracion_id = data["data"]["timeActivity"]
                     #   else:
                      #      test.fk_tipo_duracion_id = None
                    
                        test.fk_escala_evaluacion_id = data["data"]["qualification"]
                        actividad.save()
                        test.fk_estructura_programa = actividad
                        test.save()
                        if data["method"] == "Create":
                            if not "checkExpertCB" in data["data"]:
                                bloque=EvaluacionesBloques.objects.create()
                                bloque.titulo_bloque=actividad.descripcion
                                #bloque.titulo_bloque='Test'
                                
                                bloque.orden=1
                                bloque.comentario=''
                                bloque.fk_actividad_evaluaciones=test
                                bloque.fk_escala_bloque=None   
                                bloque.save()
                        return JsonResponse({"message":"Perfect"})
            except:
                 return JsonResponse({"message":"error"}, status=500)

@login_required(login_url="/login/")
def getModalNewLesson(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            modelo = {}
            try:
                if request.body:
                    data = json.load(request)
                    status = TablasConfiguracion.obtenerHijos(valor="EstLeccion")
                    if data["method"] == "Show":
                        context = {"status":status}
                        html_template = (loader.get_template('components/modalAddLesson.html'))
                        return HttpResponse(html_template.render(context, request))
                    elif data["method"] == "Find":
                        modelo = ActividadLeccion.objects.get(fk_estructura_programa=data["id"])
                        context = {"modelo": modelo, "status":status}
                        html_template = (loader.get_template('components/modalAddLesson.html'))
                        return HttpResponse(html_template.render(context, request))
                    elif data["method"] == "Delete":
                        actividad = Estructuraprograma.objects.get(pk=data["id"])
                        actividad.delete()
                        return JsonResponse({"message":"Deleted"})
                    elif data["method"] == "Update":
                        actividad = Estructuraprograma.objects.get(pk=data["id"])
                        lesson = ActividadLeccion.objects.get(fk_estructura_programa=data["id"])
                    elif data["method"] == "Create":
                        actividad = Estructuraprograma()
                        lesson = ActividadLeccion()
                        actividad.valor_elemento = "Activity"
                        actividad.fk_estructura_padre_id=data["padreActivity"]
                        actividad.orden_presentacion = len(Estructuraprograma.objects.filter(fk_estructura_padre=data["padreActivity"]))
                    actividad.descripcion = data["data"]["descriptionActivity"]
                    actividad.resumen = data["data"]["resumenActivity"]
                    actividad.url = data["data"]["urlActivity"]
                    actividad.peso_creditos = None
                    actividad.fk_categoria_id = TablasConfiguracion.obtenerHijos(valor="Tipo Actividad").get(valor_elemento="activityLesson").pk
                    lesson.disponible_desde = data["data"]["disponibleLesson"]
                    lesson.estatus_id = data["data"]["estatusLesson"]
                    actividad.save()
                    lesson.fk_estructura_programa = actividad
                    lesson.save()
                    return JsonResponse({"message":"Perfect"})
            except:
                return JsonResponse({"message":"error"}, status=500)

@login_required(login_url="/login/")
def getModalNewHomework(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            modelo = {}
            try:
                if request.body:
                    data = json.load(request)
                    if data["method"] == "Show":
                        html_template = (loader.get_template('components/modalAddHomework.html'))
                        return HttpResponse(html_template.render(context, request))
                    elif data["method"] == "Find":
                        modelo = ActividadTarea.objects.get(fk_estructura_programa=data["id"])
                        pagina = modelo.fk_estructura_programa.paginas_set.all()[0]
                        context = {"modelo": modelo, "pagina":pagina}
                        html_template = (loader.get_template('components/modalAddHomework.html'))
                        return HttpResponse(html_template.render(context, request))
                    elif data["method"] == "Delete":
                        actividad = Estructuraprograma.objects.get(pk=data["id"])
                        actividad.delete()
                        return JsonResponse({"message":"Deleted"})
                    elif data["method"] == "Update":
                        actividad = Estructuraprograma.objects.get(pk=data["id"])
                        pagina = actividad.paginas_set.all()[0]
                        homework = ActividadTarea.objects.get(fk_estructura_programa=data["id"])
                    elif data["method"] == "Create":
                        actividad = Estructuraprograma()
                        homework = ActividadTarea()
                        actividad.valor_elemento = "Activity"
                        actividad.fk_categoria_id = TablasConfiguracion.obtenerHijos(valor="Tipo Actividad").get(valor_elemento="activityHome").pk
                        actividad.fk_estructura_padre_id=data["padreActivity"]
                        actividad.orden_presentacion = len(Estructuraprograma.objects.filter(fk_estructura_padre=data["padreActivity"]))
                        pagina = Paginas()
                        pagina.titulo = ""
                        pagina.contenido = ""
                        pagina.ordenamiento = None
                    actividad.descripcion = data["data"]["descriptionActivity"]
                    actividad.resumen = data["data"]["resumenActivity"]
                    actividad.url = data["data"]["urlActivity"]
                    actividad.peso_creditos = None
                    actividad.save()
                    pagina.fk_estructura_programa = actividad
                    pagina.titulo = actividad.descripcion
                    pagina.contenido = None
                    if data["data"]["summernote"] != "<p><br></p>":
                        pagina.contenido = data["data"]["summernote"]
                    pagina.save()
                    recursos = data["data"]["recursos"]
                    oldResources = RecursoPaginas.objects.filter(fk_pagina=pagina.pk)
                    oldResources.delete()
                    for recurso in recursos:
                        resource = Recurso.objects.get(pk=recurso["id"])
                        newResource = RecursoPaginas()
                        newResource.fk_pagina = pagina
                        newResource.fk_recurso = resource
                        newResource.save()
                    homework.fk_estructura_programa = actividad
                    homework.fecha_entrega = data["data"]["entregaHomework"]
                    homework.save()
                    return JsonResponse({"message":"Perfect"})
            except:
                return JsonResponse({"message":"error"}, status=500)

@login_required(login_url="/login/")
def getModalNewForum(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            modelo = {}
            try:
                if request.body:
                    data = json.load(request)
                    if data["method"] == "Show":
                        html_template = (loader.get_template('components/modalAddForum.html'))
                        return HttpResponse(html_template.render(context, request))
                    elif data["method"] == "Find":
                        modelo = ActividadConferencia.objects.get(fk_estructura_programa=data["id"])
                        context = {"modelo": modelo}
                        html_template = (loader.get_template('components/modalAddForum.html'))
                        return HttpResponse(html_template.render(context, request))
                    elif data["method"] == "Delete":
                        actividad = Estructuraprograma.objects.get(pk=data["id"])
                        actividad.delete()
                        return JsonResponse({"message":"Deleted"})
                    elif data["method"] == "Update":
                        actividad = Estructuraprograma.objects.get(pk=data["id"])
                        forum = ActividadConferencia.objects.get(fk_estructura_programa=data["id"])
                    elif data["method"] == "Create":
                        actividad = Estructuraprograma()
                        forum = ActividadConferencia()
                        actividad.valor_elemento = "Activity"
                        actividad.fk_categoria_id = TablasConfiguracion.obtenerHijos(valor="Tipo Actividad").get(valor_elemento="activityForum").pk
                        actividad.fk_estructura_padre_id=data["padreActivity"]
                        actividad.orden_presentacion = len(Estructuraprograma.objects.filter(fk_estructura_padre=data["padreActivity"]))
                    actividad.descripcion = data["data"]["descriptionActivity"]
                    actividad.resumen = data["data"]["resumenActivity"]
                    actividad.url = data["data"]["urlActivity"]
                    actividad.peso_creditos = None
                    forum.fecha_hora = data["data"]["datetimeForum"]
                    forum.enlace = data["data"]["linkForum"]
                    forum.id_conferencia = data["data"]["idForum"]
                    forum.clave = data["data"]["keyForum"]
                    # forum.fk_publico
                    actividad.save()
                    forum.fk_estructura_programa = actividad
                    forum.save()
                    return JsonResponse({"message":"Perfect"})
            except:
                return JsonResponse({"message":"error"}, status=500)

@login_required(login_url="/login/")
def getModalQuestion(request): 
    context = {
        "tipoPreguntas" : TablasConfiguracion.obtenerHijos('PregEvalua'),
    }
    html_template = (loader.get_template('components/modalAddQuestion.html'))
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def getModalNewSimple(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            
            
                context = {}
                data = json.load(request)["data"]

                if "delete" in data:
                    pregunta=EvaluacionesPreguntas.objects.get(pk=data["id"])
                    bloque = pregunta.fk_evaluaciones_bloque
                    bloque.pointUse=bloque.pointUse-pregunta.puntos_pregunta
                    actividad=bloque.fk_actividad_evaluaciones
                    actividad.pointUse=actividad.pointUse-pregunta.puntos_pregunta
                    bloque.save()

                    actividad.save()

                    pregunta.delete()
                    
                    preguntas = bloque.bloque_pregunta.order_by('orden')
                    for idx, value in enumerate(preguntas, start=1):
                        value.orden = idx
                        value.save()
                    return JsonResponse({"message": "Deleted"})
                if "idFind" in data:
                    print(data)
                    pregunta=EvaluacionesPreguntas.objects.filter(pk=data["idFind"])
                    findpregunta = list(pregunta.values())
                    childs = PreguntasOpciones.objects.filter(fk_evaluacion_pregunta=data["idFind"])
                    listaChilds = list(childs.values())
                    return JsonResponse({"data":findpregunta[0], "childs":listaChilds}, safe=False)
                
                if data["method"] == "Show":
                        context = {}
                        html_template = (loader.get_template('components/modalAddSimple.html'))
                        return HttpResponse(html_template.render(context, request))

                if data["method"] == "Update":
                    pregunta=EvaluacionesPreguntas.objects.get(pk=data["idViejo"])
                    bloque=EvaluacionesBloques.objects.annotate(num_child=Count('bloque_pregunta', distinct=True) ).get(pk=data['fatherId'])
                  
                    pregunta.orden=pregunta.orden

                    pregunta.fk_evaluaciones_bloque=bloque
                    pregunta.texto_pregunta=data['textoPregunta']
                    pregunta.titulo_pregunta=data['tituloPregunta']


                    actividad=ActividadEvaluaciones.objects.get(pk=bloque.fk_actividad_evaluaciones.pk)
                    actividad.pointUse=float(actividad.pointUse)-float(bloque.pointUse)
                    bloque.pointUse=float(bloque.pointUse)-float(pregunta.puntos_pregunta)+float(data['puntosPregunta'])
                    actividad.pointUse=float(actividad.pointUse)+float(bloque.pointUse)
                    bloque.save()
                    actividad.save()


                    pregunta.puntos_pregunta=data['puntosPregunta']

                    
                    pregunta.fk_tipo_pregunta_evaluacion=Methods.OrigenPreguntaTipo('Simple')
                    pregunta.save()
                    childs = PreguntasOpciones.objects.filter(fk_evaluacion_pregunta=data["idViejo"])
                    
                    hijos = data["hijos"]
                    if hijos:
                            print(hijos)
                        
                            if "idViejo" in data:
                                 
                                 childs.delete()
                            selectetedOp=int(data['select2'])     
                            for newOpcion in hijos:
                                
                                 Opcion=PreguntasOpciones()
                                 Opcion.fk_evaluacion_pregunta=pregunta
                                 Opcion.texto_opcion=newOpcion['OpcionText']   
                                 Opcion.idLista=newOpcion['id']    
                                 Opcion.respuetaCorrecta=True if newOpcion['id']==selectetedOp else False
                                 Opcion.save()

                if data["method"] == "Create":
                    pregunta=EvaluacionesPreguntas.objects.create()

                    print(data)
                    bloque=EvaluacionesBloques.objects.annotate(num_child=Count('bloque_pregunta', distinct=True) ).get(pk=data['fatherId'])
                    newOrden=bloque.num_child+1
                    pregunta.orden=newOrden

                    pregunta.fk_evaluaciones_bloque=bloque
                    pregunta.texto_pregunta=data['textoPregunta']
                    pregunta.titulo_pregunta=data['tituloPregunta']


                    pregunta.puntos_pregunta=data['puntosPregunta']
                   
                    bloque.pointUse=float(bloque.pointUse)+float(pregunta.puntos_pregunta)
                    actividad=ActividadEvaluaciones.objects.get(pk=bloque.fk_actividad_evaluaciones.pk)
                    actividad.pointUse=float(pregunta.puntos_pregunta)+float(actividad.pointUse)
                    bloque.save()
                    actividad.save()


                    pregunta.fk_tipo_pregunta_evaluacion=Methods.OrigenPreguntaTipo('Simple')
                    pregunta.save()

                    hijos = data["hijos"]
                    if hijos:
                            print(hijos)
                        
                            if "idViejo" in data:
                        
                                 childs.delete()
                            selectetedOp=int(data['select2'])     
                            for newOpcion in hijos:
                                
                                 Opcion=PreguntasOpciones()
                                 Opcion.fk_evaluacion_pregunta=pregunta
                                 Opcion.texto_opcion=newOpcion['OpcionText']   
                                 Opcion.idLista=newOpcion['id']    
                                 Opcion.respuetaCorrecta=True if newOpcion['id']==selectetedOp else False
                                 Opcion.save()

             
                return JsonResponse({"message": "Perfect"})     
            
           
   
    context = {}
    html_template = (loader.get_template('components/modalAddSimple.html'))
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def getModalNewExpert(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
         
                context = {}
                data = json.load(request)["data"]

                if "delete" in data:
                    pregunta=EvaluacionesPreguntas.objects.get(pk=data["id"])
                    bloque = pregunta.fk_evaluaciones_bloque
                    bloque.pointUse=bloque.pointUse-pregunta.puntos_pregunta
                    bloque.save()
                    pregunta.delete()
                   


                    
                    preguntas = bloque.bloque_pregunta.order_by('orden')
                    for idx, value in enumerate(preguntas, start=1):
                        value.orden = idx
                        value.save()
                    return JsonResponse({"message": "Deleted"})
                if "idFind" in data:
                    
                    pregunta=EvaluacionesPreguntas.objects.filter(pk=data["idFind"])
                    findpregunta = list(pregunta.values())
                    childs = PreguntasOpciones.objects.filter(fk_evaluacion_pregunta=data["idFind"])
                    listaChilds = list(childs.values())
                    return JsonResponse({"data":findpregunta[0], "childs":listaChilds}, safe=False)
                
                if data["method"] == "Show":
                        context = {}
                        html_template = (loader.get_template('components/modalAddQuestionExpert.html'))
                        return HttpResponse(html_template.render(context, request))

                if data["method"] == "Update":
                    pregunta=EvaluacionesPreguntas.objects.get(pk=data["idViejo"])
                    bloque=EvaluacionesBloques.objects.annotate(num_child=Count('bloque_pregunta', distinct=True) ).get(pk=data['fatherId'])
                  
                    pregunta.orden=pregunta.orden

                    pregunta.fk_evaluaciones_bloque=bloque
                    pregunta.texto_pregunta=data['textoPregunta']
                    pregunta.titulo_pregunta=data['tituloPregunta']
                    
                    bloque.pointUse=float(bloque.pointUse)-float(pregunta.puntos_pregunta)+float(data['puntosPregunta'])
                    
                    bloque.save()
                   


                    pregunta.puntos_pregunta=data['puntosPregunta']
                    pregunta.fk_tipo_pregunta_evaluacion=Methods.OrigenPreguntaTipo('Expert')
                    pregunta.save()
                    childs = PreguntasOpciones.objects.filter(fk_evaluacion_pregunta=data["idViejo"])
                    
                    hijos = data["hijos"]
                    if hijos:
                            print(hijos)
                        
                            if "idViejo" in data:
                                 
                                 childs.delete()
            
                            for newOpcion in hijos:
                                
                                 Opcion=PreguntasOpciones()
                                 Opcion.fk_evaluacion_pregunta=pregunta
                                 Opcion.texto_opcion=newOpcion['OpcionText']   
                                 Opcion.idLista=newOpcion['id']    
                                 Opcion.puntos_porc=float(newOpcion['value'])  

                                 Opcion.save()
             
                
                if data["method"] == "Create":
                 
                    pregunta=EvaluacionesPreguntas.objects.create()
                    bloque=EvaluacionesBloques.objects.annotate(num_child=Count('bloque_pregunta', distinct=True) ).get(pk=data['fatherId'])
            
                    
                    newOrden=bloque.num_child+1
                    pregunta.orden=newOrden
                    pregunta.fk_evaluaciones_bloque=bloque
                    pregunta.texto_pregunta=data['textoPregunta']
                    pregunta.titulo_pregunta=data['tituloPregunta']

                    pregunta.puntos_pregunta=data['puntosPregunta']
                    bloque.pointUse=float(bloque.pointUse)+float(pregunta.puntos_pregunta)
                    
                    bloque.save()
                   
                    pregunta.fk_tipo_pregunta_evaluacion=Methods.OrigenPreguntaTipo('Expert')
                    pregunta.save()

                    hijos = data["hijos"]
                    if hijos:
                            print(hijos)
                        
                            if "idViejo" in data:
                                 childs =None
                                 childs.delete()
                         
                            for newOpcion in hijos:
                                 Opcion=PreguntasOpciones()
                                 Opcion.fk_evaluacion_pregunta=pregunta
                                 Opcion.idLista=newOpcion['id']    

                                 Opcion.texto_opcion=newOpcion['OpcionText']    
                                 Opcion.puntos_porc=float(newOpcion['value'])  
                                 Opcion.save()

             
                return JsonResponse({"message": "Perfect"})     
           
           
   
    context = {}
    html_template = (loader.get_template('components/modalAddSimple.html'))
    return HttpResponse(html_template.render(context, request))    
    
@login_required(login_url="/login/")
def getModalNewMultiple(request):

    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                context = {}
                data = json.load(request)["data"]
                if "delete" in data:
                    pregunta=EvaluacionesPreguntas.objects.get(pk=data["id"])
                    bloque = pregunta.fk_evaluaciones_bloque
                    bloque.pointUse=bloque.pointUse-pregunta.puntos_pregunta
                    actividad=bloque.fk_actividad_evaluaciones
                    actividad.pointUse=actividad.pointUse-pregunta.puntos_pregunta
                    bloque.save()

                    actividad.save()

                    pregunta.delete()
                    
                    preguntas = bloque.bloque_pregunta.order_by('orden')
                    for idx, value in enumerate(preguntas, start=1):
                        value.orden = idx
                        value.save()
                    return JsonResponse({"message": "Deleted"})
                
               
                if "idFind" in data:
                  #  print(data)
                    pregunta=EvaluacionesPreguntas.objects.filter(pk=data["idFind"])
                    findpregunta = list(pregunta.values())
                    childs = PreguntasOpciones.objects.filter(fk_evaluacion_pregunta=data["idFind"])
                    listaChilds = list(childs.values())
                    return JsonResponse({"data":findpregunta[0], "childs":listaChilds}, safe=False)
                if data["method"] == "Show":
                        context = {}
                        html_template = (loader.get_template('components/modalAddMultiple.html'))
                        return HttpResponse(html_template.render(context, request))
                if data["method"] == "Update":
                    pregunta=EvaluacionesPreguntas.objects.get(pk=data["idViejo"])
                    bloque=EvaluacionesBloques.objects.annotate(num_child=Count('bloque_pregunta', distinct=True) ).get(pk=data['fatherId'])
                  
                    pregunta.orden=pregunta.orden

                    pregunta.fk_evaluaciones_bloque=bloque
                    pregunta.texto_pregunta=data['textoPregunta']
                    pregunta.titulo_pregunta=data['tituloPregunta']
                    actividad=ActividadEvaluaciones.objects.get(pk=bloque.fk_actividad_evaluaciones.pk)
                    actividad.pointUse=float(actividad.pointUse)-float(bloque.pointUse)
                    bloque.pointUse=float(bloque.pointUse)-float(pregunta.puntos_pregunta)+float(data['puntosPregunta'])
                    actividad.pointUse=float(actividad.pointUse)+float(bloque.pointUse)
                    bloque.save()
                    actividad.save()


                    pregunta.puntos_pregunta=data['puntosPregunta']
                    pregunta.fk_tipo_pregunta_evaluacion=Methods.OrigenPreguntaTipo('Multiple')
                    pregunta.save()
                    childs = PreguntasOpciones.objects.filter(fk_evaluacion_pregunta=data["idViejo"])
                    
                    hijos = data["hijos"]
                    if hijos:
                            print(hijos)
                        
                            if "idViejo" in data:
                                 
                                 childs.delete()
            
                            for newOpcion in hijos:
                                
                                 Opcion=PreguntasOpciones()
                                 Opcion.fk_evaluacion_pregunta=pregunta
                                 Opcion.texto_opcion=newOpcion['OpcionText']   
                                 Opcion.idLista=newOpcion['id']    
                                 Opcion.puntos_porc=float(newOpcion['value'])  

                                 Opcion.save()
                
                if data["method"] == "Create":
                    pregunta=EvaluacionesPreguntas.objects.create()
                    bloque=EvaluacionesBloques.objects.annotate(num_child=Count('bloque_pregunta', distinct=True) ).get(pk=data['fatherId'])
                    newOrden=bloque.num_child+1
                    pregunta.orden=newOrden
                    pregunta.fk_evaluaciones_bloque=bloque
                    pregunta.texto_pregunta=data['textoPregunta']
                    pregunta.titulo_pregunta=data['tituloPregunta']

                    pregunta.puntos_pregunta=data['puntosPregunta']
                    bloque.pointUse=float(bloque.pointUse)+float(pregunta.puntos_pregunta)
                    actividad=ActividadEvaluaciones.objects.get(pk=bloque.fk_actividad_evaluaciones.pk)
                    actividad.pointUse=float(pregunta.puntos_pregunta)+float(actividad.pointUse)

                    bloque.save()
                    actividad.save()
                    pregunta.fk_tipo_pregunta_evaluacion=Methods.OrigenPreguntaTipo('Multiple')
                    pregunta.save()

                    hijos = data["hijos"]
                    if hijos:
                            print(hijos)
                        
                            if "idViejo" in data:
                                 childs =None
                                 childs.delete()
                         
                            for newOpcion in hijos:
                                 Opcion=PreguntasOpciones()
                                 Opcion.fk_evaluacion_pregunta=pregunta
                                 Opcion.idLista=newOpcion['id']    

                                 Opcion.texto_opcion=newOpcion['OpcionText']    
                                 Opcion.puntos_porc=float(newOpcion['value'])  
                                 Opcion.save()

             
                return JsonResponse({"message": "Perfect"})      
            except:
                return JsonResponse({"message": "Error"})
   
    context ={}
    html_template = (loader.get_template('components/modalAddMultiple.html'))
    return HttpResponse(html_template.render(context, request))
    
@login_required(login_url="/login/")
def getModalNewCompletion(request):

     if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                context = {}
                data = json.load(request)["data"]
                print(data)
                if "delete" in data:
                    pregunta=EvaluacionesPreguntas.objects.get(pk=data["id"])
                    bloque = pregunta.fk_evaluaciones_bloque
                    bloque.pointUse=bloque.pointUse-pregunta.puntos_pregunta
                    actividad=bloque.fk_actividad_evaluaciones
                    actividad.pointUse=actividad.pointUse-pregunta.puntos_pregunta
                    bloque.save()

                    actividad.save()

                    pregunta.delete()
                    
                    preguntas = bloque.bloque_pregunta.order_by('orden')
                    for idx, value in enumerate(preguntas, start=1):
                        value.orden = idx
                        value.save()
                    return JsonResponse({"message": "Deleted"})
                
               
                if "idFind" in data:
                    print(data)
                    pregunta=EvaluacionesPreguntas.objects.filter(pk=data["idFind"])
                    findpregunta = list(pregunta.values())
                    childs = PreguntasOpciones.objects.filter(fk_evaluacion_pregunta=data["idFind"])
                    listaChilds = list(childs.values())
                    return JsonResponse({"data":findpregunta[0], "childs":listaChilds}, safe=False)
                
                if data["method"] == "Show":
                        context = {}
                        html_template = (loader.get_template('components/modalAddCompletion.html'))
                        return HttpResponse(html_template.render(context, request))
                if data["method"] == "Update":
                    pregunta=EvaluacionesPreguntas.objects.get(pk=data["idViejo"])
                    bloque=EvaluacionesBloques.objects.annotate(num_child=Count('bloque_pregunta', distinct=True) ).get(pk=data['fatherId'])
                  
                    pregunta.orden=pregunta.orden

                    pregunta.fk_evaluaciones_bloque=bloque
                    pregunta.texto_pregunta=data['textoPregunta']
                    pregunta.titulo_pregunta=data['tituloPregunta']
                    pregunta.indicePalabra=data['indiceRespuesta']
                    actividad=ActividadEvaluaciones.objects.get(pk=bloque.fk_actividad_evaluaciones.pk)
                    actividad.pointUse=float(actividad.pointUse)-float(bloque.pointUse)
                    bloque.pointUse=float(bloque.pointUse)-float(pregunta.puntos_pregunta)+float(data['puntosPregunta'])
                    actividad.pointUse=float(actividad.pointUse)+float(bloque.pointUse)
                    bloque.save()
                    actividad.save()
                    pregunta.puntos_pregunta=data['puntosPregunta']
                    pregunta.fk_tipo_pregunta_evaluacion=Methods.OrigenPreguntaTipo('Completation')
                    pregunta.save()
                    childs = PreguntasOpciones.objects.filter(fk_evaluacion_pregunta=data["idViejo"])
                    hijos = data["hijos"]
                    if hijos:
                            print(hijos)
                        
                            if "idViejo" in data:
                                 
                                 childs.delete()
            
                            for newOpcion in hijos:
                                
                                 Opcion=PreguntasOpciones()
                                 Opcion.fk_evaluacion_pregunta=pregunta
                                 Opcion.fk_evaluacion_pregunta=pregunta
                                 Opcion.texto_opcion=newOpcion['OpcionText']   
                                 Opcion.idLista=newOpcion['id']    

                                 Opcion.respuetaCorrecta=int(newOpcion['isCorrect']) 

                                 Opcion.save()
                
                if data["method"] == "Create":
                    pregunta=EvaluacionesPreguntas.objects.create()
                    bloque=EvaluacionesBloques.objects.annotate(num_child=Count('bloque_pregunta', distinct=True) ).get(pk=data['fatherId'])
                    newOrden=bloque.num_child+1
                    pregunta.orden=newOrden
                    pregunta.fk_evaluaciones_bloque=bloque
                    pregunta.texto_pregunta=data['textoPregunta']
                    pregunta.puntos_pregunta=data['puntosPregunta']
                    bloque.pointUse=float(bloque.pointUse)+float(pregunta.puntos_pregunta)
                    actividad=ActividadEvaluaciones.objects.get(pk=bloque.fk_actividad_evaluaciones.pk)
                    actividad.pointUse=float(pregunta.puntos_pregunta)+float(actividad.pointUse)
                    bloque.save()
                    actividad.save()
                    pregunta.titulo_pregunta=data['tituloPregunta']
                    pregunta.indicePalabra=data['indiceRespuesta']
                    pregunta.fk_tipo_pregunta_evaluacion=Methods.OrigenPreguntaTipo('Completation')
                    pregunta.save()

                    hijos = data["hijos"]
                    if hijos:
                            print(hijos)
                        
                        
                         
                            for newOpcion in hijos:
                                 Opcion=PreguntasOpciones()
                                 Opcion.fk_evaluacion_pregunta=pregunta
                                 Opcion.texto_opcion=newOpcion['OpcionText']   
                                 Opcion.idLista=newOpcion['id']    

                                 Opcion.respuetaCorrecta=int(newOpcion['isCorrect'])  

                                 Opcion.save()

             
                return JsonResponse({"message": "Perfect"})      
            except:
                return JsonResponse({"message": "Error"})
   
        context = {}
        html_template = (loader.get_template('components/modalAddCompletion.html'))
        return HttpResponse(html_template.render(context, request))
    
@login_required(login_url="/login/")
def getModalNewAssociation(request):
    
     if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                context = {}
                data = json.load(request)["data"]
                print(data)
                if "delete" in data:
                    pregunta=EvaluacionesPreguntas.objects.get(pk=data["id"])
                    bloque = pregunta.fk_evaluaciones_bloque
                    bloque.pointUse=bloque.pointUse-pregunta.puntos_pregunta
                    actividad=bloque.fk_actividad_evaluaciones
                    actividad.pointUse=actividad.pointUse-pregunta.puntos_pregunta
                    bloque.save()

                    actividad.save()

                    pregunta.delete()
                    
                    preguntas = bloque.bloque_pregunta.order_by('orden')
                    for idx, value in enumerate(preguntas, start=1):
                        value.orden = idx
                        value.save()
                    return JsonResponse({"message": "Deleted"})
                
               
                if "idFind" in data:
                    print(data)
                    pregunta=EvaluacionesPreguntas.objects.filter(pk=data["idFind"])
                    findpregunta = list(pregunta.values())
                    childs = PreguntasOpciones.objects.filter(fk_evaluacion_pregunta=data["idFind"])
                    childsA = PreguntasOpciones.objects.filter(fk_evaluacion_pregunta=data["idFind"] ).filter(columnaPregunta=1)
                    childsB = PreguntasOpciones.objects.filter(fk_evaluacion_pregunta=data["idFind"]).filter(columnaPregunta=2)

                    listaChilds = list(childs.values())
                    listaChildsA = list(childsA.values())
                    listaChildsB = list(childsB.values())

                    return JsonResponse({"data":findpregunta[0], "childs":listaChilds, "childsA":listaChildsA, "childsB":listaChildsB}, safe=False)
                
                
                if data["method"] == "Show":
                        context = {}
                        html_template = (loader.get_template('components/modalAddAssociation.html'))
                        return HttpResponse(html_template.render(context, request))
                if data["method"] == "Update":
                    pregunta=EvaluacionesPreguntas.objects.get(pk=data["idViejo"])
                    bloque=EvaluacionesBloques.objects.annotate(num_child=Count('bloque_pregunta', distinct=True) ).get(pk=data['fatherId'])
                  
                    pregunta.orden=pregunta.orden

                    pregunta.fk_evaluaciones_bloque=bloque
                    pregunta.texto_pregunta=data['textoPregunta']
                    pregunta.titulo_pregunta=data['tituloPregunta']
                    actividad=ActividadEvaluaciones.objects.get(pk=bloque.fk_actividad_evaluaciones.pk)
                    actividad.pointUse=float(actividad.pointUse)-float(bloque.pointUse)
                    bloque.pointUse=float(bloque.pointUse)-float(pregunta.puntos_pregunta)+float(data['puntosPregunta'])
                    actividad.pointUse=float(actividad.pointUse)+float(bloque.pointUse)
                    bloque.save()
                    actividad.save()
                    
                    pregunta.puntos_pregunta=data['puntosPregunta']
                    pregunta.fk_tipo_pregunta_evaluacion=Methods.OrigenPreguntaTipo('Association')
                    pregunta.save()
                    childs = PreguntasOpciones.objects.filter(fk_evaluacion_pregunta=data["idViejo"])
                    hijos = data["hijos"]
                    if hijos:
                            print(hijos)
                        
                            if "idViejo" in data:
                                 
                                 childs.delete()
            
                            for newOpcion in hijos:
                                 OpcionA=PreguntasOpciones()
                                 OpcionA.fk_evaluacion_pregunta=pregunta
                                 OpcionA.texto_opcion=newOpcion['OpcionTextA']    
                                 OpcionA.indiceAsociacion=int(newOpcion['id'])  
                                 OpcionA.puntos_porc=float(newOpcion['value'])  
                                    

                                 OpcionA.columnaPregunta=1


                                 OpcionB=PreguntasOpciones()
                                 OpcionB.fk_evaluacion_pregunta=pregunta
                                 OpcionB.texto_opcion=newOpcion['OpcionTextB']    
                                 OpcionB.indiceAsociacion=int(newOpcion['id'])  
                                 OpcionB.puntos_porc=float(newOpcion['value'])  
                                 OpcionB.columnaPregunta=2


                                 OpcionA.save()
                                 OpcionB.save()
                
                if data["method"] == "Create":
                    pregunta=EvaluacionesPreguntas.objects.create()
                    bloque=EvaluacionesBloques.objects.annotate(num_child=Count('bloque_pregunta', distinct=True) ).get(pk=data['fatherId'])
                    newOrden=bloque.num_child+1
                    pregunta.orden=newOrden
                    pregunta.fk_evaluaciones_bloque=bloque
                    pregunta.texto_pregunta=data['textoPregunta']
                    pregunta.puntos_pregunta=data['puntosPregunta']
                    actividad=ActividadEvaluaciones.objects.get(pk=bloque.fk_actividad_evaluaciones.pk)
                    actividad.pointUse=float(actividad.pointUse)-float(bloque.pointUse)
                    bloque.pointUse=float(bloque.pointUse)+float(pregunta.puntos_pregunta)
                    actividad.pointUse=float(pregunta.puntos_pregunta)+float(actividad.pointUse)
                    bloque.save()
                    actividad.save()
                    pregunta.titulo_pregunta=data['tituloPregunta']
                    


                    pregunta.fk_tipo_pregunta_evaluacion=Methods.OrigenPreguntaTipo('Association')
                    pregunta.save()

                    hijos = data["hijos"]
                    if hijos:
                            print(hijos)
                        
                         
                            for newOpcion in hijos:
                                 OpcionA=PreguntasOpciones()
                                 OpcionA.fk_evaluacion_pregunta=pregunta
                                 OpcionA.texto_opcion=newOpcion['OpcionTextA']    
                                 OpcionA.indiceAsociacion=int(newOpcion['id'])  
                                 OpcionA.puntos_porc=float(newOpcion['value'])  
                                    

                                 OpcionA.columnaPregunta=1


                                 OpcionB=PreguntasOpciones()
                                 OpcionB.fk_evaluacion_pregunta=pregunta
                                 OpcionB.texto_opcion=newOpcion['OpcionTextB']    
                                 OpcionB.indiceAsociacion=int(newOpcion['id'])  
                                 OpcionB.puntos_porc=float(newOpcion['value'])  
                                 OpcionB.columnaPregunta=2


                                 OpcionA.save()
                                 OpcionB.save()

             
                return JsonResponse({"message": "Perfect"})      
            except:
                return JsonResponse({"message": "Error"})
   
        context = {}
        html_template = (loader.get_template('components/modalAddAssociation.html'))
        return HttpResponse(html_template.render(context, request))
    
@login_required(login_url="/login/")
def getModalNewTof(request):
    
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                context = {}
                data = json.load(request)["data"]
                if "delete" in data:
                    pregunta=EvaluacionesPreguntas.objects.get(pk=data["id"])
                    bloque = pregunta.fk_evaluaciones_bloque
                    bloque.pointUse=bloque.pointUse-pregunta.puntos_pregunta
                    actividad=bloque.fk_actividad_evaluaciones
                    actividad.pointUse=actividad.pointUse-pregunta.puntos_pregunta
                    bloque.save()

                    actividad.save()

                    pregunta.delete()
                    
                    preguntas = bloque.bloque_pregunta.order_by('orden')
                    for idx, value in enumerate(preguntas, start=1):
                        value.orden = idx
                        value.save()
                    return JsonResponse({"message": "Deleted"})
                
               
                if "idFind" in data:
                    print(data)
                    pregunta=EvaluacionesPreguntas.objects.filter(pk=data["idFind"])
                    findpregunta = list(pregunta.values())
                    childs = PreguntasOpciones.objects.filter(fk_evaluacion_pregunta=data["idFind"])
                    listaChilds = list(childs.values())
                    return JsonResponse({"data":findpregunta[0], "childs":listaChilds}, safe=False)
                
                
                if data["method"] == "Show":
                        context = {}
                        html_template = (loader.get_template('components/modalAddTof.html'))
                        return HttpResponse(html_template.render(context, request))
                if data["method"] == "Update":
                    pregunta=EvaluacionesPreguntas.objects.get(pk=data["idViejo"])
                    bloque=EvaluacionesBloques.objects.annotate(num_child=Count('bloque_pregunta', distinct=True) ).get(pk=data['fatherId'])
                  
                    pregunta.orden=pregunta.orden

                    pregunta.fk_evaluaciones_bloque=bloque
                    pregunta.texto_pregunta=data['textoPregunta']
                    pregunta.titulo_pregunta=data['tituloPregunta']
                    actividad=ActividadEvaluaciones.objects.get(pk=bloque.fk_actividad_evaluaciones.pk)
                    actividad.pointUse=float(actividad.pointUse)-float(bloque.pointUse)
                    bloque.pointUse=float(bloque.pointUse)-float(pregunta.puntos_pregunta)+float(data['puntosPregunta'])
                    actividad.pointUse=float(actividad.pointUse)+float(bloque.pointUse)
                    bloque.save()
                    actividad.save()


                    pregunta.puntos_pregunta=data['puntosPregunta']
                    pregunta.fk_tipo_pregunta_evaluacion=Methods.OrigenPreguntaTipo('True or False')
                    pregunta.save()
                    childs = PreguntasOpciones.objects.filter(fk_evaluacion_pregunta=data["idViejo"])
                    
                    hijos = data["hijos"]
                    if hijos:
                            print(hijos)
                        
                            if "idViejo" in data:
                                 
                                 childs.delete()
            
                            for newOpcion in hijos:
                                
                                 Opcion=PreguntasOpciones()
                                 Opcion.fk_evaluacion_pregunta=pregunta
                                 Opcion.texto_opcion=newOpcion['OpcionText']    
                                 Opcion.puntos_porc=float(newOpcion['value'])  
                                 Opcion.respuetaCorrecta=int(newOpcion['trueFalse'])  
                                 Opcion.idLista=newOpcion['id']    


                                 Opcion.save()
                
                if data["method"] == "Create":
                    pregunta=EvaluacionesPreguntas.objects.create()
                    bloque=EvaluacionesBloques.objects.annotate(num_child=Count('bloque_pregunta', distinct=True) ).get(pk=data['fatherId'])
                    newOrden=bloque.num_child+1
                    pregunta.orden=newOrden
                    pregunta.fk_evaluaciones_bloque=bloque
                    pregunta.texto_pregunta=data['textoPregunta']
                    pregunta.puntos_pregunta=data['puntosPregunta']
                    actividad=ActividadEvaluaciones.objects.get(pk=bloque.fk_actividad_evaluaciones.pk)
                    actividad.pointUse=float(actividad.pointUse)-float(bloque.pointUse)
                    bloque.pointUse=float(bloque.pointUse)+float(pregunta.puntos_pregunta)
                    actividad.pointUse=float(pregunta.puntos_pregunta)+float(actividad.pointUse)
                    bloque.save()
                    actividad.save()
                    pregunta.titulo_pregunta=data['tituloPregunta']

                    pregunta.fk_tipo_pregunta_evaluacion=Methods.OrigenPreguntaTipo('True or False')
                    pregunta.save()

                    hijos = data["hijos"]
                    if hijos:
                         
                            for newOpcion in hijos:
                                 Opcion=PreguntasOpciones()
                                 Opcion.fk_evaluacion_pregunta=pregunta
                                 Opcion.texto_opcion=newOpcion['OpcionText']    
                                 Opcion.puntos_porc=float(newOpcion['value'])  
                                 Opcion.respuetaCorrecta=int(newOpcion['trueFalse'])  
                                 Opcion.idLista=newOpcion['id']    

                                 Opcion.save()

             
                return JsonResponse({"message": "Perfect"})      
            except:
                return JsonResponse({"message": "Error"})
   
    context = {}
    html_template = (loader.get_template('components/modalAddTof.html'))
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def programa(request, programa):
    context = {}
    try:
        program = Estructuraprograma.objects.get(url=programa, valor_elemento="Program")
        rol = request.session.get("user_rol")
        context = {"programa" : program}
        context['segment'] = 'academic'
        #Vista del gestor
        if rol == "Admin" or rol == "Student":
            html_template = (loader.get_template('academic/procesos.html'))
        else:
            return HttpResponseForbidden()
        #Vista del profesor
    except:
        html_template = loader.get_template( 'errors/page-404.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def proceso(request, programa, proceso):
    context = {}
    try:
        program = Estructuraprograma.objects.get(url=programa, valor_elemento="Program")
        process = Estructuraprograma.objects.get(url=proceso, valor_elemento="Process")
        context = {"programa" : program, "proceso":process}
        context['segment'] = 'academic'
        #Vista del gestor
        html_template = (loader.get_template('academic/unidades.html'))
        #Vista del profesor
    except:
        html_template = loader.get_template( 'errors/page-404.html' )
    return HttpResponse(html_template.render(context, request))
@login_required(login_url="/login/")
def unidad(request, programa, proceso, unidad):
    context = {}
    try:
        program = Estructuraprograma.objects.get(url=programa, valor_elemento="Program")
        process = Estructuraprograma.objects.get(url=proceso, valor_elemento="Process")
        unit = Estructuraprograma.objects.get(url=unidad, valor_elemento="Unit")
        context = {"programa" : program, "proceso":process, "unidad":unit}
        context['segment'] = 'academic'
        #Vista del gestor

        html_template = (loader.get_template('academic/cursos.html'))
        #Vista del profesor
    except:
        html_template = loader.get_template( 'errors/page-404.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def curso(request, programa, proceso, unidad, curso):
    context = {}
    user = request.user.extensionusuario
    publico = user.Publico
    rol = user.CtaUsuario.fk_rol_usuario.desc_elemento
    try:
        program = Estructuraprograma.objects.get(url=programa, valor_elemento="Program")
        process = Estructuraprograma.objects.get(url=proceso, valor_elemento="Process")
        unit = Estructuraprograma.objects.get(url=unidad, valor_elemento="Unit")
        course = Estructuraprograma.objects.get(url=curso, valor_elemento="Course")
        sort = False
        if rol == "Admin":
            sort=True
        elif rol == "Teacher":
            today = timezone.now().date()
            activo = ProgramaProfesores.objects.filter(fk_publico=publico, fecha_retiro__gt=today, fk_estructura_programa=course)
            if activo.exists():
                sort=True
        elif rol == "Student":
            sort=False
        else:
            return HttpResponseForbidden()
        context = {"programa" : program, "proceso":process, "unidad":unit, "curso":course}
        context['segment'] = 'academic'
        context['sort'] = sort
        #Vista del gestor
        html_template = (loader.get_template('academic/topicos.html'))
        #Vista del profesor
    except:
        html_template = loader.get_template( 'errors/page-404.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def actividad(request, programa, proceso, unidad, curso, topico, idActividad):
    context = {}
    try:
        program = Estructuraprograma.objects.get(url=programa, valor_elemento="Program")
        process = Estructuraprograma.objects.get(url=proceso, valor_elemento="Process")
        unit = Estructuraprograma.objects.get(url=unidad, valor_elemento="Unit")
        course = Estructuraprograma.objects.get(url=curso, valor_elemento="Course")
        topic = Estructuraprograma.objects.get(url=topico, valor_elemento="Topic")
        actividad = Estructuraprograma.objects.get(pk=idActividad, valor_elemento="Activity")
        context = {"programa" : program, "proceso":process, "unidad":unit, "curso":course, "topico":topic, "actividad":actividad}
        context['segment'] = 'academic'
        #Vista del gestor
        html_template = (loader.get_template('academic/actividad.html'))
        #Vista del profesor
    except:
        html_template = loader.get_template( 'errors/page-404.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def logUser(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            user = request.user.extensionusuario
            publico = user.Publico
            rol = user.CtaUsuario.fk_rol_usuario.desc_elemento
            try:
                if request.body:
                    data=json.load(request)
                    if rol == 'Student':
                        idEstructura = data["pk"]
                        fecha = timezone.now()
                        estado = data["estado"]
                        update = HistoricoUser.objects.filter(fk_publico=publico, fk_estructura_programa=idEstructura)
                        if update.exists():
                            historia = update.order_by("-fecha")[0]
                        else:
                            historia = HistoricoUser()
                        historia.fecha = fecha
                        historia.estado = estado
                        historia.fk_estructura_programa_id = idEstructura
                        historia.fk_publico = publico
                        historia.save()     
            except:
                return JsonResponse({"message":"error"}, status=500)

def logUserBackEnd(usuario, activity, estado, esUpdate):
            
            
            user = ExtensionUsuario.objects.get(user=usuario).Publico
            log=HistoricoUser.objects.filter(fk_publico=user, fk_estructura_programa=activity)
            
            if log.exists():
                if esUpdate ==True:
                    new=HistoricoUser.objects.get(pk=log[0].pk)
                    new.fecha = datetime.datetime.now()
                    new.estado = estado
                    new.save()
                else:
                        log.delete()
                        historia = HistoricoUser()
                        historia.fecha = datetime.datetime.now()
                        historia.estado = estado
                        historia.fk_estructura_programa_id = activity
                        historia.fk_publico = user
                        historia.save()    
            else:
                        historia = HistoricoUser()
                        historia.fecha = datetime.datetime.now()
                        historia.estado = estado
                        historia.fk_estructura_programa_id = activity
                        historia.fk_publico = user
                        historia.save()     

            

@login_required(login_url="/login/")
def getComboContent(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            try:
                if request.body:
                    data=json.load(request)
                    if data["id"] == "null" or data["id"] == None:
                        hijos=None
                    else:
                        padre = Estructuraprograma.objects.get(pk=data["id"])
                        hijos = padre.estructuraprograma_set.all()
                    context = {"subEstructuraProg":hijos, "valor":data["valor"]}
                    html_template = (loader.get_template('registration/ComboOptions.html'))
                    return HttpResponse(html_template.render(context, request))
            except:
                return JsonResponse({"message":"error"}, status=500)
    
@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))
