from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages.api import success
from django.shortcuts import render, redirect  
from .forms import competenciaAdqForm, competenciaForm, perfilForm
from .models import CompetenciasAdq, Perfil, CompetenciasReq, cursos_prerequisitos
from ..app.models import Estructuraprograma, TablasConfiguracion, Publico
from ..app.Methods import MyMethod
from ..security.models import ExtensionUsuario, CtaUsuario
from ..registration.models import MatriculaAlumnos
from json import dumps
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.template.defaulttags import register
from django.db.models import Q, F, Max
import re
from django.core import serializers
from django.http import HttpResponse
import json
from ..security import Methods
# Create your views here.
TITULOPERFIL = {'idperfil': '#', 'deescripcion': 'Name', 'desc_corta': 'Description', 'fk_rama': 'Branch'}
TITULOCOMPETENCIA = {'idcompetenciasreq': '#', 'desc_competencia': 'Name', 'fk_perfil': 'Profile', 'fk_tipo_competencia': 'Type', 'fk_nivel': 'Minimum Level'}
TITULOCOMPETENCIAADQ = {'idcompetencias_adq': '#', 'fk_publico': 'Public', 'periodo': 'Period', 'experiencia': 'Experience', 'fk_tipo_duracion': 'Duration', 'fk_competencia': 'Competence', 'fk_nivel': 'Level'}
TITULOPLAN = {'idpublico':'#', 'nombre': 'Name', 'apellido': 'Last Name'}
TITULOPLANES = {'idmatricula_alumnos': '#', 'fk_estruc_programa': 'Program', 'fecha_matricula': 'Date', 'fk_status_matricula': 'Status'}
TITULOPUBLIC = {'idpublico':'#', 'nombre': 'Name', 'apellido': 'Last Name', 'fk_rol_usuario': 'Role', 'telefonos': 'Primary Phone', 'correos': 'Primary Email:', 'fk_status_cuenta': 'Status'}

@register.filter
def get_attr(dictionary, key):
    return(getattr(dictionary, key))

@register.filter
def get_list(dictionary, key):
    return dictionary[key-1]

@register.filter
def replaces(value, key):
    txt = re.search(key, value, flags = re.IGNORECASE)
    print(txt)
    return re.sub(key, '<b style="background-color:#c0ffc8;">%s</b>' %txt[0], value, flags = re.IGNORECASE, count =1)

@register.filter
def matches(value, key):
    return re.search(key, value, flags = re.IGNORECASE) != None

@register.filter
def tostring(value):
    return str(value)

@register.filter
def hasPrograms(value):
    return len(MatriculaAlumnos.objects.filter(fk_publico = value, origenSolicitud = MyMethod.ReturnCode('Planning'))) > 0

@register.filter
def tostringJson(value, key):
    try:
        txt = json.loads(value)
        return txt[key] if txt[key] else ""
    except:
        return ""

def show(request): 


    if(request.user.is_staff):
        
        search_query = request.GET.get('search_box', "")
        plan = Perfil.objects.all()

        if(search_query):

            plan = plan.filter(deescripcion__icontains=search_query) 

        return render(request,"planning/show.html",{'plan':paginas(request, plan), 'keys' : TITULOPERFIL, 'urlEdit': 'createProfile', 'urlRemove': 'destroyProfilage', 'search':search_query, 'categoria': 'profile', 'segment':'planning'}) 
    
    else:
        
        return redirect('/') 


def showCompetences(request): 

    if(request.user.is_staff):

        search_query = request.GET.get('search_box', "")
        competencia = CompetenciasReq.objects.all()  

        if(search_query):

            competencia = competencia.filter(desc_competencia__icontains=search_query) 

        return render(request,"planning/showCompetence.html",{'plan': paginas(request, competencia), 'keys' : TITULOCOMPETENCIA, 'urlEdit': 'createCompetence', 'urlRemove': 'destroyCompetence', 'categoria': 'competence', 'search':search_query, 'segment':'planning'}) 
    
    else:

        return redirect('/') 

def showCompetencesAdq(request):  

    search_query = request.GET.get('search_box', "")
    competencia = CompetenciasAdq.objects.all()
    # print(request.user)
    if not request.user.is_staff:

        competencia = competencia.filter(fk_publico = ExtensionUsuario.objects.get(user = request.user).Publico)

    if(search_query and request.user.is_staff):

        competencia = competencia.filter(fk_publico__nombre__icontains=search_query) 

    return render(request,"planning/showCompetenceAdq.html",{'plan': paginas(request, competencia), 'keys' : TITULOCOMPETENCIAADQ, 'urlEdit': 'createCompetenceAdq', 'urlRemove': 'destroyCompetenceAdq', 'categoria': 'competenceadq', 'search':search_query, 'segment':'planning'}) 

