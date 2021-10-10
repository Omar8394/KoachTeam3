from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django import template
from django.template import loader
from modules.registration import forms
from modules.app.models import Estructuraprograma
from modules.security.models import ExtensionUsuario

from modules.app.models import TablasConfiguracion
from modules.app.models import Publico
from modules.registration.models import MatriculaAlumnos, MatriculasPagos
from django.http import JsonResponse
import datetime
from modules.app import Methods
from django.core.paginator import Paginator
from django.utils.dateparse import parse_datetime
from modules.registration.models import PreciosFormacion
from django.db.models import Q
from django.db.models import F
from django.db.models import Count
from django.db.models import Max
import random
import uuid
import os
from pathlib import Path

from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from core import settings

from time import gmtime, strftime
import hashlib
# Create your views here.



@login_required(login_url="/login/")
def enrollment(request):
  

    form = forms.MatriculaForm(request.POST or None)


    msg = None
   # structuraProg=Estructuraprograma.objects.filter(fk_estructura_padre=None)
    structuras=Estructuraprograma.objects.all()

    structuras=structuras.annotate(precio=F('prize__precio'), fechaIngreso=F('prize__fecha_registro'), id=F('prize__idprograma_precios'), descuento=F('prize__PorcentajeDescuento'), max=Max('prize__idprograma_precios'), amountDiscount=Max('prize__idprograma_precios')  ).filter(id=Max('prize__idprograma_precios')  )
    structuras=structuras.filter(fk_estructura_padre=None)
    
  

    tipoPrograma=TablasConfiguracion.obtenerHijos("Tipo matricula")


            

    html_template = loader.get_template( 'registration/Matriculacion.html' )

    #return HttpResponse(html_template.render(context, request))
    return render(request, 'registration/Matriculacion.html', {"form": form, "msg" : msg,'structuraProg':structuras, 'tipoPrograma':tipoPrograma, 'segment':'registration'})

@login_required(login_url="/login/")
def ManageEnrollments(request):
   msg = None
   matriculaList=MatriculaAlumnos.objects.all()


   if request.method == "POST":
        
      
        idPersona=request.POST.get('idPersona') 
        
        matriculaList=matriculaList.filter(fk_publico=idPersona)

        fechaInicial=request.POST.get('fechaInicial') 

        
        fechaFinal=request.POST.get('fechaFinal') 
        print(fechaFinal)
        print(fechaFinal)
        if fechaInicial!=None and fechaInicial!="":
          dateI=parse_datetime(fechaFinal+' 00:00:00-00')

          matriculaList=matriculaList.filter(fecha_matricula__gte=dateI)
        if fechaFinal!=None and fechaFinal!="":
          dateF=parse_datetime(fechaFinal+' 00:00:00-00')
          print(dateF)
          matriculaList=matriculaList.filter(fecha_matricula__lte=dateF)



    
        paginator = Paginator(matriculaList, 10)
    
    
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

 

    
        return render(request, 'registration/MatriculacionAdmin.html', {'msg':msg,'matriculasList': page_obj})



@login_required(login_url="/login/")
def PublicoAdmin(request):
  
    publicoObject=Publico.objects.all()

    fechaFinalPersona=None
    fechaInicialPersona=None
  
    idNumberPersona=None

    personaBuscarNombrePersona=None
    is_cookie_set = 0
    
    if 'fechaInicialPersona' in request.session or 'fechaFinalPersona' in request.session or 'idNumberPersona' in request.session or 'personaBuscarNombrePersona' in request.session : 
        fechaFinalPersona = request.session['fechaFinalPersona'] if 'fechaFinalPersona' in request.session else None
        fechaInicialPersona = request.session['fechaInicialPersona'] if 'fechaInicialPersona' in request.session else None
        idNumberPersona=request.session['idNumberPersona'] if 'idNumberPersona' in request.session else None
        personaBuscarNombrePersona=request.session['personaBuscarNombrePersona'] if 'personaBuscarNombrePersona' in request.session else None
       

        
        is_cookie_set = 1

    if request.method == "GET":
      

     if request.GET.get('page')==None:
        is_cookie_set = 0
        request.session['fechaInicialPersona']=None
        request.session['fechaFinalPersona']=None
        request.session['idNumberPersona']=None
        request.session['personaBuscarNombrePersona']=None
        
        fechaInicialPersona=None
        fechaFinalPersona=None
  
        idNumberPersona=None

        personaBuscarNombrePersona=None

      
      
     if (is_cookie_set == 1): 
          if fechaInicialPersona!=None and fechaInicialPersona!="":

           dateI=parse_datetime(fechaInicialPersona+' 00:00:00-00')
          
         
           publicoObject=publicoObject.filter(fecha_registro__gte=dateI)
          if fechaFinalPersona!=None  and fechaFinalPersona!="":

           dateF=parse_datetime(fechaFinalPersona+' 00:00:00-00')
          
          
           publicoObject=publicoObject.filter(fecha_registro__lte=dateF)
          
          if idNumberPersona!=None and idNumberPersona!="":
           publicoObject=publicoObject.filter(docto_identidad__contains=idNumberPersona)

          if personaBuscarNombrePersona!=None and personaBuscarNombrePersona!="":
           publicoObject=publicoObject.filter(Q(nombre__contains=personaBuscarNombrePersona) | Q(apellido__contains=personaBuscarNombrePersona))

    if request.method == "POST":
        
        if (is_cookie_set == 1): 
          
          
         request.session['fechaInicialPersona']=None
         request.session['fechaFinalPersona']=None
         request.session['idNumberPersona']=None
         request.session['personaBuscarNombrePersona']=None

       

        fechaInicialPersona=request.POST.get('fechaInicialPersona') 
        

        print(request.POST)
       
        fechaFinalPersona=request.POST.get('fechaFinalPersona') 
        idNumberPersona=request.POST.get('idNumberPersona') 
        personaBuscarNombrePersona=request.POST.get('personaBuscarNombrePersona') 
        

        if personaBuscarNombrePersona != None and personaBuscarNombrePersona!="":
         
         
         publicoObject=publicoObject.filter(Q(nombre__contains=personaBuscarNombrePersona) | Q(apellido__contains=personaBuscarNombrePersona))

         request.session['personaBuscarNombrePersona'] = personaBuscarNombrePersona

        if idNumberPersona != None and idNumberPersona!="" :
         
         
         publicoObject=publicoObject.filter(docto_identidad__contains=idNumberPersona)
         request.session['idNumberPersona'] = idNumberPersona

        
        if fechaInicialPersona != None and fechaInicialPersona!="":
          dateI=parse_datetime(fechaInicialPersona+' 00:00:00-00')
          fechaI=fechaInicialPersona
          request.session['fechaInicialPersona'] = fechaI
          
          publicoObject=publicoObject.filter(fecha_registro__gte=dateI)

        if fechaFinalPersona != None and fechaFinalPersona!="":
          dateF=parse_datetime(fechaFinalPersona+' 00:00:00-00')
          fechaF=fechaFinalPersona
          request.session['fechaFinalPersona'] = fechaF
          
          publicoObject=publicoObject.filter(fecha_registro__lte=dateF)
          





    msg = None
     
    paginator = Paginator(publicoObject, 10)
    
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if personaBuscarNombrePersona==None:
     personaBuscarNombrePersona=""
    if idNumberPersona==None:
      idNumberPersona=""


            
    context = { 'msg':msg, 'publicoObject':page_obj ,'fechaFinalPersona':fechaFinalPersona,'personaBuscarNombrePersona':personaBuscarNombrePersona,'fechaInicialPersona':fechaInicialPersona,'idNumberPersona':idNumberPersona}
    context['segment'] = 'registration'

  
    html_template = (loader.get_template('registration/PublicoAdmin.html'))

   # return HttpResponse(html_template.render(context, request))
    return render(request, 'registration/PublicoAdmin.html', context)



