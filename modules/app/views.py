# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from .models import TablasConfiguracion
from ..academic.models import EscalaCalificacion






@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

def componentTabla(request, fields, data):
    context = {
        "fields": fields,
        "data": data
    }
    html_template = loader.get_template('components/tabla.html')
    return HttpResponse(html_template.render(context, request))

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