def showProgram(request): 
     
    search_query = request.GET.get('search_box', "")
    program = Publico.objects.all()
    return render(request,"planning/showProgram.html",{'plan': paginas(request, program), 'keys' : TITULOPLAN, 'urlEdit': 'editProgram', 'urlRemove': 'destroyProgram', 'search':search_query, 'tipo':'Schedule', 'segment':'planning'}) 

def editProgram(request, id):  
    return render(request,'planning/editProgram.html', {'id': id})  
    
def destroy(request):  

    if(request.user.is_staff):

        if request.method == "POST":  

            profilage = Perfil.objects.get(idperfil=request.POST['id'])  
            profilage.delete()  
            # messages.info(request, '%s deleted successfully' %(profilage.deescripcion))
            return JsonResponse({})  
            
    else:

        return redirect('/') 

def destroyCompetence(request):  

    if(request.user.is_staff):

        if request.method == "POST":  

            competence = CompetenciasReq.objects.get(idcompetenciasreq=request.POST['id'])  
            competence.delete()  
            # messages.info(request, '%s deleted successfully' %(competence.desc_competencia))
            return JsonResponse({})  

    else:

        return redirect('/') 

def destroyCompetenceAdq(request):  

    if request.method == "POST":  

        competence = CompetenciasAdq.objects.get(idcompetencias_adq=request.POST['id'])  
        competence.delete()  
        # messages.info(request, 'Competence deleted successfully')
        return JsonResponse({})  

def validate_username(request):

    username = request.GET.get('deescripcion', None)
    id = request.GET.get('id', None)

    response = {
        'message': "This record already exists!" if Perfil.filtering(username.strip() if username else username, id if id.isdecimal() else None) else None
    }
    return JsonResponse(response)

    
def validate_competence(request):

    username = request.GET.get('desc_competencia', None)
    id = request.GET.get('id', None)
    # print(id)
    response = {
        'message': "This record already exists!" if CompetenciasReq.filtering(username.strip() if username else username, id if id.isdecimal() else None) else None
    }
    return JsonResponse(response)

    
def renderListasPublic(request):

    id = request.POST.get('id', None)
    tipo = request.POST.get('tipo', None)
    tipoHijo = request.POST.get('tipoHijo', None)
    tipoPadre = request.POST.get('tipoPadre', None)
    req = None

    if(not tipo):

        competence = CompetenciasReq.objects.all()

        for publico in CompetenciasAdq.objects.filter(fk_publico = id):
            
            competence = competence.exclude(idcompetenciasreq=publico.fk_competencia.idcompetenciasreq)

        html = render_to_string('planning/lista.html', {'lista': competence, 'defecto': "Select a competence" if len(competence) > 0 else "There is no more competences to add", 'tipo' : 'CompetenciasReq'})

    elif (tipo == 'Perfil'):

        competence = CompetenciasReq.objects.all()

        perfil = Perfil.objects.all()

        for publico in Perfil.objects.all():

            if(len(competence.filter(fk_perfil__idperfil=publico.idperfil))<=0):

                perfil = perfil.exclude(idperfil=publico.idperfil)
        
        html = render_to_string('planning/lista.html', {'lista': perfil, 'defecto': "Select a profile" if len(perfil) > 0 else 'There are no more profiles with competences asociated', 'tipo': 'Profile'})

        
    elif (tipo == 'Estructuraprograma'):

        if tipoPadre: 

            structuras=Estructuraprograma.objects.all()
            structuras=structuras.filter(fk_estructura_padre=tipoPadre)
            structuras=structuras.exclude(idestructuraprogrmas=tipoHijo)
            actividad = Estructuraprograma.objects.get(idestructuraprogrmas=tipoHijo)
            requisitos=cursos_prerequisitos.objects.filter(fk_estructura_programa=actividad)
            for x in requisitos:
                structuras=structuras.exclude(idestructuraprogrmas=x.fk_estructura_programa_pre.idestructuraprogrmas)

            if(structuras.first()): print(structuras.first().valor_elemento)
            html = render_to_string('planning/lista.html', {'lista': structuras, 'tipo': 'Estructuraprograma'})
            req = render_to_string('planning/lista.html', {'lista': requisitos, 'tipo': 'cursos_prerequisitos'})

        else:

            structuras=Estructuraprograma.objects.all()
            structuras=structuras.filter(fk_estructura_padre=tipoHijo)
            if(structuras.first()): print(structuras.first().valor_elemento)
            message = 'You can select a specific %s if you wish'%(structuras.first().valor_elemento,) if tipoHijo and structuras.first() else "Select a program"
            html = render_to_string('planning/lista.html', {'lista': structuras, 'defecto': message if len(structuras) > 0 else 'There are no more elements for this selection', 'tipo': 'Estructuraprograma'})

    response = {

        'competence': html,
        'requirements': req if req else None

    }

    return JsonResponse(response)



