from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django import template
from django.template import loader
from modules.registration import forms
from modules.app.models import Estructuraprograma
from modules.app.models import TablasConfiguracion
from modules.app.models import Publico
from modules.registration.models import MatriculaAlumnos
from django.http import JsonResponse
import datetime
from modules.app import Methods
from django.core.paginator import Paginator
from django.utils.dateparse import parse_datetime
from modules.registration.models import PreciosFormacion

# Create your views here.



@login_required(login_url="/login/")
def enrollment(request):
  

    form = forms.MatriculaForm(request.POST or None)


    msg = None
    structuraProg=Estructuraprograma.objects.filter(fk_estructura_padre=None)
    tipoPrograma=TablasConfiguracion.obtenerHijos("Tipo matricula")


            
    context = {}
   # context['segment'] = 'index'

    html_template = loader.get_template( 'registration/Matriculacion.html' )

    #return HttpResponse(html_template.render(context, request))
    return render(request, 'registration/Matriculacion.html', {"form": form, "msg" : msg,'structuraProg':structuraProg, 'tipoPrograma':tipoPrograma})

@login_required(login_url="/login/")
def ManageEnrollments(request):
   msg = None
   matriculaList=MatriculaAlumnos.objects.all()


   if request.method == "POST":
        
      
        idPersona=request.POST.get('idPersona') 
        print(idPersona + "ssss")
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
  

    
    msg = None
    publicoObject=Publico.objects.all()
     
    paginator = Paginator(publicoObject, 10)
    
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


            
    context = { 'msg':msg, 'publicoObject':page_obj}
   # context['segment'] = 'index'

  
    html_template = (loader.get_template('registration/PublicoAdmin.html'))

   # return HttpResponse(html_template.render(context, request))
    return render(request, 'registration/PublicoAdmin.html', context)


@login_required(login_url="/login/")
def MatriculacionAdmin(request):

    msg = None
    matriculaList=MatriculaAlumnos.objects.all()
    fechaF=None
    fechaI=None

    is_cookie_set = 0
   
    if 'fechaInicial' in request.session and 'fechaFinal' or request.session: 
        fechaF = request.session['fechaFinal']
        fechaI = request.session['fechaInicial']
        
        is_cookie_set = 1

   

    if request.method == "GET":
      

      if request.GET.get('page')==None:
        is_cookie_set = 0
        request.session['fechaInicial']=None
        request.session['fechaFinal']=None
        fechaF=None
        fechaI=None

      
      
      if (is_cookie_set == 1): 
          if fechaI!=None:

           dateI=parse_datetime(fechaI+' 00:00:00-00')
          
         
           matriculaList=matriculaList.filter(fecha_matricula__gte=dateI)
          if fechaI!=fechaF:

           dateF=parse_datetime(fechaF+' 00:00:00-00')
          
          
           matriculaList=matriculaList.filter(fecha_matricula__lte=dateF)



    if request.method == "POST":
        
        if (is_cookie_set == 1): 
          
          request.session['fechaInicial']=None
          request.session['fechaFinal']=None
       

        fechaInicial=request.POST.get('fechaInicial') 

       
        fechaFinal=request.POST.get('fechaFinal') 
        idPersona=request.POST.get('idPersona') 

        if idPersona!=None and idPersona!="":
         matriculaList=matriculaList.filter(fk_publico=idPersona)
        
        if fechaInicial!=None and fechaInicial!="":
          dateI=parse_datetime(fechaInicial+' 00:00:00-00')
          fechaI=fechaInicial
          request.session['fechaInicial'] = fechaI
          
          matriculaList=matriculaList.filter(fecha_matricula__gte=dateI)
        if fechaFinal!=None and fechaFinal!="":
          dateF=parse_datetime(fechaFinal+' 00:00:00-00')
          fechaF=fechaFinal
          request.session['fechaFinal'] = fechaF
          
          matriculaList=matriculaList.filter(fecha_matricula__lte=dateF)
          

        
          




    
    paginator = Paginator(matriculaList, 10)
    
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

 
            
    context = { 'msg':msg,'matriculasList': matriculaList}
   # context['segment'] = 'index'

    
    html_template = (loader.get_template('registration/MatriculacionAdmin.html'))

   # return HttpResponse(html_template.render(context, request))
    return render(request, 'registration/MatriculacionAdmin.html', {'msg':msg,'matriculasList': page_obj,'FechaInicial':fechaI,'FechaFinal':fechaF})




login_required(login_url="/login/")
def MyEnrollments(request):

    msg = None
    publico=Publico.objects.get(user=request.user)

    matriculaList=MatriculaAlumnos.objects.filter(fk_publico=publico)


    if request.method == "POST":
        
        print(request.POST)
        
        print(request.POST.get('idPersona'))

        fechaInicial=request.POST.get('fechaInicial') 

       
        fechaFinal=request.POST.get('fechaFinal') 
        idPersona=request.POST.get('idPersona') 

       # matriculaList=matriculaList.filter(fk_publico=idPersona)
        print(fechaFinal)
        print(fechaFinal)
        if fechaInicial!=None and fechaInicial!="":
          dateI=parse_datetime(fechaInicial+' 00:00:00-00')

          matriculaList=matriculaList.filter(fecha_matricula__gte=dateI)
        if fechaFinal!=None and fechaFinal!="":
          dateF=parse_datetime(fechaFinal+' 00:00:00-00')
          print(dateF)
          matriculaList=matriculaList.filter(fecha_matricula__lte=dateF)





    
    paginator = Paginator(matriculaList, 10)
    
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

 
            
    context = { 'msg':msg,'matriculasList': matriculaList}
   # context['segment'] = 'index'

    
    html_template = (loader.get_template('registration/MatriculacionAdmin.html'))

   # return HttpResponse(html_template.render(context, request))
    return render(request, 'registration/MyMatriculas.html', {'msg':msg,'matriculasList': page_obj})


