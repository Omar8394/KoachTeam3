from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.db.models import query
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django import template
import json
from ..app.models import TablasConfiguracion, Estructuraprograma
from .models import ActividadEvaluaciones, Cursos, ActividadConferencia, ActividadLeccion, ActividadTarea, EscalaEvaluacion, EvaluacionesPreguntas

# Create your views here.
@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'academic'
    #Vista del gestor
    html_template = (loader.get_template('academic/gestor.html'))
    #Vista del profesor
    #html_template = (loader.get_template('academic/index.html'))
    return HttpResponse(html_template.render(context, request))


#PRUEBA
@login_required(login_url="/login/")
def prueba(request):
    context = {}
    # html_template = (loader.get_template('academic/topicos.html'))
    # return HttpResponse(html_template.render(context, request))
    pass

@login_required(login_url="/login/")
def evaluaciones(request):
    context = {}
    context['segment'] = 'academic'
    html_template = (loader.get_template('academic/evaluaciones.html'))
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def test(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                context = {}
                data = json.load(request)["data"]
                if "delete" in data:
                    test = ActividadEvaluaciones.objects.get(pk=data["id"])
                    test.delete()
                    return JsonResponse({"message": "Deleted"})
                elif "idFind" in data:
                    test = ActividadEvaluaciones.objects.filter(pk=data["idFind"])
                    findTest = list(test.values())
                    return JsonResponse({"data":findTest[0]}, safe=False)
                elif "idViejo" in data:
                    test = ActividadEvaluaciones.objects.get(pk=data["idViejo"])
                else:
                    test = ActividadEvaluaciones()
                    test.titulo.data = data[""]
                    test.fk_curso_actividad.data = data[""]
                    test.nro_repeticiones.data = data[""]
                    test.duracion.data = data[""]
                    test.fk_tipo_duracion.data = data[""]
                    test.fk_escala_calificacion.data = data[""]
                    test.calificacion_aprobar .data = data[""]
                    test.save()
                return JsonResponse({"message": "Perfect"})      
            except:
                return JsonResponse({"message": "Error"})
                
    context = {}
    html_template = (loader.get_template('academic/evaluaciones.html'))
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def createQuestions(request):
    context = {
        "tipoPreguntas" : TablasConfiguracion.obtenerHijos('PregEvalua'),     
    }
    context['segment'] = 'academic'
    return render(request, 'academic/createQuestions.html', context)


@login_required(login_url="/login/")
def saveQuestions(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                context = {}
                data = json.load(request)["data"]
                if "delete" in data:
                    question = EvaluacionesPreguntas.objects.get(pk=data["id"])
                    question.delete()
                    return JsonResponse({"message": "Deleted"})
                elif "idFind" in data:
                    question = EvaluacionesPreguntas.objects.filter(pk=data["idFind"])
                    findQuestion = list(question.values())
                    return JsonResponse({"data":findQuestion[0]}, safe=False)
                elif "idViejo" in data:
                    question = EvaluacionesPreguntas.objects.get(pk=data["idViejo"])
                else:
                    question = EvaluacionesPreguntas()
                question.texto_pregunta.data = data["textoPregunta"]
                question.puntos_pregunta.data = data["puntosPregunta"]
                question.fk_actividad_evaluaciones.data = data["fk_actividad_evaluaciones"]
                question. fk_tipo_pregunta_evaluacion.data = data["tipoPregunta"]
                question.save()
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
            if request.body:
                data = json.load(request)    
                lista = {}
                edit=True
                delete=True
                categorias = TablasConfiguracion.obtenerHijos("CatPrograma")
                if data["query"] == "" or data["query"] == None:
                    for categoria in categorias:
                        lista[categoria.desc_elemento]=categoria.estructuraprograma_set.all().filter(valor_elemento="Program")
                else:
                    for categoria in categorias:
                        lista[categoria.desc_elemento]=categoria.estructuraprograma_set.all().filter(valor_elemento="Program", descripcion__icontains=data["query"])
                context = {"data" : lista, "edit": edit, "delete":delete, "query":data["query"]}
                html_template = (loader.get_template('academic/contenidoProgramas.html'))
                return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def getContentProcesos(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            if request.body:
                data = json.load(request)    
                edit=True
                delete=True
                programa=Estructuraprograma.objects.get(valor_elemento="Program", url=data["url"])
                if data["query"] == "" or data["query"] == None:
                    lista = programa.estructuraprograma_set.all()
                else:
                    lista = programa.estructuraprograma_set.all().filter(valor_elemento="Process", descripcion__icontains=data["query"])
                context = {"data":lista, "programa":programa, "edit": edit, "delete":delete, "query":data["query"]}
                html_template = (loader.get_template('academic/contenidoProcesos.html'))
                return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def getContentUnidades(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            if request.body:
                data = json.load(request)    
                edit=True
                delete=True
                programa=Estructuraprograma.objects.get(valor_elemento="Program", url=data["url"])
                proceso=Estructuraprograma.objects.get(valor_elemento="Process", url=data["urlProceso"])
                if data["query"] == "" or data["query"] == None:
                    lista = proceso.estructuraprograma_set.all()
                else:
                    lista = proceso.estructuraprograma_set.all().filter(valor_elemento="Unit", descripcion__icontains=data["query"])
                context = {"data":lista, "programa":programa, "proceso":proceso ,"edit": edit, "delete":delete, "query":data["query"]}
                html_template = (loader.get_template('academic/contenidoUnidades.html'))
                return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def getContentCursos(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            if request.body:
                data = json.load(request)    
                edit=True
                delete=True
                programa=Estructuraprograma.objects.get(valor_elemento="Program", url=data["url"])
                proceso=Estructuraprograma.objects.get(valor_elemento="Process", url=data["urlProceso"])
                unidad=Estructuraprograma.objects.get(valor_elemento="Unit", url=data["urlUnidad"])
                if data["query"] == "" or data["query"] == None:
                    lista = unidad.estructuraprograma_set.all()
                else:
                    lista = unidad.estructuraprograma_set.all().filter(valor_elemento="Course", descripcion__icontains=data["query"])
                context = {"data":lista, "programa":programa, "proceso":proceso, "unidad":unidad ,"edit": edit, "delete":delete, "query":data["query"]}
                html_template = (loader.get_template('academic/contenidoCursos.html'))
                return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def getContentTopicos(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            if request.body:
                data = json.load(request)    
                take=True
                see=True
                edit=True
                add=True
                delete=True
                programa=Estructuraprograma.objects.get(valor_elemento="Program", url=data["url"])
                proceso=Estructuraprograma.objects.get(valor_elemento="Process", url=data["urlProceso"])
                unidad=Estructuraprograma.objects.get(valor_elemento="Unit", url=data["urlUnidad"])
                curso=Estructuraprograma.objects.get(valor_elemento="Course", url=data["urlCurso"])
                if data["query"] == "" or data["query"] == None:
                    lista = curso.estructuraprograma_set.all()
                else:
                    lista = curso.estructuraprograma_set.all().filter(valor_elemento="Topic", descripcion__icontains=data["query"])
                context = {"data":lista, "programa":programa, "proceso":proceso, "unidad":unidad, "curso":curso ,"add":add,"edit": edit,"take": take,"see": see, "delete":delete, "query":data["query"]}
                html_template = (loader.get_template('academic/contenidoTopicos.html'))
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
                    return JsonResponse({"message":"Perfect"})
                # else:
                
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
                    elif data["method"] == "Delete":
                        actividad = Estructuraprograma.objects.get(pk=data["id"])
                        actividad.delete()
                        return JsonResponse({"message":"Deleted"})
                    elif data["method"] == "Update":
                        actividad = Estructuraprograma.objects.get(pk=data["id"])
                    elif data["method"] == "Create":
                        actividad = Estructuraprograma()
                        actividad.valor_elemento = "Activity"
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
                        actividad.fk_estructura_padre_id=data["padreActivity"]
                    actividad.descripcion = data["data"]["descriptionActivity"]
                    actividad.resumen = data["data"]["resumenActivity"]
                    actividad.url = data["data"]["urlActivity"]
                    actividad.peso_creditos = None
                    actividad.fk_categoria_id = TablasConfiguracion.obtenerHijos(valor="Tipo Actividad").get(desc_elemento="Test").pk
                    if "checkExpertCB" in data["data"]:
                        actividad.fk_categoria_id = TablasConfiguracion.obtenerHijos(valor="Tipo Actividad").get(desc_elemento="Expert test").pk
                    if "durationActivity" in data["data"]:
                        test.duracion = data["data"]["durationActivity"]
                    else:
                        test.duracion = None
                    if "timeActivity" in data["data"]:
                        test.fk_tipo_duracion_id = data["data"]["timeActivity"]
                    else:
                        test.fk_tipo_duracion_id = None
                    test.nro_repeticiones = data["data"]["repeats"]
                    test.calificacion_aprobar = data["data"]["minApp"]
                    test.fk_escala_evaluacion_id = data["data"]["qualification"]
                    actividad.save()
                    test.fk_estructura_programa = actividad
                    test.save()
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
                    actividad.descripcion = data["data"]["descriptionActivity"]
                    actividad.resumen = data["data"]["resumenActivity"]
                    actividad.url = data["data"]["urlActivity"]
                    actividad.peso_creditos = None
                    actividad.fk_categoria_id = TablasConfiguracion.obtenerHijos(valor="Tipo Actividad").get(desc_elemento="Lesson").pk
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
                        context = {"modelo": modelo}
                        html_template = (loader.get_template('components/modalAddHomework.html'))
                        return HttpResponse(html_template.render(context, request))
                    elif data["method"] == "Delete":
                        actividad = Estructuraprograma.objects.get(pk=data["id"])
                        actividad.delete()
                        return JsonResponse({"message":"Deleted"})
                    elif data["method"] == "Update":
                        actividad = Estructuraprograma.objects.get(pk=data["id"])
                        homework = ActividadTarea.objects.get(fk_estructura_programa=data["id"])
                    elif data["method"] == "Create":
                        actividad = Estructuraprograma()
                        homework = ActividadTarea()
                        actividad.valor_elemento = "Activity"
                        actividad.fk_categoria_id = TablasConfiguracion.obtenerHijos(valor="Tipo Actividad").get(desc_elemento="Homework").pk
                        actividad.fk_estructura_padre_id=data["padreActivity"]
                    actividad.descripcion = data["data"]["descriptionActivity"]
                    actividad.resumen = data["data"]["resumenActivity"]
                    actividad.url = data["data"]["urlActivity"]
                    actividad.peso_creditos = None
                    actividad.save()
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
            # try:
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
                    actividad.fk_categoria_id = TablasConfiguracion.obtenerHijos(valor="Tipo Actividad").get(desc_elemento="Forum").pk
                    actividad.fk_estructura_padre_id=data["padreActivity"]
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
            # except:
            #     return JsonResponse({"message":"error"}, status=500)

@login_required(login_url="/login/")
def getModalQuestion(request): 
    context = {
        "tipoPreguntas" : TablasConfiguracion.obtenerHijos('PregEvalua'),
    }
    html_template = (loader.get_template('components/modalAddQuestion.html'))
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def getModalNewSimple(request):
   
    context = {}
    html_template = (loader.get_template('components/modalAddSimple.html'))
    return HttpResponse(html_template.render(context, request))
    
@login_required(login_url="/login/")
def getModalNewMultiple(request):
   
    context ={}
    html_template = (loader.get_template('components/modalAddMultiple.html'))
    return HttpResponse(html_template.render(context, request))
    
@login_required(login_url="/login/")
def getModalNewCompletion(request):
   
    context = {}
    html_template = (loader.get_template('components/modalAddCompletion.html'))
    return HttpResponse(html_template.render(context, request))
    
@login_required(login_url="/login/")
def getModalNewAssociation(request):
   
    context = {}
    html_template = (loader.get_template('components/modalAddAssociation.html'))
    return HttpResponse(html_template.render(context, request))
    
@login_required(login_url="/login/")
def getModalNewTof(request):
   
    context = {}
    html_template = (loader.get_template('components/modalAddTof.html'))
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def programa(request, programa):
    program = Estructuraprograma.objects.get(url=programa)
    context = {"programa" : program}
    context['segment'] = 'academic'
    #Vista del gestor
    html_template = (loader.get_template('academic/procesos.html'))
    #Vista del profesor
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def proceso(request, programa, proceso):
    program = Estructuraprograma.objects.get(url=programa)
    process = Estructuraprograma.objects.get(url=proceso)
    context = {"programa" : program, "proceso":process}
    #Vista del gestor

    html_template = (loader.get_template('academic/unidades.html'))
    #Vista del profesor
    return HttpResponse(html_template.render(context, request))
@login_required(login_url="/login/")
def unidad(request, programa, proceso, unidad):
    program = Estructuraprograma.objects.get(url=programa)
    process = Estructuraprograma.objects.get(url=proceso)
    unit = Estructuraprograma.objects.get(url=unidad)
    context = {"programa" : program, "proceso":process, "unidad":unit}
    #Vista del gestor

    html_template = (loader.get_template('academic/cursos.html'))
    #Vista del profesor
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def curso(request, programa, proceso, unidad, curso):
    program = Estructuraprograma.objects.get(url=programa)
    process = Estructuraprograma.objects.get(url=proceso)
    unit = Estructuraprograma.objects.get(url=unidad)
    course = Estructuraprograma.objects.get(url=curso)
    context = {"programa" : program, "proceso":process, "unidad":unit, "curso":course}
    #Vista del gestor
    html_template = (loader.get_template('academic/topicos.html'))
    #Vista del profesor
    return HttpResponse(html_template.render(context, request))
@login_required(login_url="/login/")
def topico(request):
    return
@login_required(login_url="/login/")
def actividad(request):
    return

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
