from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect  
from .forms import competenciaAdqForm, competenciaForm, perfilForm, programForm
from .models import CompetenciasAdq, Perfil, CompetenciasReq
from ..app.models import PublicoRelacion, TablasConfiguracion, Programascap, Publico
from json import dumps
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.template.defaulttags import register
# Create your views here.
TITULOPERFIL = {'idperfil': '#', 'deescripcion': 'Name', 'desc_corta': 'Description', 'fk_rama': 'Branch'}
TITULOCOMPETENCIA = {'idcompetenciasreq': '#', 'desc_competencia': 'Name', 'fk_perfil': 'Profile', 'fk_tipo_competencia': 'Type', 'fk_nivel': 'Minimum Level'}
TITULOCOMPETENCIAADQ = {'idcompetencias_adq': '#', 'fk_publico': 'Public', 'periodo': 'Period', 'experiencia': 'Experience', 'fk_tipo_duracion': 'Duration', 'fk_competencia': 'Competence', 'fk_nivel': 'Level'}

@register.filter
def get_attr(dictionary, key):
    return getattr(dictionary, key)

def editCompetenceAdq(request, id = None):  

    competence = CompetenciasAdq.objects.get(idcompetencias_adq=id) if id else None

    if request.method == "POST":  

        form = competenciaAdqForm(data = request.POST, instance = competence) 

        if form.is_valid():  

            form.save()  

            if id:

                messages.info(request, 'Changes applied successfully')
                
            else:
                
                messages.info(request, 'Competence Added Succefuly')

            return redirect('/planning/showCompetenceAdq/') 

        else:
            
            messages.warning(request, 'An error has occurred!')
            return render(request,'planning/editCompetenceAdq.html',{'form':form})

    form = competenciaAdqForm(instance=competence)

    competencias = CompetenciasReq.objects.all()
    publicos = Publico.objects.all()
    publicos = publicos.filter(user=request.user) if not request.user.is_staff else publicos.filter(user=Publico.objects.get(idpublico=CompetenciasAdq.objects.get(idcompetencias_adq=id).fk_publico.idpublico).user) if id else publicos
    
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
        
        else:
            print("mensaje")
            messages.error(request, 'There are no more competences to include')
            
            return redirect('/planning/showCompetenceAdq/') 

    return render(request,'planning/editCompetenceAdq.html', {'form':form, 'id':id})  

def editCompetence(request, id = None):  

    if(request.user.is_staff):

        competence = CompetenciasReq.objects.get(idcompetenciasreq=id) if id else None

        if request.method == "POST":  

            form = competenciaForm(property_id = id, data = request.POST, instance = competence)  

            if form.is_valid():  

                form.save()  

                if id:

                    messages.info(request, 'Changes applied to %s successfully' %(form.data['desc_competencia']))
                    
                else:
                    
                    messages.info(request, 'Competence Named %s Added Succefuly ' %(form.data['desc_competencia']))

                return redirect('/planning/showCompetence/') 

            else:

                messages.warning(request, 'An error has occurred!')
                return render(request,'planning/editCompetence.html',{'form':form})

        # print(id)
        form = competenciaForm(instance=competence)
        return render(request,'planning/editCompetence.html', {'form':form, 'id':id}) 
    
    else:

        return redirect('/') 

def edit(request, id=None):  

    if(request.user.is_staff):
        
        profilage = Perfil.objects.get(idperfil=id) if id else None

        if request.method == "POST":  

            form = perfilForm(property_id = id, data = request.POST, instance = profilage) 

            if form.is_valid():  

                form.save()  

                if id:

                    messages.info(request, 'Changes applied to %s successfully' %(form.data['deescripcion']))

                else:
                    
                    messages.info(request, 'Profile Named %s Added Succefuly ' %(form.data['deescripcion']))

                return redirect('/planning/show/')  

            else:

                messages.warning(request, 'An error has occurred!')
                return render(request,'planning/edit.html',{'form':form})

        form = perfilForm(instance=profilage)
        return render(request,'planning/edit.html', {'form':form, 'id':id}) 

    else:

        return redirect('/') 
    
def show(request):  

    # if(request.user.is_staff):
        
        search_query = request.GET.get('search_box', "")
        plan = Perfil.objects.all()

        if(search_query):

            plan = plan.filter(deescripcion__startswith=search_query) 

        return render(request,"planning/show.html",{'plan':paginas(request, plan), 'keys' : TITULOPERFIL, 'urlEdit': 'editProfilage', 'urlRemove': 'destroyProfilage', 'search':search_query}) 
    
    # else:
        
    #     return redirect('/') 


def showCompetences(request): 

    # if(request.user.is_staff):

        search_query = request.GET.get('search_box', "")
        competencia = CompetenciasReq.objects.all()  
        pagina = paginas(request, competencia)
        print(pagina)
        if(search_query):

            competencia = competencia.filter(desc_competencia__startswith=search_query) 

        return render(request,"planning/showCompetence.html",{'plan': paginas(request, competencia), 'keys' : TITULOCOMPETENCIA, 'urlEdit': 'editCompetence', 'urlRemove': 'destroyCompetence', 'search':search_query}) 
    
    # else:

    #     return redirect('/') 

