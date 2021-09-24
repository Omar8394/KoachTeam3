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
import json, math
from .models import TablasConfiguracion
from ..academic.models import EscalaCalificacion






@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

def componentLista(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        context = {}
        data = json.load(request)["data"]
        if data["name"] == "listaConfig":
            hijos = TablasConfiguracion.objects.filter(fk_tabla_padre=1, mostrar_en_combos=1)
            if not hijos:
                return JsonResponse({"message":"there are no childs"})
            page = int(data["page"])
            limit = int(data["limit"])
            total = len(hijos)
            lastPage = math.ceil(total/limit)
            if page > lastPage:
                return JsonResponse({"message":"some kind of error"})
            lista=[]
            last = page * limit
            begin = last - limit
            for i in list(hijos.values()):
                i['pk'] = i['id_tabla']
                i['descripcion'] = i['desc_elemento']
                lista.append(i)
            context = {
                "list":lista[begin:last],
                "limit":limit,
                "lastPage":lastPage,
                "begin": begin,
                "last": last,
                "page": page,
                "before": page - 1 ,
                "after": page + 1,
            }
        return render(request, 'components/lista.html', context)
    return

def componentTabla(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        context = {}
        data = json.load(request)["data"]
        #Aqui cada quien puede poner su script para su tabla
        #aqui comienza la de tabla configuraciones
        if data["name"] == "tablaConfig":
            padre = data["padre"]
            hijos = TablasConfiguracion.objects.filter(fk_tabla_padre=padre, mostrar_en_combos=1)
            if not hijos:
                return JsonResponse({"message":"there are no childs"})
            lista = []
            #en este bucle les paso la pk de cada elemento 
            #con el fin de llamar a los metodos luego en JS
            for i in list(hijos.values()):
                i['pk'] = i['id_tabla']
                if i["maneja_lista"] == 1:
                    i["manejaLista"] = True
                    i["crearHijos"] = True
                if i["permite_cambios"] == 1:
                    i["editar"] = True
                    i["eliminable"] = True
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
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            context = {}
            data = json.load(request)["data"]
            if "idFind" in data:
                newConfig = TablasConfiguracion.objects.filter(pk=data["idFind"])
                findConfig = list(newConfig.values())
                return JsonResponse({"data":findConfig[0]}, safe=False)
            elif "idViejo" in data:
                newConfig = TablasConfiguracion.objects.get(pk=data["idViejo"])
            else:
                newConfig = TablasConfiguracion()
            newConfig.desc_elemento=data["descripcion"] 
            newConfig.tipo_elemento=data["tipoElemento"] 
            newConfig.permite_cambios=data["permiteCambios"] 
            newConfig.valor_elemento=data["valorElemento"] 
            newConfig.mostrar_en_combos=data["mostrarEnCombos"] 
            newConfig.maneja_lista=data["manejaLista"] 
            newConfig.fk_tabla_padre_id=data["idPadre"]
            newConfig.save()
            return JsonResponse({"message": "perfect"})
        except:
            return JsonResponse({"message": "something went wrong"})
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
