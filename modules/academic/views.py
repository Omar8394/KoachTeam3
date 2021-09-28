from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django import template
import json
from ..app.models import TablasConfiguracion

# Create your views here.
@login_required(login_url="/login/")
def index(request):
    
    context = {}
    #Vista del gestor
    html_template = (loader.get_template('academic/gestor.html'))
    #Vista del profesor
    #html_template = (loader.get_template('academic/index.html'))
    return HttpResponse(html_template.render(context, request))


#PRUEBA
@login_required(login_url="/login/")
def cursos(request):
    context = {}
    html_template = (loader.get_template('academic/cursos.html'))
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def evaluaciones(request):
    context = {}
    html_template = (loader.get_template('academic/evaluaciones.html'))
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
                return JsonResponse({"message":"error"})

@login_required(login_url="/login/")
def getModalProgramas(request):
    context = {}
    html_template = (loader.get_template('components/modalAddPrograma.html'))
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def getModalProcesos(request):
    context = {}
    html_template = (loader.get_template('components/modalAddProceso.html'))
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def getModalCursos(request):
    context = {}
    html_template = (loader.get_template('components/modalAddCurso.html'))
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def getModalTopico(request):
    context = {}
    html_template = (loader.get_template('components/modalAddTopico.html'))
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def programa(request):
    return
@login_required(login_url="/login/")
def proceso(request):
    return
@login_required(login_url="/login/")
def unidad(request):
    return
@login_required(login_url="/login/")
def topico(request):
    return
@login_required(login_url="/login/")
def actividad(request):
    return

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