@login_required(login_url="/login/")
def MatriculacionAdmin(request):

  
    msg = None
    matriculaList=MatriculaAlumnos.objects.all()
    status=TablasConfiguracion.obtenerHijos("EstMatricula")
    types=TablasConfiguracion.obtenerHijos("Tipo Matricula")

    fechaF=None
    fechaI=None
    
    idPersona=None
    idStatus=None
    idTipo=None

    personaBuscarNombre=None

   #numero de paginas para el modal
    publico=Publico.objects.all()
    paginatorP = Paginator(publico, 1)
    
    
    
    
    publicoObject = paginatorP.get_page(1)
    numeroPaginas=publicoObject.paginator.num_pages

    del publicoObject
    del paginatorP
    del publico

    

    is_cookie_set = 0
   
    if 'fechaInicial' in request.session or 'fechaFinal' in request.session or 'idPersona' in request.session or 'idStatus' in request.session or 'idTipo' in request.session : 
        fechaF = request.session['fechaFinal'] if 'fechaFinal' in request.session else None
        fechaI = request.session['fechaInicial'] if 'fechaInicial' in request.session else None
        idPersona=request.session['idPersona'] if 'idPersona' in request.session else None
        idStatus=request.session['idStatus'] if 'idStatus' in request.session else None
        idTipo=request.session['idTipo'] if 'idTipo' in request.session else None

        
        is_cookie_set = 1

   

    if request.method == "GET":
      

      if request.GET.get('page')==None:
        is_cookie_set = 0
        request.session['fechaInicial']=None
        request.session['fechaFinal']=None
        request.session['idPersona']=None
        request.session['idStatus']=None
        request.session['idTipo']=None
        fechaF=None
        fechaI=None
        idPersona=None
        idStatus=None
        idTipo=None

      
      
      if (is_cookie_set == 1): 
          if fechaI!=None and fechaI!="":

           dateI=parse_datetime(fechaI+' 00:00:00-00')
          
         
           matriculaList=matriculaList.filter(fecha_matricula__gte=dateI)
          if fechaF!=None  and fechaF!="":

           dateF=parse_datetime(fechaF+' 00:00:00-00')
          
          
           matriculaList=matriculaList.filter(fecha_matricula__lte=dateF)
          
          if idPersona!=None and idPersona!="":
           matriculaList=matriculaList.filter(fk_publico=idPersona)

          if idTipo!=None and idTipo!="":
           matriculaList=matriculaList.filter(fk_tipo_matricula=idTipo)

          if idStatus!=None and idStatus!="":
           matriculaList=matriculaList.filter(fk_status_matricula=idStatus)


           




    if request.method == "POST":
        
        if (is_cookie_set == 1): 
          
          request.session['fechaInicial']=None
          request.session['fechaFinal']=None
          request.session['idPersona']=None
          request.session['idStatus']=None
          request.session['idTipo']=None

       

        fechaInicial=request.POST.get('fechaInicial') 
        

        print(request.POST)
       
        fechaFinal=request.POST.get('fechaFinal') 
        idPersona=request.POST.get('PersonId') 
        idStatus=request.POST.get('idStatus') 
        idTipo=request.POST.get('idTipo') 
        
        print(request.POST.get('idStatus') )

        
        print("Amtes")
        
        if idTipo!= None and idTipo!="":
         matriculaList=matriculaList.filter(fk_tipo_matricula=idTipo)
         request.session['idTipo'] = idTipo

        print("request.POST")

        if idStatus != None and idStatus!="":
         print("eke")
         
         matriculaList=matriculaList.filter(fk_status_matricula=idStatus)

         request.session['idStatus'] = idStatus
        if idPersona != None and idPersona!="" :
         
         print(idPersona)
         matriculaList=matriculaList.filter(fk_publico=idPersona)
         request.session['idPersona'] = idPersona

        
        if fechaInicial != None and fechaInicial!="":
          dateI=parse_datetime(fechaInicial+' 00:00:00-00')
          fechaI=fechaInicial
          request.session['fechaInicial'] = fechaI
          
          matriculaList=matriculaList.filter(fecha_matricula__gte=dateI)

        if fechaFinal != None and fechaFinal!="":
          dateF=parse_datetime(fechaFinal+' 00:00:00-00')
          fechaF=fechaFinal
          request.session['fechaFinal'] = fechaF
          
          matriculaList=matriculaList.filter(fecha_matricula__lte=dateF)
          

        
          




    
    paginator = Paginator(matriculaList, 10)
    
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if idPersona!=None and idPersona!="" :
     personaBuscarNombre=Publico.objects.get(pk=idPersona)
    else:
      personaBuscarNombre=""
      idPersona=""
    
    if idStatus!=None and idStatus!="":
     idStatus=int(idStatus)
    if idTipo!=None and idTipo!="":
     idTipo=int(idTipo)
            
    context = { 'msg':msg,'matriculasList': matriculaList}
    context['segment'] = 'registration'
    

    
    html_template = (loader.get_template('registration/MatriculacionAdmin.html'))

    
    
   # return HttpResponse(html_template.render(context, request))
    return render(request, 'registration/MatriculacionAdmin.html', {'msg':msg,'matriculasList': page_obj,'FechaInicial':fechaI,'FechaFinal':fechaF, 'publicoObject':numeroPaginas,'idPersona':idPersona,'personaBuscarNombre':personaBuscarNombre, 'selectedStatus':idStatus,'selectedType':idTipo ,'status':status,'types':types, 'segment':'registration'} )




