from django.contrib.auth.decorators import login_required
from django.forms.utils import pretty_name
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django import template
import json, math
from django.core.paginator import Paginator
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
            if data["query"] != "" and data["query"] != None:
                hijos = hijos.filter(desc_elemento__icontains=data["query"])
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
                "query": data["query"]
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
                return JsonResponse({"message":"There are no childs"})
            lista = []
            limit = None
            page = None
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
            if data["page"] != None and data["page"] != "":
                paginator = Paginator(lista, data["limit"])
                lista = paginator.get_page(data["page"])
                page = data["page"]
                limit = data["limit"]
            context = {
                #aqui el nombre de la columna a mostrar
                "fields": ["Description", "Actions"],
                #aqui ponemos el nombre de la columna de la BBDD
                "keys": ["desc_elemento"],
                "data": lista,
                "page": page,
                "limit": limit,
            }
        #if data["name"] == "El nombre de tu tabla"
        return render(request,'components/tabla.html', context)
    return

@login_required(login_url="/login/")
def tables(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                context = {}
                data = json.load(request)["data"]
                if "delete" in data:
                    newConfig = TablasConfiguracion.objects.get(pk=data["id"])
                    newConfig.delete()
                    return JsonResponse({"message": "Deleted"})
                elif "idFind" in data:
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
                return JsonResponse({"message": "Perfect"})
            except:
                return JsonResponse({"message": "Error"})
    context = {}
    html_template = (loader.get_template('app/settings/tables.html'))
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def getModalSetting(request):
    context = {"tables": TablasConfiguracion.objects.all()}
    html_template = (loader.get_template('components/modalAddSetting.html'))
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def scales(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                context = {}
                data = json.load(request)["data"]
                if "delete" in data:
                    newScaleGe = EscalaEvaluacion.objects.get(pk=data["id"])
                    newScaleGe.delete()
                    return JsonResponse({"message": "Deleted"})
                elif "idFind" in data:
                    newScaleGe = EscalaEvaluacion.objects.filter(pk=data["idFind"])
                    findScaleGe = list(newScaleGe.values())
                    return JsonResponse({"data":findScaleGe[0]}, safe=False)
                elif "idViejo" in data:
                    newScaleGe = EscalaEvaluacion.objects.get(pk=data["idViejo"])
                else:
                    newScaleGe = EscalaEvaluacion()
                    newScaleGe.desc_escala=data["descripcion"] 
                    newScaleGe.maxima_puntuacion=data["maxScore"] 
                    newScaleGe.save()
                    return JsonResponse({"message": "Perfect"})
                  
            except:
                return JsonResponse({"message": "Error"})
                
    context = {}
    html_template = (loader.get_template('app/settings/scales.html'))
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def scalesPa(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                context = {}
                data = json.load(request)["data"]
                if "delete" in data:
                    newScalePa = EscalaCalificacion.objects.get(pk=data["id"])
                    newScalePa.delete()
                    return JsonResponse({"message": "Deleted"})
                elif "idFind" in data:
                    newScalePa = EscalaCalificacion.objects.filter(pk=data["idFind"])
                    findScalePa = list(newScalePa.values())
                    return JsonResponse({"data":findScalePa[0]}, safe=False)
                elif "idViejo" in data:
                    newScalePa = EscalaCalificacion.objects.get(pk=data["idViejo"])
                else:
                    newScalePa = EscalaCalificacion()
                    newScalePa.desc_calificacion=data["descCalificacion"] 
                    newScalePa.puntos_maximo=data["maxPoints"] 
                    newScalePa.fk_calificacion=data["fkCalificacion"] 
                    newScalePa.save()
                    return JsonResponse({"message": "Perfect"})
                  
            except:
                return JsonResponse({"message": "Error"})
                
    context = {}
    html_template = (loader.get_template('app/settings/scales.html'))
    return HttpResponse(html_template.render(context, request))
    # return render(request, 'app/settings/scales.html', context)

@login_required(login_url="/login/")
def scalesGeAddModal(request): 

    return render(request, 'components/modalAddScaleGe.html')

@login_required(login_url="/login/")
def scalesPaAddModal(request):

    return render(request, 'components/modalAddScalePa.html')



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
