from django.contrib.auth.models import User
from django.shortcuts import render, redirect  
from .forms import competenciaAdqForm, competenciaForm, perfilForm, programForm
from .models import CompetenciasAdq, Perfil, CompetenciasReq
from ..app.models import TablasConfiguracion, Programascap, Publico
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def emp(request):  
    if request.method == "POST":  
        form = perfilForm(request.POST)
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/planning/show/')  
            except:  
                pass  
    else:  
        form = perfilForm()  
    # print(type(form.fields["fk_rama"].choices))
    # for x in form.fields["fk_rama"].choices:
    #     print(x)
    # print("hola")
    return render(request,'planning/add.html',{'form':form})
    
def paginas(request, obj):
    page = request.GET.get('page', 1)

    paginator = Paginator(obj, 5)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return pages

def show(request):  

    search_query = request.GET.get('search_box', "")
    plan = Perfil.objects.all()
    # print(plan.__class__.__name__)
    context = {}
    context['segment'] = 'planning'

    if(search_query):

        plan = plan.filter(deescripcion__startswith=search_query) 

    return render(request,"planning/show.html",{'plan':paginas(request, plan), 'search':search_query}, context) 

def showCompetences(request):  
    search_query = request.GET.get('search_box', "")
    competencia = CompetenciasReq.objects.all()  
    context = {}
    context['segment'] = 'planning'

    if(search_query):
        competencia = competencia.filter(desc_competencia__startswith=search_query) 

    return render(request,"planning/showCompetence.html",{'competencia':paginas(request, competencia), 'search':search_query}, context) 

def showCompetencesAdq(request):  
    search_query = request.GET.get('search_box', "")
    context = {}
    context['segment'] = 'planning'

    if not request.user.is_staff:
        competencia = CompetenciasAdq.objects.filter(fk_publico= Publico.objects.get(user = request.user))
    else:
        competencia = CompetenciasAdq.objects.all()  

    if(search_query):

        competencia = competencia.filter(periodo__startswith=search_query) 

    return render(request,"planning/showCompetenceAdq.html",{'competencia':paginas(request, competencia), 'search':search_query}, context) 

def showProgram(request):  
    program = Programascap.objects.all()  
    context = {}
    context['segment'] = 'planning'
    return render(request,"planning/showProgram.html",{'programs':program}, context) 

def addCompetence(request):  
    if request.method == "POST":  
        form = competenciaForm(request.POST, )
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/planning/showCompetence/')  
            except:  
                pass  
    else:  
        form = competenciaForm()  
    return render(request,'planning/addCompetence.html',{'form':form})

def addCompetenceAdq(request):  
    if request.method == "POST":  
        form = competenciaAdqForm(request.POST)
        if form.is_valid():  
            try:  
                print("valid")
                form.save()  
                return redirect('/planning/showCompetenceAdq/')  
            except:  
                print("error")
                print(form.errors)
                pass  
        else:
            print(form.errors)
            print(request.POST)

    elif not request.user.is_staff:
        publico=Publico.objects.filter(user=request.user)
        form = competenciaAdqForm()
        form.fields['fk_publico'].queryset = publico
    else:  
        form = competenciaAdqForm()  
    return render(request,'planning/addCompetenceAdq.html',{'form':form})

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

def edit(request, id):  
    
    profilage = Perfil.objects.get(idperfil=id) 
    if request.method == "POST":  
        # print("update")
        form = perfilForm(request.POST, instance = profilage)  
        if form.is_valid():  
            form.save()  
            return redirect('/planning/show/')  
    tabla = TablasConfiguracion.objects.filter(id_tabla=1)
    # print(profilage.fk_rama)
    # print("hola edit")
    # form = perfilForm(initial={'deescripcion': profilage.deescripcion, 'desc_corta' : profilage.desc_corta, 'fk_rama' : profilage.fk_rama})
    form = perfilForm(instance=profilage)
    # form.fields['fk_rama'].queryset = TablasConfiguracion.objects.filter(id_tabla=TablasConfiguracion.objects.get(valor_elemento="Padre").id_tabla)
    return render(request,'planning/edit.html', {'form':form}) 
    
def editCompetence(request, id):  
    competence = CompetenciasReq.objects.get(idcompetenciasreq=id) 
    # print(competence)
    if request.method == "POST":  
        # print("update")
        form = competenciaForm(request.POST, instance = competence)  
        if form.is_valid():  
            form.save()  
            return redirect('/planning/showCompetence/')  

    # print("hola edit")
    # form = perfilForm(initial={'deescripcion': profilage.deescripcion, 'desc_corta' : profilage.desc_corta, 'fk_rama' : profilage.fk_rama})
    form = competenciaForm(instance=competence)
    return render(request,'planning/editCompetence.html', {'form':form})  

def editCompetenceAdq(request, id):  
    competence = CompetenciasAdq.objects.get(idcompetencias_adq=id) 
    if request.method == "POST":  
        # print("update")
        form = competenciaAdqForm(request.POST, instance = competence)  
        if form.is_valid():  
            form.save()  
            return redirect('/planning/showCompetenceAdq/')  

    # print("hola edit")
    # form = perfilForm(initial={'deescripcion': profilage.deescripcion, 'desc_corta' : profilage.desc_corta, 'fk_rama' : profilage.fk_rama})
    elif not request.user.is_staff:
        publico=Publico.objects.filter(user=request.user)
        form = competenciaAdqForm(instance=competence)
        form.fields['fk_publico'].queryset = publico
    else:
        form = competenciaAdqForm(instance=competence)
    return render(request,'planning/editCompetenceAdq.html', {'form':form})  

def editProgram(request, id):  
    program = Programascap.objects.get(idprogramascap=id) 
    if request.method == "POST":  
        # print("update")
        form = programForm(request.POST, instance = program)  
        if form.is_valid():  
            form.save()  
            return redirect('/planning/showProgram/')  

    # print("hola edit")
    # form = perfilForm(initial={'deescripcion': profilage.deescripcion, 'desc_corta' : profilage.desc_corta, 'fk_rama' : profilage.fk_rama})
    form = programForm(instance=program)
    return render(request,'planning/editProgram.html', {'form':form})  
    
# def update(request, id):  
#     employee = Perfil.objects.get(id=id)  
#     form = perfilForm(request.POST, instance = employee)  
#     if form.is_valid():  
#         form.save()  
#         return redirect("/show")  
#     return render(request, 'edit.html', {'employee': employee})  

def destroy(request, id):  
    profilage = Perfil.objects.get(idperfil=id)  
    profilage.delete()  
    return redirect('/planning/show/') 

def destroyCompetence(request, id):  
    competence = CompetenciasReq.objects.get(idcompetenciasreq=id)  
    competence.delete()  
    return redirect('/planning/showCompetence/') 

def destroyCompetenceAdq(request, id):  
    competence = CompetenciasAdq.objects.get(idcompetencias_adq=id)  
    competence.delete()  
    return redirect('/planning/showCompetenceAdq/') 

def destroyProgram(request, id):  
    program = Programascap.objects.get(idprogramascap=id)  
    program.delete()  
    return redirect('/planning/showProgram/') 