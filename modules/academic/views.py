from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django import template

# Create your views here.
@login_required(login_url="/login/")
def index(request):
    
    context = {}

    html_template = (loader.get_template('academic/index.html'))
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