@login_required(login_url="/login/")
def Courses(request):
   programa=None
   Unidad=[]
   Cursos=[]
   Proceso=[]

   programa=Estructuraprograma.objects.filter(fk_estructura_padre=None)
   for prog in programa:
      print(prog.idestructuraprogrmas)
      pro =Estructuraprograma.objects.filter(fk_estructura_padre=prog.idestructuraprogrmas)
      print(pro)

      for p in pro:
       Proceso.append(p) 


   for procc in Proceso:
      unit =Estructuraprograma.objects.filter(fk_estructura_padre=procc.idestructuraprogrmas)
      for u in unit:
       Unidad.append(u)     

   for Unid in Unidad:
      Course =Estructuraprograma.objects.filter(fk_estructura_padre=Unid.idestructuraprogrmas)
      for c in Course:
       Cursos.append(c)    

   return render(request, 'registration/Courses.html', {"cursos": Cursos, })




#parciales
def ComboOptions(request):
    structuraProg=request.GET.get("structuraProg")
    subEstructuraProg=Estructuraprograma.objects.filter(fk_estructura_padre=structuraProg)
    return render(request, 'registration/ComboOptions.html', {'subEstructuraProg':subEstructuraProg})
    
 

@login_required(login_url="/login/")
def MatriculacionAdminModal(request):
  
       
    matricula=request.GET.get("matricula")
    matriculaApplication=MatriculaAlumnos.objects.get(pk=matricula)
    persona=Publico.objects.get(pk=matriculaApplication.fk_publico.idpublico)
    status=TablasConfiguracion.obtenerHijos("Status")
    types=TablasConfiguracion.obtenerHijos("Tipo Matricula")

    

    

    return render(request, 'components/modalMatricula.html', {'matriculaApplication':matriculaApplication,'persona':persona ,'status':status, 'types':types})



@login_required(login_url="/login/")
def MatriculacionAddModal(request):
  
    structuraProg=Estructuraprograma.objects.filter(fk_estructura_padre=None)
    tipoPrograma=TablasConfiguracion.obtenerHijos("Tipo matricula")

    return render(request, 'components/modalAddMatricula.html',{'structuraProg':structuraProg, 'tipoPrograma':tipoPrograma})

@login_required(login_url="/login/")
def ModalPay(request):
  if request.method == "GET":
   id=request.GET.get('matricula')
   print (id)
   estructura=Estructuraprograma.objects.get( pk=id  )

   listaPrecio=PreciosFormacion.objects.filter(fk_estruc_programa=estructura)
   listaPrecio=listaPrecio.last()
  

  return render(request, 'components/modalpay.html',{'precio':listaPrecio,})

@login_required(login_url="/login/")
def ModalPayDetail(request):
  
    # idU=request.POST.get('un')
    # idC=request.POST.get('cant')
    idU="12"
    idC="24"
    structuraProg=""
    tipoPrograma=""

    return render(request, 'components/modalpaydetail.html',{'idU':idU, 'idC':idC})

@login_required(login_url="/login/")
def ModalPayDetail2(request):
  
    structuraProg=""
    tipoPrograma=""

    return render(request, 'components/modalpaydetail2.html',{'structuraProg':structuraProg, 'tipoPrograma':tipoPrograma})


#metod
@login_required(login_url="/login/")
def save(request):

     if request.method == "POST":
     
      try:
        program=request.POST.get('program')
        cbProcess=request.POST.get('cbProcess')
        cbUnit=request.POST.get('cbUnit')
        cbCourse=request.POST.get('cbCourse')

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

        
        publico=Publico.objects.get(user=request.user)
        struct=Estructuraprograma.objects.get(idestructuraprogrmas=idEstruct)
        tipo=TablasConfiguracion.objects.get(id_tabla=type)

        
        matricula=MatriculaAlumnos.objects.create(fk_publico=publico,fk_estruc_programa=struct, fecha_matricula=datetime.date.today(),fk_tipo_matricula=tipo,fk_status_matricula=None,fecha_aprobada=None  )
        matricula.save()
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
        tipo=TablasConfiguracion.objects.get(id_tabla=type)

        
        matricula=MatriculaAlumnos.objects.create(fk_publico=publico,fk_estruc_programa=struct, fecha_matricula=datetime.date.today(),fk_tipo_matricula=tipo,fk_status_matricula=None,fecha_aprobada=None  )
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
   precio=listaPrecio.precio

  return HttpResponse(precio)

   