def renderCompetencesPublic(request):

    id = request.POST.get('id', None)
    idPublic = request.POST.get('idPublic', None)
    competence = CompetenciasReq.objects.all()
    competenceadq = CompetenciasAdq.objects.all()

    if(id and idPublic):

        competence = competence.filter(fk_perfil__idperfil=id) 
        competenceadq = competenceadq.filter(fk_publico__idpublico=idPublic) 
        lista = []
        
        for publico in competence:

            if not competenceadq:

                lista.append(False)

            elif(len(competenceadq.filter(fk_competencia__idcompetenciasreq=publico.idcompetenciasreq))<=0):

                lista.append(False)

            elif(publico.fk_nivel.tipo_elemento>competenceadq.get(fk_competencia__idcompetenciasreq=publico.idcompetenciasreq).fk_nivel.tipo_elemento):

                lista.append(False)
            
            else:
                
                lista.append(True)

    print(lista)
    aprovados = len(list(filter(lambda c: c, lista)))
    mensaje = 'You not need any training programa for the selected profile' if aprovados == len(lista) else 'You have approved %s competence%s of %s for the selected profile, you must select those failed competences and select a training program in order to master them'%(str(aprovados), '' if aprovados == 1 else 's', str(len(lista)))

    html = render_to_string('planning/lista.html', {'lista': competence, 'tipo' : 'Schedule', 'resultados': lista})

    response = {

        'competence': html,
        'titulo': mensaje
        # 'levels': lvl

    }

    return JsonResponse(response)


    
def renderListasCombos(request):

    clave = request.POST.get('clave', None)
    tipo = request.POST.get('tipo', None)
    print(tipo)
    
    if(tipo and clave and tipo == 'TablasConfiguracion'):

        lista = TablasConfiguracion.obtenerHijos('Rama' if clave == 'fk_rama' else 'NivelComp' if clave == 'fk_nivel' else 'Tipo Competencia' if clave == 'fk_tipo_competencia' else 'Duracion' if clave == 'fk_tipo_duracion' else '')

    if(tipo and clave and tipo == 'Perfil'):

        lista = Perfil.objects.all()

    if(tipo and clave and tipo == 'CompetenciasReq'):

        lista = CompetenciasReq.objects.all()

    if(tipo and clave and tipo == 'Publico'):

        lista = Publico.objects.all()

    if(tipo and clave and tipo == 'Estructuraprograma'):

        lista = Estructuraprograma.objects.all()

    html = render_to_string('planning/comboFiltro.html', {'lista': lista, 'tipo': tipo})

    response = {

        'lista': html

    }

    return JsonResponse(response)


    