login_required(login_url="/login/")
def MyEnrollments(request):

    msg = None
    publico=Publico.objects.get(user=request.user)

    matriculaList=MatriculaAlumnos.objects.filter(fk_publico=publico)
    status=TablasConfiguracion.obtenerHijos("EstMatricula")
    types=TablasConfiguracion.obtenerHijos("Tipo Matricula")

    
    fechaF=None
    fechaI=None
    
    idStatus=None
    idTipo=None

    personaBuscarNombre=None
    
    context = {}
    context['segment'] = 'registration'




    

    is_cookie_set = 0
   
    if 'fechaInicial' in request.session or 'fechaFinal' in request.session  or 'idStatus' in request.session or 'idTipo' in request.session : 
        fechaF = request.session['fechaFinal'] if 'fechaFinal' in request.session else None
        fechaI = request.session['fechaInicial'] if 'fechaInicial' in request.session else None
        
        idStatus=request.session['idStatus'] if 'idStatus' in request.session else None
        idTipo=request.session['idTipo'] if 'idTipo' in request.session else None

        
        is_cookie_set = 1

   

    if request.method == "GET":
      

      if request.GET.get('page')==None:
        is_cookie_set = 0
        request.session['fechaInicial']=None
        request.session['fechaFinal']=None
        
        request.session['idStatus']=None
        request.session['idTipo']=None
        fechaF=None
        fechaI=None
        
        idStatus=None
        idTipo=None

      
      
      if (is_cookie_set == 1): 
          if fechaI!=None and fechaI!="":

           dateI=parse_datetime(fechaI+' 00:00:00-00')
          
         
           matriculaList=matriculaList.filter(fecha_matricula__gte=dateI)
          if fechaF!=None  and fechaF!="":

           dateF=parse_datetime(fechaF+' 00:00:00-00')
          
          
           matriculaList=matriculaList.filter(fecha_matricula__lte=dateF)
          
          

          if idTipo!=None and idTipo!="":
           matriculaList=matriculaList.filter(fk_tipo_matricula=idTipo)

          if idStatus!=None and idStatus!="":
           matriculaList=matriculaList.filter(fk_status_matricula=idStatus)


           




    if request.method == "POST":
        
        if (is_cookie_set == 1): 
          
          request.session['fechaInicial']=None
          request.session['fechaFinal']=None
          
          request.session['idStatus']=None
          request.session['idTipo']=None

       

        fechaInicial=request.POST.get('fechaInicial') 
        

        print(request.POST)
       
        fechaFinal=request.POST.get('fechaFinal') 
        
        idStatus=request.POST.get('idStatus') 
        idTipo=request.POST.get('idTipo') 
        
        print(request.POST.get('idStatus') )

        
        
        
        if idTipo!= None and idTipo!="":
         matriculaList=matriculaList.filter(fk_tipo_matricula=idTipo)
         request.session['idTipo'] = idTipo

        

        if idStatus != None and idStatus!="":
         
         
         matriculaList=matriculaList.filter(fk_status_matricula=idStatus)

         request.session['idStatus'] = idStatus
       

        
        if fechaInicial != None and fechaInicial!="":
          dateI=parse_datetime(fechaInicial+' 00:00:00-00')
          fechaI=fechaInicial
          request.session['fechaInicial'] = fechaI
          
          matriculaList=matriculaList.filter(fecha_matricula__gte=dateI)

        if fechaFinal != None and fechaFinal!="":
          dateF=parse_datetime(fechaFinal+' 00:00:00-00')
          fechaF=fechaFinal
          request.session['fechaFinal'] = fechaF
          
          matriculaList=matriculaList.filter(fecha_matricula__lte=dateF)
          

        
          




    
    paginator = Paginator(matriculaList, 10)
    
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
   
    if idStatus!=None and idStatus!="":
     idStatus=int(idStatus)
    if idTipo!=None and idTipo!="":
     idTipo=int(idTipo)
    return render(request, 'registration/MyMatriculas.html', {'msg':msg,'matriculasList': page_obj,'FechaInicial':fechaI,'FechaFinal':fechaF, 'selectedStatus':idStatus,'selectedType':idTipo ,'status':status,'types':types, 'segment':'registration'} )

    return render(request, 'registration/MyMatriculas.html', {'msg':msg,'matriculasList': page_obj})


@login_required(login_url="/login/")
def ManagePrices(request):
   #structuras=Estructuraprograma.objects.raw("Select * from app_Estructuraprograma INNER  join registration_PreciosFormacion on app_Estructuraprograma.idestructuraprogrmas=registration_PreciosFormacion Where ( select fk_estruc_programa from registration_PreciosFormacion) ")
   structuras=Estructuraprograma.objects.all()
   structuras=structuras.annotate(precio=F('prize__precio'), fechaIngreso=F('prize__fecha_registro'), id=F('prize__idprograma_precios'), descuento=F('prize__PorcentajeDescuento'), max=Max('prize__idprograma_precios'), amountDiscount=Max('prize__idprograma_precios')  ).filter(id=Max('prize__idprograma_precios'))
   
   fechaFinalPrecios=None
   fechaInicialPrecios=None
    
   cbCurso=None
   cbUnidad=None
   cbProceso=None
   cbPrograma=None
   cbPrecio=None


   is_cookie_set = 0
   
   if 'fechaFinalPrecios' in request.session or 'fechaInicialPrecios' in request.session or 'cbCurso' in request.session or 'cbUnidad' in request.session or 'cbProceso' in request.session  or 'cbPrograma' in request.session or 'cbPrecio' in request.session : 
        fechaFinalPrecios = request.session['fechaFinalPrecios'] if 'fechaFinalPrecios' in request.session else None
        fechaInicialPrecios = request.session['fechaInicialPrecios'] if 'fechaInicialPrecios' in request.session else None
        cbProceso=request.session['cbProceso'] if 'cbProceso' in request.session else None
        cbUnidad=request.session['cbUnidad'] if 'cbUnidad' in request.session else None
        cbCurso=request.session['cbCurso'] if 'cbCurso' in request.session else None
        cbPrograma=request.session['cbPrograma'] if 'cbPrograma' in request.session else None
        cbPrecio=request.session['cbPrecio'] if 'cbPrecio' in request.session else None



        
        is_cookie_set = 1

   if request.GET.get('page')==None:
        is_cookie_set = 0
        request.session['fechaFinalPrecios']=None
        request.session['fechaInicialPrecios']=None
        request.session['cbUnidad']=None
        request.session['cbCurso']=None
        request.session['cbProceso']=None
        request.session['cbPrograma']=None
        request.session['cbPrecio']=None

        

        
        
        fechaInicialPrecios=None
        fechaFinalPrecios=None
        cbCurso=None
        cbUnidad=None
        cbProceso=None
        cbPrecio=None

      
      
        if (is_cookie_set == 1): 
          if fechaInicialPrecios!=None and fechaInicialPrecios!="":

           dateI=parse_datetime(fechaInicialPrecios+' 00:00:00-00')
          
         
           structuras=structuras.filter(fechaIngreso__gte=dateI)

          if fechaFinalPrecios!=None  and fechaFinalPrecios!="":

           dateF=parse_datetime(fechaFinalPrecios+' 00:00:00-00')
          
          
           structuras=structuras.filter(fechaIngreso__lte=dateF)
          
          if cbCurso!="1":
             structuras=structuras.exclude(valor_elemento='Curso')

          if cbUnidad!="2":
             structuras=structuras.exclude(valor_elemento='Unidad')

          if cbProceso!="3":
             structuras=structuras.exclude(valor_elemento='Proceso')

          if cbPrograma!="4":
             structuras=structuras.exclude(valor_elemento='Programa')
          if cbPrecio=="5":
             structuras=structuras.filter(precio=None)
   

   
   if request.method == "POST":
        
        if (is_cookie_set == 1): 
          
          request.session['fechaFinalPrecios']=None
          request.session['fechaInicialPrecios']=None
          request.session['cbUnidad']=None
          request.session['cbCurso']=None
          request.session['cbProceso']=None
          request.session['cbPrograma']=None
          request.session['cbPrecio']=None

          


        print(request.POST)

        fechaInicialPrecios=request.POST.get('fechaInicialPrecios') 
        fechaFinalPrecios=request.POST.get('fechaFinalPrecios') 
        cbUnidad=request.POST.get('cbUnidad') 
        cbCurso=request.POST.get('cbCurso') 
        cbProceso=request.POST.get('cbProceso') 
        cbPrograma=request.POST.get('cbPrograma') 
        cbPrecio=request.POST.get('cbPrecio') 


        
        
        
       
        
        if fechaInicialPrecios != None and fechaInicialPrecios!="":
          dateI=parse_datetime(fechaInicialPrecios+' 00:00:00-00')
          fechaI=fechaInicialPrecios
          request.session['fechaInicialPrecios'] = fechaI
          
          structuras=structuras.filter(fechaIngreso__gte=dateI)

        if fechaFinalPrecios != None and fechaFinalPrecios!="":
          dateF=parse_datetime(fechaFinalPrecios+' 00:00:00-00')
          fechaF=fechaFinalPrecios
          request.session['fechaFinalPrecios'] = fechaF
          
          structuras=structuras.filter(fechaIngreso__lte=dateF)
        
        if cbCurso!="1":
             structuras=structuras.exclude(valor_elemento='Curso')
             request.session['cbCurso'] = cbCurso


        if cbUnidad!="2":
             structuras=structuras.exclude(valor_elemento='Unidad')
             request.session['cbUnidad'] = cbUnidad


        if cbProceso!="3":
             structuras=structuras.exclude(valor_elemento='Proceso')
             request.session['cbProceso'] = cbProceso


        if cbPrograma!="4":
             structuras=structuras.exclude(valor_elemento='Programa')
             request.session['cbPrograma'] = cbPrograma

        if cbPrecio=="5":
             structuras=structuras.filter(precio=None)

             request.session['cbPrecio'] = cbPrecio

        
        

       

   
   paginator = Paginator(structuras, 10)

   for item in paginator.object_list:
     
          descuento=float(item.descuento) if item.descuento!=None else 0
          


          descuentoUnidad=None
          if (item.descuento!=None and item.descuento!=0 ):
            descuentoUnidad=(descuento*0.01) 
            print(descuentoUnidad)

          else:
            descuentoUnidad=1
          
          PO=float(item.precio) if item.precio!=None else 0
          

          PN= (PO*descuentoUnidad ) 
          PN= (PO*descuentoUnidad )  if descuentoUnidad!=1 else 0
          



          PZ=PO-PN
                

                
               
          item.amountDiscount=PZ
          


    

  
    
    
   page_number = request.GET.get('page')
   page_obj = paginator.get_page(page_number)
   print(cbUnidad)
   
   return render(request, 'registration/Courses.html', {"structuras": page_obj, 'segment':'registration','fechaInicialPrecios':fechaInicialPrecios,'fechaFinalPrecios':fechaFinalPrecios,'cbCurso':cbCurso, 'cbProceso':cbProceso,'cbPrograma':cbPrograma,'cbUnidad':cbUnidad, 'cbPrecio':cbPrecio, 'segment':'registration'  })



