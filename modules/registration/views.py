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

# Create your views here.

def ComboOptions(request):
    structuraProg=request.GET.get("structuraProg")
    subEstructuraProg=Estructuraprograma.objects.filter(fk_estructura_padre=structuraProg)
    return render(request, 'registration/ComboOptions.html', {'subEstructuraProg':subEstructuraProg})
    
 


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
def PublicoAdmin(request):
  

    
    msg = None
    publicoObject=Publico.objects.all()
    


            
    context = { 'msg':msg, 'publicoObject':publicoObject}
   # context['segment'] = 'index'

  
    html_template = (loader.get_template('registration/PublicoAdmin.html'))

   # return HttpResponse(html_template.render(context, request))
    return render(request, 'registration/PublicoAdmin.html', context)


@login_required(login_url="/login/")
def MatriculacionAdmin(request):
  

    
    msg = None
    matriculaList=MatriculaAlumnos.objects.all()
    


            
    context = { 'msg':msg,'matriculasList': matriculaList}
   # context['segment'] = 'index'

    
    html_template = (loader.get_template('registration/MatriculacionAdmin.html'))

   # return HttpResponse(html_template.render(context, request))
    return render(request, 'registration/MatriculacionAdmin.html', {'msg':msg,'matriculasList': matriculaList})




#parciales
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


  