def paginar(request):
    
    public = request.POST.get('id', None)
    tipo = request.POST.get('tipo', None)
    filtro = request.POST.get('filtro', None)
    orden = request.POST.get('orden', None)
    tipoOrden = request.POST.get('tipoOrden', "")

    if tipo and tipo == 'competencia':

        plan = CompetenciasReq.objects.all()

    elif tipo and tipo == 'competenciaadq':

        plan = CompetenciasAdq.objects.all()

        if not request.user.is_staff:
            
            plan = plan.filter(fk_publico = ExtensionUsuario.objects.get(user = request.user).Publico)

    elif tipo and tipo == 'Schedule':

        plan = Publico.objects.all()

    elif tipo and tipo == 'tablaSchedule':
        
        plan = MatriculaAlumnos.objects.filter(fk_publico__idpublico=public, origenSolicitud=MyMethod.ReturnCode("Planning"))

    elif tipo and tipo == 'Public':
        
        plan = ExtensionUsuario.objects.select_related().all()
        # extension = ExtensionUsuario.objects.select_related().all()
        # for ext in extension:
        #     if ext.CtaUsuario:
        #         print(ext.Publico.nombre)

    else:

        plan = Perfil.objects.all()

    if filtro:

        filtro = filtro.strip()

        if tipo and tipo == 'competencia':

            plan = plan.filter(Q(desc_competencia__icontains=filtro) | Q(fk_perfil__deescripcion__icontains=filtro) | Q(fk_tipo_competencia__desc_elemento__icontains=filtro) | Q(fk_nivel__desc_elemento__icontains=filtro))

        elif tipo and tipo == 'competenciaadq':

            plan = plan.filter(Q(periodo__icontains=filtro) | Q(experiencia__icontains=filtro) | Q(fk_publico__nombre__icontains=filtro) | Q(fk_competencia__desc_competencia__icontains=filtro) | Q(fk_nivel__desc_elemento__icontains=filtro) | Q(fk_tipo_duracion__desc_elemento__icontains=filtro))

        elif tipo and tipo == 'Schedule':
            
            plan = plan.filter(Q(nombre__icontains=filtro) | Q(apellido__icontains=filtro))

        elif tipo and tipo == 'Public':
            
            plan = plan.filter(Q(Publico__idpublico__icontains=filtro) | Q(Publico__nombre__icontains=filtro) | Q(Publico__apellido__icontains=filtro) | Q(CtaUsuario__fk_rol_usuario__desc_elemento__icontains=filtro) | Q(Publico__correos__icontains=filtro) | Q(Publico__telefonos__icontains=filtro) | Q(CtaUsuario__fk_status_cuenta__desc_elemento__icontains=filtro))
    
        else:

            plan = plan.filter(Q(deescripcion__icontains=filtro) | Q(desc_corta__icontains=filtro) | Q(fk_rama__desc_elemento__icontains=filtro))


    if(orden):

        plan = plan.order_by(tipoOrden + orden)



    # test = Perfil.objects.get(idperfil=55)
    # print(getattr(test, 'idperfil'))
    # # print(pagina)
    
    if(tipo and tipo == 'competencia'):
        
        pagina = render_to_string('planning/paginas.html', {'plan': paginas(request, plan)})
        tabla = render_to_string('planning/contenidoTabla.html', {'plan': paginas(request, plan), 'keys' : TITULOCOMPETENCIA, 'urlEdit': 'editCompetence', 'urlRemove': 'destroyCompetence', 'search':filtro, 'orden':orden, 'tipoOrden': tipoOrden})
        
    elif tipo and tipo == 'competenciaadq':

        pagina = render_to_string('planning/paginas.html', {'plan': paginas(request, plan)})
        tabla = render_to_string('planning/contenidoTabla.html', {'plan': paginas(request, plan), 'keys' : TITULOCOMPETENCIAADQ, 'urlEdit': 'editCompetenceAdq', 'urlRemove': 'destroyCompetenceAdq', 'search':filtro, 'orden':orden, 'tipoOrden': tipoOrden})

    elif tipo and tipo == 'Schedule':

        pagina = render_to_string('planning/paginas.html', {'plan': paginas(request, plan)})
        tabla = render_to_string('planning/contenidoTabla.html', {'plan': paginas(request, plan), 'keys' : TITULOPLAN, 'urlEdit': 'editProgram', 'urlRemove': 'destroyProgram', 'search':filtro, 'orden':orden, 'tipoOrden': tipoOrden, 'tipo': 'Schedule'})
   
    elif tipo and tipo == 'tablaSchedule':

        pagina = None
        tabla = render_to_string('planning/contenidoTabla.html', {'plan': plan, 'keys' : TITULOPLANES, 'tipo': tipo})

    elif tipo and tipo == 'Public':

        pagina = render_to_string('planning/paginas.html', {'plan': paginas(request, plan)})
        tabla = render_to_string('planning/contenidoTablaPublic.html', {'plan': paginas(request, plan), 'keys' : TITULOPUBLIC, 'urlEdit': 'unlockPublic', 'urlRemove': 'lockPublic', 'search':filtro, 'orden':orden, 'tipoOrden': tipoOrden, 'tipo': 'Public'})

    else:
        pagina = render_to_string('planning/paginas.html', {'plan': paginas(request, plan)})
        tabla = render_to_string('planning/contenidoTabla.html', {'plan': paginas(request, plan), 'keys' : TITULOPERFIL, 'urlEdit': 'editProfilage', 'urlRemove': 'destroyProfilage', 'search':filtro, 'orden':orden, 'tipoOrden': tipoOrden})
    # print(tabla)

    response = {
        'paginas': pagina,
        'contenido' : tabla
    }

    return JsonResponse(response)