def MasterPiece(request):
   programa=None
   Unidad=[]
   Cursos=[]
   Proceso=[]

   programa=Estructuraprograma.objects.filter(fk_estructura_padre=None)
   for prog in programa:
      precio=PreciosFormacion.objects.create(fk_estruc_programa=prog, fecha_registro=datetime.date.today(),precio=None,PorcentajeDescuento=None,fk_tipo_moneda=None, fecha_habilitado=None  )
      precio.save()
      
      print(prog.idestructuraprogrmas)
      pro =Estructuraprograma.objects.filter(fk_estructura_padre=prog.idestructuraprogrmas)
      print(pro)

      for p in pro:
       p.valor_elemento="Proceso"
       p.save()
       
       Proceso.append(p) 
   

   for procc in Proceso:
      precio=PreciosFormacion.objects.create(fk_estruc_programa=procc, fecha_registro=datetime.date.today(),precio=None,PorcentajeDescuento=None,fk_tipo_moneda=None, fecha_habilitado=None  )
      precio.save()
      unit =Estructuraprograma.objects.filter(fk_estructura_padre=procc.idestructuraprogrmas)
      for u in unit:
       u.valor_elemento="Unidad"
       u.save()
       Unidad.append(u)     
   unit.update()
   for Unid in Unidad:
      precio=PreciosFormacion.objects.create(fk_estruc_programa=Unid, fecha_registro=datetime.date.today(),precio=None,PorcentajeDescuento=None,fk_tipo_moneda=None, fecha_habilitado=None  )
      precio.save()
      Course =Estructuraprograma.objects.filter(fk_estructura_padre=Unid.idestructuraprogrmas)
      for c in Course:
       precio=PreciosFormacion.objects.create(fk_estruc_programa=c, fecha_registro=datetime.date.today(),precio=None,PorcentajeDescuento=None,fk_tipo_moneda=None, fecha_habilitado=None  )
       precio.save()
       c.valor_elemento="Curso"
       c.save()
       Cursos.append(c)    

    
   
   return render(request, 'registration/Courses.html', {"cursos": Cursos, })







