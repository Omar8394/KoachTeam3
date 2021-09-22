# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.forms.utils import pretty_name
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django import template
import json
from .models import TablasConfiguracion
from ..academic.models import EscalaCalificacion






@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

def componentTabla(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        context = {}
        data = json.load(request)["data"]
        #Aqui cada quien puede poner su script para su tabla
        #aqui comienza la de tabla configuraciones
        if data["name"] == "tablaConfig":
            padre = data["padre"]
            hijos = TablasConfiguracion.objects.filter(fk_tabla_padre=padre)
            if not hijos:
                return JsonResponse({"message":"there are no childs"})
            lista = []
            #en este bucle les paso la pk de cada elemento 
            #con el fin de llamar a los metodos luego en JS
            for i in list(hijos.values()):
                i['pk'] = i['id_tabla']
                lista.append(i)
            context = {
                #aqui el nombre de la columna a mostrar
                "fields": ["Description", "Actions"],
                #aqui ponemos el nombre de la columna de la BBDD
                "keys": ["desc_elemento"],
                "data": lista,
            }
        #if data["name"] == "El nombre de tu tabla"
        return render(request,'components/tabla.html', context)
    return

@login_required(login_url="/login/")
def tables(request):
    context = {"tables": TablasConfiguracion.objects.all()}
    html_template = (loader.get_template('app/settings/tables.html'))
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def scales(request):
    context = {"escalas": EscalaCalificacion.objects.all()}
    html_template = (loader.get_template('app/settings/scales.html'))
    return HttpResponse(html_template.render(context, request))

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