def showCompetencesAdq(request):  

    search_query = request.GET.get('search_box', "")
    competencia = CompetenciasAdq.objects.all()

    if not request.user.is_staff:

        competencia = competencia.filter(fk_publico__user = request.user)

    if(search_query and request.user.is_staff):

        competencia = competencia.filter(fk_publico__nombre__startswith=search_query) 

    return render(request,"planning/showCompetenceAdq.html",{'plan': paginas(request, competencia), 'keys' : TITULOCOMPETENCIAADQ, 'urlEdit': 'editCompetenceAdq', 'urlRemove': 'destroyCompetenceAdq', 'search':search_query, 'segment':'planning'}) 

def showProgram(request): 
     
    program = Programascap.objects.all()  
    return render(request,"planning/showProgram.html",{'programs':program, 'segment':'planning'}) 

def addProgram(request):  
    if request.method == "POST":  
        form = programForm(request.POST)
        if form.is_valid():  
            try:  
                # print("valid")
                form.save()  
                return redirect('/planning/showProgram/')  
            except:  
                pass  
        # else:
        #     print("no valid")

    else:  
        form = programForm()  
    
    return render(request,'planning/addProgram.html',{'form':form})
     


def editProgram(request, id):  

    program = Programascap.objects.get(idprogramascap=id) 

    if request.method == "POST":  

        form = programForm(request.POST, instance = program)  

        if form.is_valid():  

            form.save()  
            return redirect('/planning/showProgram/')  

    form = programForm(instance=program)
    return render(request,'planning/editProgram.html', {'form':form})  
    
def destroy(request):  

    if(request.user.is_staff):

        if request.method == "POST":  

            profilage = Perfil.objects.get(idperfil=request.POST['id'])  
            profilage.delete()  
            messages.info(request, '%s deleted successfully' %(profilage.deescripcion))
            return JsonResponse({})  
            
    else:

        return redirect('/') 

def destroyCompetence(request):  

    if(request.user.is_staff):

        if request.method == "POST":  

            competence = CompetenciasReq.objects.get(idcompetenciasreq=request.POST['id'])  
            competence.delete()  
            messages.info(request, '%s deleted successfully' %(competence.desc_competencia))
            return JsonResponse({})  

    else:

        return redirect('/') 

def destroyCompetenceAdq(request):  

    if request.method == "POST":  

        competence = CompetenciasAdq.objects.get(idcompetencias_adq=request.POST['id'])  
        competence.delete()  
        messages.info(request, 'Competence deleted successfully')
        return JsonResponse({})  

def destroyProgram(request, id):  

    program = Programascap.objects.get(idprogramascap=id)  
    program.delete()  
    return redirect('/planning/showProgram/') 

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

    id = request.GET.get('id', None)
    competence = CompetenciasReq.objects.all()

    for publico in CompetenciasAdq.objects.filter(fk_publico = id):
        
        competence = competence.exclude(idcompetenciasreq=publico.fk_competencia.idcompetenciasreq)

    niveles = TablasConfiguracion.obtenerHijos("NivelComp")
    html = render_to_string('planning/lista.html', {'lista': competence, 'defecto': "Select a competence" if len(competence) > 0 else "There is no more competences to add", 'tipo' : 'CompetenciasReq'})
    lvl = render_to_string('planning/lista.html', {'lista': niveles, 'defecto': "Skill level" if len(niveles) > 0 else "There is no more levels to add", 'tipo' : 'NivelComp'})

    response = {

        'competence': html,
        'levels': lvl

    }

    return JsonResponse(response)
    
def paginar(request):
    
    tipo = request.POST.get('tipo', None)
    filtro = request.POST.get('filtro', None)
    orden = request.POST.get('orden', None)
    tipoOrden = request.POST.get('tipoOrden', "")

    if tipo and tipo == 'competencia':

        plan = CompetenciasReq.objects.all()

    elif tipo and tipo == 'competenciaadq':

        plan = CompetenciasAdq.objects.all()

    else:

        plan = Perfil.objects.all()


    if filtro:

        filtro = filtro.strip()

        if tipo and tipo == 'competencia':

            plan = plan.filter(desc_competencia__startswith=filtro).order_by('desc_competencia')

        elif tipo and tipo == 'competenciaadq':

            plan = plan.filter(fk_publico__nombre__startswith=filtro).order_by('fk_publico__nombre')

        else:

            plan = plan.filter(deescripcion__startswith=filtro).order_by('deescripcion')


    if(orden):
        # print(tipoOrden + orden)
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

    else:

        pagina = render_to_string('planning/paginas.html', {'plan': paginas(request, plan)})
        tabla = render_to_string('planning/contenidoTabla.html', {'plan': paginas(request, plan), 'keys' : TITULOPERFIL, 'urlEdit': 'editProfilage', 'urlRemove': 'destroyProfilage', 'search':filtro, 'orden':orden, 'tipoOrden': tipoOrden })
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