@login_required(login_url="/login/")
def ViewPayments(request):

   
   structuras=MatriculasPagos.objects.all()

   fechaFinalPago=None
   fechaInicialPago=None
      
   userPagoId=None
   idStatusPago=None
   idOrigenPago=None

   userPago=None
   refPago=None



   is_cookie_set = 0
   
   if 'fechaFinalPago' in request.session or 'fechaInicialPago' in request.session or 'userPagoId' in request.session or 'idStatusPago' in request.session or 'idOrigenPago' in request.session or 'refPago' in request.session : 
        fechaFinalPago = request.session['fechaFinalPago'] if 'fechaFinalPago' in request.session else None
        fechaInicialPago = request.session['fechaInicialPago'] if 'fechaInicialPago' in request.session else None
        userPagoId=request.session['userPagoId'] if 'userPagoId' in request.session else None
        idStatusPago=request.session['idStatusPago'] if 'idStatusPago' in request.session else None
        idOrigenPago=request.session['idOrigenPago'] if 'idOrigenPago' in request.session else None
        refPago=request.session['refPago'] if 'refPago' in request.session else None


        
        is_cookie_set = 1

   if request.method == "GET":
      

      if request.GET.get('page')==None:
        is_cookie_set = 0
        request.session['fechaFinalPago']=None
        request.session['fechaInicialPago']=None
        request.session['idStatusPago']=None
        request.session['userPagoId']=None
        request.session['idOrigenPago']=None
        request.session['refPago']=None

        fechaFinalPago=None
        fechaInicialPago=None
              
        userPagoId=None
        idStatusPago=None
        idOrigenPago=None

        userPago=None
        refPago=None

      
      
      if (is_cookie_set == 1): 
          if fechaInicialPago!=None and fechaInicialPago!="":

           dateI=parse_datetime(fechaInicialPago+' 00:00:00-00')
          
         
           structuras=structuras.filter(fecha_pago__gte=dateI)
          if fechaFinalPago!=None  and fechaFinalPago!="":

           dateF=parse_datetime(fechaFinalPago+' 00:00:00-00')
          
          
           structuras=structuras.filter(fecha_pago__lte=dateF)
          
          if userPagoId!=None and userPagoId!="":
           structuras=structuras.filter(fk_matricula_alumnos__fk_publico=userPagoId)

          if idOrigenPago!=None and idOrigenPago!="":
           structuras=structuras.filter(fk_metodopago_id=idOrigenPago)

          if idStatusPago!=None and idStatusPago!="":
           structuras=structuras.filter(status_pay=idStatusPago)

          if refPago!=None and refPago!="":
           structuras=structuras.filter(referencia__contains=refPago)




   if request.method == "POST":
        
        if (is_cookie_set == 1): 
          
          request.session['fechaFinalPago']=None
          request.session['fechaInicialPago']=None
          request.session['idStatusPago']=None
          request.session['userPagoId']=None
          request.session['idOrigenPago']=None
          request.session['refPago']=None

       

        fechaInicialPago=request.POST.get('fechaInicialPago') 
        fechaFinalPago=request.POST.get('fechaFinalPago') 
        userPagoId=request.POST.get('userPagoId') 
        idStatusPago=request.POST.get('idStatusPago') 
        idOrigenPago=request.POST.get('idOrigenPago') 
        refPago=request.POST.get('refPago') 

        
  
        
        if userPagoId!= None and userPagoId!="":
         structuras=structuras.filter(fk_matricula_alumnos__fk_publico=userPagoId)
         request.session['userPagoId'] = userPagoId

       

        if idStatusPago != None and idStatusPago!="":
         structuras=structuras.filter(status_pay=idStatusPago)

         request.session['idStatusPago'] = idStatusPago



        if idOrigenPago != None and idOrigenPago!="" :
         
         
         structuras=structuras.filter(fk_metodopago_id=idOrigenPago)
         request.session['idOrigenPago'] = idOrigenPago


        if refPago != None and refPago!="" :
         
         
         structuras=structuras.filter(referencia__contains=refPago)
         request.session['refPago'] = refPago

        
        if fechaInicialPago != None and fechaInicialPago!="":
          dateI=parse_datetime(fechaInicialPago+' 00:00:00-00')
          fechaI=fechaInicialPago
          request.session['fechaInicial'] = fechaI
          
          structuras=structuras.filter(fecha_matricula__gte=dateI)

        if fechaFinalPago != None and fechaFinalPago!="":
          dateF=parse_datetime(fechaFinalPago+' 00:00:00-00')
          fechaF=fechaFinalPago
          request.session['fechaFinalPago'] = fechaF
          
          structuras=structuras.filter(fecha_matricula__lte=dateF)
          



   
   paginator = Paginator(structuras, 10)
   statusPago=TablasConfiguracion.obtenerHijos('PayStatus')
   origenes=Methods.getOrigenes()


   if userPagoId!=None and userPagoId!="" :
     userPago=Publico.objects.get(pk=userPagoId)
   else:
      userPago=""
      userPagoId=""
    
   if idOrigenPago!=None and idOrigenPago!="":
     idOrigenPago=int(idOrigenPago)

   if idStatusPago!=None and idStatusPago!="":
     idStatusPago=int(idStatusPago)
   
   if refPago==None:
      refPago=""
    
   page_number = request.GET.get('page')
   structuras = paginator.get_page(page_number)

   context = {"structuras": structuras,
    'segment':'registration',
    'statusPago':statusPago,
     'origenes':origenes,
     'idOrigenPago':idOrigenPago,
     'idStatusPago':idStatusPago,
     'userPago':userPago,
     'userPagoId':userPagoId,
     'fechaFinalPago':fechaFinalPago,
      'fechaInicialPago':fechaInicialPago  ,
      'refPago':refPago
      }
   context['segment'] = 'registration'

   
   return render(request, 'registration/viewpay.html', context)







# region parciales

@login_required(login_url="/login/")
def PaymentModal(request):
  id=request.GET.get('id')
  vista=int(request.GET.get('vista'))
  statusPago=TablasConfiguracion.obtenerHijos('PayStatus')
  Ruta=settings.UPLOAD_ROOT


  pago=MatriculasPagos.objects.raw("Select * from registration_matriculaspagos as rmp join registration_matriculaalumnos as rpf on rmp.fk_matricula_alumnos_id=rpf.idmatricula_alumnos join app_publico as ap on ap.idpublico=rpf.fk_publico_id where idmatricula_pagos="+id)
  

  if vista!=3:
   return render(request, 'components/modalEditPay.html', {'pago':pago[0], 'statusPago':statusPago, 'Ruta':Ruta})
  if vista==3:

   return render(request, 'components/modalEditTransfer.html', {'pago':pago[0], 'statusPago':statusPago, 'Ruta':Ruta})


  



def ComboOptions(request):
    structuraProg=request.GET.get("structuraProg")
    subEstructuraProg=Estructuraprograma.objects.filter(fk_estructura_padre=structuraProg)
    return render(request, 'registration/ComboOptions.html', {'subEstructuraProg':subEstructuraProg})
    
 

@login_required(login_url="/login/")
def MatriculacionAdminModal(request):
  
       
    matricula=request.GET.get("matricula")
    

    matriculaApplication=MatriculaAlumnos.objects.get(pk=matricula)
    persona=Publico.objects.get(pk=matriculaApplication.fk_publico.idpublico)
    status=TablasConfiguracion.obtenerHijos("EstMatricula")
    types=TablasConfiguracion.obtenerHijos("Tipo Matricula")

    admin=True if request.GET.get("admin")==1 else False

    

    

    return render(request, 'components/modalMatricula.html', {'matriculaApplication':matriculaApplication,'persona':persona ,'status':status, 'types':types, 'admin':admin })



@login_required(login_url="/login/")
def MatriculacionAddModal(request):
  
 

    # structuraProg=Estructuraprograma.objects.filter(fk_estructura_padre=None)
    structuras=Estructuraprograma.objects.all()

    structuras=structuras.annotate(precio=F('prize__precio'), fechaIngreso=F('prize__fecha_registro'), id=F('prize__idprograma_precios'), descuento=F('prize__PorcentajeDescuento'), max=Max('prize__idprograma_precios'), amountDiscount=Max('prize__idprograma_precios')  ).filter(id=Max('prize__idprograma_precios')  )
    structuras=structuras.filter(fk_estructura_padre=None)
    tipoPrograma=TablasConfiguracion.obtenerHijos("Tipo matricula")
    estatus=TablasConfiguracion.obtenerHijos("EstMatricula")


    return render(request, 'components/modalAddMatricula.html',{'structuraProg':structuras, 'tipoPrograma':tipoPrograma, 'status':estatus})

