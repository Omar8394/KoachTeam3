from django.conf.urls import url
from django.contrib.auth import models
from django.db import connection
from django.db.models import query

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import loader
from django.urls import reverse
from django import template


from ..academic.models import ProgramaProfesores
import json
from django.db.models import F

from ..app.models import Aplicaciones, TablasConfiguracion, Estructuraprograma, Publico,  PublicoRelacion

# Create your views here.

@login_required(login_url="/login/")
def professors(request):
    context = {}
    context['segment'] = 'academic'

    return render(request,'professors/inicioProfessors.html', context)

# mi prueba query sql
@login_required(login_url="/login/")
def getContentProf(request):
    
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if request.body:
                context={}
                data = json.load(request)
                edit=True
                delete=True
                lista=""
                sql="SELECT tab_conf.desc_elemento, app_p.* FROM app_tablasconfiguracion AS tab_conf JOIN app_publicorelacion AS app_pr ON tab_conf.id_tabla=app_pr.fk_relacion_id JOIN app_publico AS app_p ON app_pr.fk_publico_id=app_p.idpublico"
                item=data["id_Course"]
            
                if data["query"] == "" or data["query"] == None:
                    
                    if item:
                        lista=Publico.objects.raw(sql+" "+"WHERE tab_conf.valor_elemento='prof' AND app_p.idpublico NOT IN (SELECT fk_publico_id FROM academic_programaprofesores AS acd_pro WHERE fk_estructura_programa_id=%s)", [item])
                    else:
                        lista={}
                else:   
                    if item:
                        item1=data["query"]
                        lista=Publico.objects.raw(sql+" "+"WHERE tab_conf.valor_elemento='prof' AND app_p.idpublico NOT IN (SELECT fk_publico_id FROM academic_programaprofesores AS acd_pro WHERE fk_estructura_programa_id=%s) AND app_p.nombre LIKE '%s%%%%'" %(item, item1))
                        print(lista)
                    else:
                        lista={}
                    
                context = {"pro":lista, "edit": edit, "delete":delete, "query":data["query"]}
                html_template = (loader.get_template('professors/contentProfessors.html'))
    
    
                return HttpResponse(html_template.render(context, request))



@login_required(login_url="/login/")
def getcontetCourso(request):
    if request.method == "POST":
       if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if request.body:
                context={}
                data = json.load(request)

                edit=True
                delete=True
                sql="SELECT app_es.*, app_p.*, acad_prop.* FROM app_estructuraprograma app_es JOIN academic_programaprofesores acad_prop ON app_es.idestructuraprogrmas=acad_prop.fk_estructura_programa_id JOIN app_publico app_p ON acad_prop.fk_publico_id=app_p.idpublico"
             
            
                if data["query"] == "" or data["query"] == None:
                    items=" "
                    lista=Estructuraprograma.objects.raw(sql+" "+"WHERE app_es.descripcion=%s", [items])
                    
                else: 
                    item=data["query"]
                
                    lista=Estructuraprograma.objects.raw(sql+" "+("WHERE app_es.descripcion like '%s%%%%'" %item))
            
                context = { "data":lista,"pro":lista, "edit": edit, "delete":delete, "query":data["query"]}
          
                html_template = (loader.get_template('professors/contentCourse.html'))
    
    
                return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def selectProfessors(request, id):
                
    context = {"pro":" ", "id_corso":id}
    context['segment'] = 'academic'
    

    html_template = (loader.get_template('professors/selectProfessor.html'))
    return HttpResponse(html_template.render(context, request))
    
    #if request.method == "POST":
        #if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    
        
            
            #context['segment'] = 'academic'

            #sql="SELECT app_es.*, app_p.* FROM app_estructuraprograma app_es JOIN academic_programaprofesores acad_prop ON app_es.idestructuraprogrmas=acad_prop.fk_estructura_programa_id JOIN app_publico app_p ON acad_prop.fk_publico_id=app_p.idpublico"
    
            #lista=Publico.objects.raw(sql+" "+("WHERE tab_conf.valor_elemento='prof' AND app_p.idpublico NOT IN (SELECT fk_publico_id FROM academic_programaprofesores AS acd_pro WHERE fk_estructura_programa_id=%s)" %item))
             
            



@login_required(login_url="/login/")
def getmodalProf(request):

    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            
            
            
            sql="SELECT * FROM app_estructuraprograma WHERE valor_elemento='program'"
             

            result=Estructuraprograma.objects.raw(sql)
            

            context = {"categorias":result}
          
            html_template = (loader.get_template('professors/selectCourso.html'))
    
    
            return HttpResponse(html_template.render(context, request))



@login_required(login_url="/login/")
def getmodalProf2(request):
    context={}
    if request.method == "POST":

        list1 = request.POST.getlist('categoryProgram')      
  
    return redirect('/professors/professors/')
  
        
@login_required(login_url="/login/")
def saveProfessors(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            modelo = {}
            context = {}
            try:
                if request.body:
                    data = json.load(request)
                    print(data)
                    
                    if data["method"] == "delete":
                        programa = ProgramaProfesores.objects.get(pk=data["id_delete"])
                        print(programa)
                        programa.delete()
                        return JsonResponse({"message":"Deleted"})
                        
                    elif data["method"] == "save":

                        programa=ProgramaProfesores()
                        
                        programa.comentarios=data["data"]["resumenprofessors"]
                        programa.fk_publico_id=data["data"]["idpublic"]
                        programa.fk_estructura_programa_id=data["data"]["idcourso"]
                        programa.fk_situacion_id=data["data"]["situacion"]
                        programa.fecha_autorizado=data["data"]["fechaAutorizado"]
                        programa.fecha_retiro=data["data"]["fechaRetiro"]
                        
                        programa.save()
                            
                        return JsonResponse({"message":"Perfect"})

                    elif data["codigo"] == "true":
                         
                        cod=data["id"]
                        data_p=Publico.objects.raw("SELECT * FROM app_publico WHERE idpublico= %s" %cod)
                        cod1=data["id_Course"]
                        data_courso=Estructuraprograma.objects.raw("SELECT * FROM app_estructuraprograma WHERE idestructuraprogrmas= %s" %cod1)
                        print(data_p)
                        print(data_courso)     
                        context = {"publico":data_p, "courso":data_courso}
                        html_template = (loader.get_template('professors/saveProfessors.html')) 
        
                        return HttpResponse(html_template.render(context, request))
                else:

                    context={}
                    html_template = (loader.get_template('professors/saveProfessors.html')) 
        
                    return HttpResponse(html_template.render(context, request))
            except:
        
                return JsonResponse({"message":"error"}, status=500)

    

@login_required(login_url="/login/")
def combobox101(request):

    valor=request.GET.get('valor')

    data={'opcion1': metodo_llenar_combo_process(valor)}

    html_template = (loader.get_template('professors/combobox.html'))
    
    
    return HttpResponse(html_template.render(data, request))




def metodo_llenar_combo_process(valor):
    valor1=valor
    sql1=("SELECT idestructuraprogrmas, descripcion FROM app_estructuraprograma WHERE fk_estructura_padre_id IN (SELECT idestructuraprogrmas FROM app_estructuraprograma WHERE idestructuraprogrmas=%s)")
    result1=Estructuraprograma.objects.raw(sql1,[valor1])

    list=[]

    for file in result1:
        
        list.append(file)
        
    return list





            
            
                
            
        
        
     
    
        
        
   
                