def paginas(request, obj):


    page = request.GET.get('page', 1) if request.GET else request.POST.get('page', 1)
    # print(request.GET.get('page') if request.GET.get('page') else "nada get")
    # print(request.POST.get('page') if request.POST.get('page') else "nada post")

    paginator = Paginator(obj, 5)

    try:

        pages = paginator.page(page)
        # print(page)

    except PageNotAnInteger:
        # print("error 1")
        pages = paginator.page(1)

    except EmptyPage:
        # print("error 2")
        pages = paginator.page(paginator.num_pages)

    return pages








    # # structuraProg=Estructuraprograma.objects.filter(fk_estructura_padre=None)
    # structuras=Estructuraprograma.objects.all()

    # structuras=structuras.annotate(precio=F('prize__precio'), fechaIngreso=F('prize__fecha_registro'), id=F('prize__idprograma_precios'), descuento=F('prize__PorcentajeDescuento'), max=Max('prize__idprograma_precios'), amountDiscount=Max('prize__idprograma_precios')  ).filter(id=Max('prize__idprograma_precios')  )
    # structuras=structuras.filter(fk_estructura_padre=None)
    # tipoPrograma=TablasConfiguracion.obtenerHijos("Tipo matricula")
    # estatus=TablasConfiguracion.obtenerHijos("EstMatricula")


    # return render(request, 'components/modalAddMatricula.html',{'structuraProg':structuras, 'tipoPrograma':tipoPrograma, 'status':estatus})

    
def saveProgram(request):  

    if request.method == "POST":  

        try:

            publico=request.POST.get('idPublico')
            idEstruct=request.POST.get('idEstructura')
            perfil=request.POST.get('idPerfil')
            fecha=request.POST.get('fecha')

            publico=Publico.objects.get(idpublico=publico)

            struct=Estructuraprograma.objects.get(idestructuraprogrmas=idEstruct)
            print(struct.descripcion)
            statusDB=TablasConfiguracion.objects.get(valor_elemento='EstatusRevision')
            


            
            matricula=MatriculaAlumnos.objects.create(fk_publico=publico,fk_estruc_programa=struct, fecha_matricula=fecha, fk_tipo_matricula=None ,fk_status_matricula=statusDB,fecha_aprobada=None, origenSolicitud = MyMethod.ReturnCode('Planning'))
            matricula.save()
            messages.info(request, 'Training Program Added Successfully')
            return JsonResponse({"mensaje" : "exito"})

        except:

            return JsonResponse({"mensaje" : "Error, try again later"})



def managePublic(request):

    search_query = request.GET.get('search_box', "")
    program = ExtensionUsuario.objects.select_related().all()
    return render(request,"planning/managePublic.html",{'plan': paginas(request, program), 'keys' : TITULOPUBLIC, 'urlEdit': 'unlockPublic', 'urlRemove': 'lockPublic', 'search':search_query, 'tipo':'Public', 'segment':'settings'}) 

    
def lockPublic(request):

    if request.method == "POST":  

        try:

            id=request.POST.get('id')

            ctauser = CtaUsuario.objects.filter(idcta_usuario=ExtensionUsuario.objects.get(Publico=Publico.objects.get(idpublico=id)).CtaUsuario.idcta_usuario)


            ctauser.update(fk_status_cuenta= TablasConfiguracion.objects.get(valor_elemento='status_locked').id_tabla)

            messages.info(request, 'Public Locked Successfully')
            return JsonResponse({"mensaje" : "exito"})

        except:

            return JsonResponse({"mensaje" : "Error, try again later"})

    
def unlockPublic(request):

    code = str(Methods.getVerificationLink(request.user.email, 1))

    if request.method == "POST":  

        try:

            id=request.POST.get('id')

            ctauser = CtaUsuario.objects.filter(idcta_usuario=ExtensionUsuario.objects.get(Publico=Publico.objects.get(idpublico=id)).CtaUsuario.idcta_usuario)


            ctauser.update(fk_status_cuenta= TablasConfiguracion.objects.get(valor_elemento='status_active').id_tabla)

            messages.info(request, 'Public Unlocked Successfully')
            return JsonResponse({"mensaje" : "exito"})

        except:

            return JsonResponse({"mensaje" : "Error, try again later"})

   