@login_required(login_url="/login/")
def ModalPay(request):
  if request.method == "GET":
   id=request.GET.get('matricula')
   print (id)
   estructura=Estructuraprograma.objects.get( pk=id  )

   listaPrecio=PreciosFormacion.objects.filter(fk_estruc_programa=estructura)
   listaPrecio=listaPrecio.last()
  

  return render(request, 'components/modalpay.html',{'precio':listaPrecio,})



def ModalPublico(request):
  

    
    msg = None
    publicoObject=Publico.objects.all()
     


    personaBuscar=None
    

   
    is_cookie_set = 0
   
    if 'personaBuscar' in request.session : 
        personaBuscar = request.session['personaBuscar']
        
        
        is_cookie_set = 1

    if request.method == "GET":
      

      if request.GET.get('page')==None:
        is_cookie_set = 0
        request.session['personaBuscar']=None
        
        personaBuscar=None
        

      
      
    if (is_cookie_set == 1): 
          if personaBuscar!=None:

           
          
         
           publicoObject=publicoObject.filter(Q(nombre__contains=personaBuscar) | Q(apellido__contains=personaBuscar))
          

    
    
    if request.method == "POST":
     if (is_cookie_set == 1): 
          
          request.session['fechaInicial']=None
          request.session['fechaFinal']=None
     personaBuscar = request.POST.get('nombreBuscar')
     publicoObject=publicoObject.filter(Q(nombre__contains=personaBuscar) | Q(apellido__contains=personaBuscar) )
     
     request.session['personaBuscar'] = personaBuscar


    paginator = Paginator(publicoObject, 1)
    
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if personaBuscar==None:
      personaBuscar=""
    context = { 'msg':msg,'publicoObject':page_obj ,'personaBuscar':personaBuscar}



   # return HttpResponse(html_template.render(context, request))
    return render(request, 'components/modalPublicoBuscar.html', context)

  #  return render(request, 'components/modalPublico.html', context)

#endregion

# region metodos

@login_required(login_url="/login/")
def save(request):

     if request.method == "POST":
     
      try:
        program=request.POST.get('program')
        cbProcess=request.POST.get('cbProcess')
        cbUnit=request.POST.get('cbUnit')
        cbCourse=request.POST.get('cbCourse')
        statusDB=None
        typeDB=None
        status=request.POST.get('status')

        type=request.POST.get('type')
        idEstruct=None
        if cbCourse!=None and cbCourse!="":
               idEstruct=cbCourse
        elif cbUnit!=None and cbUnit!="" :      
                idEstruct =cbUnit
        elif cbProcess!=None and cbProcess!="" :      
                idEstruct =cbProcess
        else  : 
              idEstruct=program

        
       # publico=Publico.objects.get(user=request.user)


        
        publico=ExtensionUsuario.objects.get(user=request.user).Publico

       

       



        




        struct=Estructuraprograma.objects.get(idestructuraprogrmas=idEstruct)

        if type!=None and type!="":
         typeDB=TablasConfiguracion.objects.get(id_tabla=type)


        if status!=None and status!="":
         statusDB=TablasConfiguracion.objects.get(id_tabla=status)
        else:
         statusDB=TablasConfiguracion.objects.get(valor_elemento='EstatusRevision')
       


        
        matricula=MatriculaAlumnos.objects.create(fk_publico=publico,fk_estruc_programa=struct, fecha_matricula=datetime.date.today(),fk_tipo_matricula=typeDB,fk_status_matricula=statusDB,fecha_aprobada=None  )
        matricula.save()
        return HttpResponse("Errolment application saved")

      except:
        return HttpResponse("Error, try again later")

@login_required(login_url="/login/")
def saveDiscount(request):
   if request.method == "POST":
     
      try:
        print(request.POST)
        porcentaje=request.POST.get('porcentaje')
        idEstructura=request.POST.get('idEstructura')
        

        
        struct=Estructuraprograma.objects.get(idestructuraprogrmas=idEstructura)
        
        precioViejo=PreciosFormacion.objects.filter(fk_estruc_programa=idEstructura).last()
        

        
        precioNuevo=PreciosFormacion.objects.create(fk_estruc_programa=struct, fecha_registro=datetime.date.today(),PorcentajeDescuento=porcentaje, precio=precioViejo.precio, fk_tipo_moneda=precioViejo.fk_tipo_moneda  )
        precioNuevo.save()

        nivelProceso=0
        if struct.valor_elemento=="Programa":
          nivelProceso=0
          

        if struct.valor_elemento=="Proceso":
          nivelProceso=1
        
        if struct.valor_elemento=="Unidad":
          nivelProceso=2

        
        

        hijoMayor =struct
        for x in range(nivelProceso):
              precioHijos=0
              hijos=Estructuraprograma.objects.filter(fk_estructura_padre=hijoMayor.fk_estructura_padre)
              for u in hijos:

                precioH=PreciosFormacion.LastStructura(u.idestructuraprogrmas)
                descuentoHijo=None 
                print(u)
                print(precioH.precio)
                print(precioHijos)

                pp=float(precioH.PorcentajeDescuento) if precioH.PorcentajeDescuento!=None else 0
                print("ssss")
                print("pp")
                print(pp)

                


                


                if (precioH.PorcentajeDescuento!=None and precioH.PorcentajeDescuento!=0.0 ):
                  descuentoHijo=(pp*0.01) 
                  print(descuentoHijo)

                else:
                  descuentoHijo=1
                  print("pedro")

                  print(descuentoHijo)



                  
                PO=float(precioH.precio)
                print("pedro")

                print(PO)
                

                PN= (PO*descuentoHijo )  if descuentoHijo!=1 else 0
                print("PN")

                print(PN)


                PZ=PO-PN
                

                
                print(PZ)
                print("xcvxcv")

                precioHijos=PZ+precioHijos if precioH.precio !=None else None
                print("dfm12312kj")


              padre=Estructuraprograma.objects.get(pk=hijoMayor.fk_estructura_padre.pk)
              print("dfmkj")

        
              precioViejo=PreciosFormacion.objects.filter(fk_estruc_programa=padre.pk).last()
                
              print("precioViejo" )
              print(precioHijos)

                #Inserto Nuevo Precio para proceso
              if precioHijos!=None:

                  precioViejo=PreciosFormacion.objects.filter(fk_estruc_programa=padre.pk).last()
                  

                  nuevoPrecio=PreciosFormacion.objects.create(fk_estruc_programa=padre, fecha_registro=datetime.date.today(),PorcentajeDescuento=precioViejo.PorcentajeDescuento, precio=precioHijos, fk_tipo_moneda=precioViejo.fk_tipo_moneda  )
                  nuevoPrecio.save()
              else:
                  nuevoPrecio=PreciosFormacion.objects.create(fk_estruc_programa=padre, fecha_registro=datetime.date.today(),PorcentajeDescuento=precioViejo.PorcentajeDescuento, precio=None, fk_tipo_moneda=precioViejo.fk_tipo_moneda  )
                  nuevoPrecio.save()

              hijoMayor=padre
            
          

        return HttpResponse("Errolment application saved")

      except:
        return HttpResponse("Error, try again later")

@login_required(login_url="/login/")
def savePrices(request):
   if request.method == "POST":
     
      try:
        print(request.POST)
        precio=request.POST.get('precio')
        idEstructura=request.POST.get('idEstructura')
        

        
        struct=Estructuraprograma.objects.get(idestructuraprogrmas=idEstructura)
        
        precioViejo=PreciosFormacion.objects.filter(fk_estruc_programa=idEstructura).last()
        

        #inserto precio nuevo Curso
        precioNuevo=PreciosFormacion.objects.create(fk_estruc_programa=struct, fecha_registro=datetime.date.today(),PorcentajeDescuento=precioViejo.PorcentajeDescuento, precio=precio, fk_tipo_moneda=precioViejo.fk_tipo_moneda  )
        precioNuevo.save()



        #Consulto Precio cursos de esa unidad 
        cursos=Estructuraprograma.objects.filter(fk_estructura_padre=struct.fk_estructura_padre)


        precioCursos=0
        for curso in cursos:
          precioCurso=PreciosFormacion.LastStructura(curso.idestructuraprogrmas)
          precioCursos=precioCursos+precioCurso.precio if precioCurso.precio !=None else None



        #consulto unidad
        unidad=Estructuraprograma.objects.get(pk=struct.fk_estructura_padre.pk)
        
        precioViejo=PreciosFormacion.objects.filter(fk_estruc_programa=unidad.pk).last()
        
        #inserto nuevo precio unidad
       
        if precioCursos!=None:

         precioViejo=PreciosFormacion.objects.filter(fk_estruc_programa=unidad.pk).last()
         

         nuevoPrecio=PreciosFormacion.objects.create(fk_estruc_programa=unidad, fecha_registro=datetime.date.today(),PorcentajeDescuento=precioViejo.PorcentajeDescuento, precio=precioCursos, fk_tipo_moneda=precioViejo.fk_tipo_moneda  )
         nuevoPrecio.save()
        else:
         nuevoPrecio=PreciosFormacion.objects.create(fk_estruc_programa=unidad, fecha_registro=datetime.date.today(),PorcentajeDescuento=precioViejo.PorcentajeDescuento, precio=None, fk_tipo_moneda=precioViejo.fk_tipo_moneda  )
         nuevoPrecio.save()
         
        #Calculo precio proceso usando las unidades
        precioUnidades=0
        unidades=Estructuraprograma.objects.filter(fk_estructura_padre=unidad.fk_estructura_padre)
        for u in unidades:

          precioU=PreciosFormacion.LastStructura(u.idestructuraprogrmas)
          descuentoUnidad=None 
          print(u)
          print(precioU.precio)
          print(precioUnidades)

          pp=float(precioU.PorcentajeDescuento) if precioU.PorcentajeDescuento!=None else 0
          print("ssss")


          if (precioU.PorcentajeDescuento!=None and precioU.PorcentajeDescuento!=0 ):
            descuentoUnidad=(pp*0.01) 
            print(descuentoUnidad)

          else:
            descuentoUnidad=1


            
          PO=float(precioU.precio)
          

          PN= (PO*descuentoUnidad )  if descuentoUnidad!=1 else 0
          PZ=PO-PN
          

          
          print(PN+precioUnidades)
          precioUnidades=PZ+precioUnidades if precioU.precio !=None else None

        
         #consulto proceso
        proceso=Estructuraprograma.objects.get(pk=unidad.fk_estructura_padre.pk)
        
        precioViejo=PreciosFormacion.objects.filter(fk_estruc_programa=proceso.pk).last()
        

        #Inserto Nuevo Precio para proceso
        if precioUnidades!=None:

         precioViejo=PreciosFormacion.objects.filter(fk_estruc_programa=proceso.pk).last()
         

         nuevoPrecio=PreciosFormacion.objects.create(fk_estruc_programa=proceso, fecha_registro=datetime.date.today(),PorcentajeDescuento=precioViejo.PorcentajeDescuento, precio=precioUnidades, fk_tipo_moneda=precioViejo.fk_tipo_moneda  )
         nuevoPrecio.save()
        else:
         nuevoPrecio=PreciosFormacion.objects.create(fk_estruc_programa=proceso, fecha_registro=datetime.date.today(),PorcentajeDescuento=precioViejo.PorcentajeDescuento, precio=None, fk_tipo_moneda=precioViejo.fk_tipo_moneda  )
         nuevoPrecio.save()

        #Calculo precio programa usando los procesos
        precioProcesos=0
        procesos=Estructuraprograma.objects.filter(fk_estructura_padre=proceso.fk_estructura_padre)
        for p in procesos:
          precioP=PreciosFormacion.LastStructura(p.idestructuraprogrmas)
          descuentoProceso=None 
          print(p)
          print(precioP.precio)
          print(precioProcesos)

          pp=float(precioP.PorcentajeDescuento) if precioP.PorcentajeDescuento!=None else 0
          print("yyy")


          if (precioP.PorcentajeDescuento!=None and precioP.PorcentajeDescuento!=0 ):
            descuentoProceso=(pp*0.01) 
            print(descuentoProceso)

          else:
            descuentoProceso=1

          PO=float(precioP.precio)
          

          PN= (PO*descuentoProceso )  if descuentoProceso!=1 else 0
          PZ=PO-PN


          print(PN+precioProcesos)
          precioProcesos=PZ+precioProcesos if precioP.precio !=None else None


         # precioProcesos=precioProcesos+precioP.precio if precioP.precio !=None else None
          #print(precioProcesos)

          #consulto programa
        programa=Estructuraprograma.objects.get(pk=proceso.fk_estructura_padre.pk)
        
        precioViejo=PreciosFormacion.objects.filter(fk_estruc_programa=programa.pk).last()

         #Inserto Nuevo Precio para programa
        if precioProcesos!=None:

         precioViejo=PreciosFormacion.objects.filter(fk_estruc_programa=programa.pk).last()
         

         nuevoPrecio=PreciosFormacion.objects.create(fk_estruc_programa=programa, fecha_registro=datetime.date.today(),PorcentajeDescuento=precioViejo.PorcentajeDescuento, precio=precioProcesos, fk_tipo_moneda=precioViejo.fk_tipo_moneda  )
         nuevoPrecio.save()
        else:
         nuevoPrecio=PreciosFormacion.objects.create(fk_estruc_programa=programa, fecha_registro=datetime.date.today(),PorcentajeDescuento=precioViejo.PorcentajeDescuento, precio=None, fk_tipo_moneda=precioViejo.fk_tipo_moneda  )
         nuevoPrecio.save()
        

        
        


         
       

        return HttpResponse("Errolment application saved")

      except:
        return HttpResponse("Error, try again later")