def modalForm(request):
    print(request.user.id)
    id = request.POST.get('idModal')
    tipo = request.POST.get('tipoModal')

    if tipo == 'profile':

        profilage = Perfil.objects.get(idperfil=id) if id else None
        form = perfilForm(instance=profilage)
        html = render_to_string('planning/formularios.html', {'form': form}, request=request)

    elif tipo == 'competence':

        profilage = CompetenciasReq.objects.get(idcompetenciasreq=id) if id else None
        form = competenciaForm(instance=profilage)
        html = render_to_string('planning/formularios.html', {'form': form}, request=request)

    else:

        profilage = CompetenciasAdq.objects.get(idcompetencias_adq=id) if id else None
        form = competenciaAdqForm(instance=profilage)
        competencias = CompetenciasReq.objects.all()
        publicos = Publico.objects.all()
        publicos = publicos.filter(idpublico=ExtensionUsuario.objects.get(user = request.user).Publico.idpublico) if not request.user.is_staff else publicos.filter(idpublico=ExtensionUsuario.objects.get(Publico = CompetenciasAdq.objects.get(idcompetencias_adq=id).fk_publico).Publico.idpublico) if id else publicos
        
        if(publicos and len(publicos)==1):

            form.fields['fk_publico'].queryset = publicos
            form.fields['fk_publico'].initial = publicos[0].idpublico

            if not id:

                for publico in CompetenciasAdq.objects.filter(fk_publico = publicos[0].idpublico):
                    
                    competencias = competencias.exclude(idcompetenciasreq=publico.fk_competencia.idcompetenciasreq)

            else:

                competencias = competencias.filter(idcompetenciasreq=CompetenciasAdq.objects.get(idcompetencias_adq=id).fk_competencia.idcompetenciasreq)

            if competencias:

                form.fields['fk_competencia'].queryset = competencias
                if id: form.fields['fk_competencia'].initial = competencias[0].idcompetenciasreq

        html = render_to_string('planning/formularios.html', {'form': form}, request=request)

    return JsonResponse({'formulario':html, 'nombre': profilage.deescripcion if profilage and tipo == 'profile' else profilage.desc_competencia if profilage and tipo == 'competence' else None}) 


def createProfile(request):  

    print('entro')
    id = request.POST.get('idEdit')
    profilage = Perfil.objects.get(idperfil=id) if id else None

    if request.method == "POST":  

        form = perfilForm(data = request.POST, instance=profilage) 

        if form.is_valid():  

            form.save()  
            print('guardado')
            return JsonResponse({})

        else:
            print('error')
            return JsonResponse({'mensaje': 'error'})

    print('no entro')
    return JsonResponse({}) 


def createCompetence(request):  

    print('entro')
    id = request.POST.get('idEdit')
    profilage = CompetenciasReq.objects.get(idcompetenciasreq=id) if id else None

    if request.method == "POST":  

        form = competenciaForm(data = request.POST, instance=profilage) 

        if form.is_valid():  

            form.save()  
            print('guardado')
            return JsonResponse({})

        else:
            print('error')
            return JsonResponse({'mensaje': 'error'})

    print('no entro')
    return JsonResponse({}) 

def createCompetenceAdq(request):  

    print('entro')
    id = request.POST.get('idEdit')
    profilage = CompetenciasAdq.objects.get(idcompetencias_adq=id) if id else None

    if request.method == "POST":  

        form = competenciaAdqForm(data = request.POST, instance=profilage) 

        if form.is_valid():  

            form.save()  
            print('guardado')
            return JsonResponse({})

        else:
            print('error')
            return JsonResponse({'mensaje': 'error'})

    print('no entro')
    return JsonResponse({}) 

    
def preRequirements(request):  

    return render(request,"planning/prerequisitos.html") 
    


def requirements(request):  


    if request.method == "POST":  
        
        tipo = request.POST.get('tipo')
        requisito = Estructuraprograma.objects.get(idestructuraprogrmas=request.POST.get('requisito'))
        actividad = Estructuraprograma.objects.get(idestructuraprogrmas=request.POST.get('actividad'))

        if tipo == 'agregar':
            matricula=cursos_prerequisitos.objects.create(fk_estructura_programa=actividad,fk_estructura_programa_pre=requisito)
            matricula.save()

        else:
            matricula = cursos_prerequisitos.objects.get(fk_estructura_programa=actividad,fk_estructura_programa_pre=requisito)  
            matricula.delete()  

        return JsonResponse({'mensaje': 'succes'})

    return JsonResponse({}) 