@login_required(login_url="/login/")
def ManagePersonSave(request):

     if request.method == "POST":
     
      try:
        program=request.POST.get('program')
        cbProcess=request.POST.get('cbProcess')
        cbUnit=request.POST.get('cbUnit')
        cbCourse=request.POST.get('cbCourse')
        idPersona=request.POST.get('id')
        statusDB=None
        typeDB=None
        status=request.POST.get('status')

        type=request.POST.get('type')
        idEstruct=None
        if cbCourse!=None and cbCourse!="":
               idEstruct=cbCourse
        elif cbUnit!=None and cbUnit!="" :      
                idEstruct =cbUnit
        elif cbProcess!=None and cbProcess!="" :      
                idEstruct =cbProcess
        else  : 
              idEstruct=program

        
        publico=Publico.objects.get(pk=idPersona)
        struct=Estructuraprograma.objects.get(idestructuraprogrmas=idEstruct)
        if type!=None and type!="":
          typeDB=TablasConfiguracion.objects.get(id_tabla=type)


        if status!=None and status!="":
         statusDB=TablasConfiguracion.objects.get(id_tabla=status)
        else:
         statusDB=TablasConfiguracion.objects.get(valor_elemento='EstatusRevision')
       


        
        matricula=MatriculaAlumnos.objects.create(fk_publico=publico,fk_estruc_programa=struct, fecha_matricula=datetime.date.today(),fk_tipo_matricula=typeDB,fk_status_matricula=statusDB,fecha_aprobada=None  )
        matricula.save()
        return HttpResponse("Errolment application saved")

      except:
        return HttpResponse("Error, try again later")

        
@login_required(login_url="/login/")
def updateEnrollment(request):

     if request.method == "POST":
     
      try:
        status=request.POST.get('status')
       

        type=request.POST.get('type')
        
        id=request.POST.get('id')
        print(id)
        
        estado=TablasConfiguracion.objects.get(id_tabla=status)
        
        tipo=TablasConfiguracion.objects.get(id_tabla=type)

        matricula=MatriculaAlumnos.objects.get( pk=id  )
        
        matricula.fk_status_matricula=estado
        matricula.fk_tipo_matricula=tipo
        matricula.save()
        return HttpResponse("Changes saved")

      except:
        return HttpResponse("Error, try again later")


@login_required(login_url="/login/")
def Pay(request):
    
  context = {}
  context['segment'] = 'registration'

  msg = None
  
  structuraProg = ""
  tipoPrograma  = "" 
  doc_et=PreciosFormacion.objects.all()
  
  return render(request, 'registration/Pyments.html', {"doc_et": doc_et, "msg" : msg,'structuraProg':structuraProg, 'tipoPrograma':tipoPrograma})



@login_required(login_url="/login/")
def GetPrice(request):
  if request.method == "GET":
   id=request.GET.get('matricula')
   print (id)
   estructura=Estructuraprograma.objects.get( pk=id  )

   listaPrecio=PreciosFormacion.objects.filter(fk_estruc_programa=estructura)
   listaPrecio=listaPrecio.last()


   if listaPrecio.PorcentajeDescuento==None or listaPrecio.PorcentajeDescuento==0 :
       precio=listaPrecio.precio
   else:
       precio=listaPrecio.precio*(listaPrecio.PorcentajeDescuento*0.01)

      



  return HttpResponse(precio)


@login_required(login_url="/login/")
def updatePayStatus(request):


    
   if request.method == "POST":
      
      try:



        
        id=request.POST.get('idPago')
        status=request.POST.get('statusG')

        
        estado=TablasConfiguracion.objects.get(id_tabla=status)
        
      
        

        matricula=MatriculasPagos.objects.get( pk=id  )
        
        matricula.status_pay=estado
       
        matricula.save()
        return HttpResponse("Changes saved")

      except:
        return HttpResponse("Error, try again later")

@login_required(login_url="/login/")
def hashPay(request):

  
         
       
       hash = uuid.uuid4()
      # contraseña_cifrada = hashlib.sha512(contraseña.encode()) 
      # print(contraseña_cifrada.hexdigest())
      # hash=contraseña_cifrada.hexdigest()   
       #print (hash.hexdigest())
       #m = hashlib.shake_128(b.binary_converted)
       #hash=m.hexdigest(15)
       print(hash)
       return HttpResponse(hash)


@login_required(login_url="/login/")
def InsertPayTr(request):

     if request.method == "POST":
        print(request.POST)
        hash=request.POST.get('hash')
        precio=request.POST.get('precio')
        matricula=request.POST.get('matricula')
        

        
        matriculadb = MatriculaAlumnos.objects.get(idmatricula_alumnos = matricula)
        

        reference=request.POST.get('reference')
        origen=request.POST.get('origen')
       
        if origen == '3':
          
          myfile = request.FILES['imagenRuta']
          
          fs = FileSystemStorage(location=settings.UPLOAD_ROOT )
          nombreImagen = str(uuid.uuid4())
          extensionFile=Path(myfile.name).suffix
          nombreImagen=nombreImagen+extensionFile
          Ruta=settings.UPLOAD_ROOT
          


          folder = request.path.replace("/", "_")
          try:
            os.mkdir(os.path.join(Ruta))
          except:
           pass

        

          filename = fs.save(Ruta+'/'+nombreImagen, myfile)
          

          id4 = nombreImagen

          statusPago=TablasConfiguracion.objects.get(valor_elemento='payWait')

         
          showtime=datetime.datetime.now() # Returns 2018-01-15 09:00

          Pago = MatriculasPagos.objects.create(
            fk_matricula_alumnos = matriculadb,
            fk_metodopago_id  = 3,
            monto_cancel  = precio,
            fk_tipomoneda  = None,
            fecha_pago = showtime,
            referencia   = reference,
            status_pay = statusPago ,
            codigo_hash   = hash,
            url_imagen  = id4  )
          Pago.save()

          matriculadb.fk_status_matricula=TablasConfiguracion.objects.get('EstatusPay')
          matriculadb.save()

          return HttpResponse("Changes saved con valor")   
        else:
         

          statusPago=TablasConfiguracion.objects.get(valor_elemento='payConfirm')

         
          showtime=datetime.datetime.now() # Returns 2018-01-15 09:00

          Pago = MatriculasPagos.objects.create(
            fk_matricula_alumnos = matriculadb,
            fk_metodopago_id  = 1,
            monto_cancel  = precio,
            fk_tipomoneda  = None,
            fecha_pago = showtime,
            referencia   = reference,
            status_pay = statusPago ,
            codigo_hash   = None,
            url_imagen  = None  )
          Pago.save()
          matriculadb.fk_status_matricula=TablasConfiguracion.objects.get('EstatusAprovado')
          matriculadb.save()

              
#endregion
      

@login_required(login_url="/login/")
def ModalPayDetail2(request):

    structuraProg=""
    tipoPrograma=""

    return render(request, 'components/modalpaydetail2.html',{'structuraProg':structuraProg, 'tipoPrograma':tipoPrograma})
    
@login_required(login_url="/login/")
def ModalPayDetail(request):

    # idU=request.POST.get('un')
    # idC=request.POST.get('cant')
    idU="12"
    idC="24"
    structuraProg=""
    tipoPrograma=""

    return render(request, 'components/modalpaydetail.html',{'idU':idU, 'idC':idC})