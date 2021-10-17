from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.template.loader import get_template
from ..app.models import TablasConfiguracion,PreguntasFrecuentes
from .forms import preguntasfrecuentes
import json
# Create your views here.


def helpSecurity(request):
    context = {}
    context['segment'] = 'help'

    return render(request,'help/myhelp.html', context)

def myHelp(request):
    context = {}
    context['segment'] = 'help'

    return render(request,'help/myhelp.html', context)
def save_Q (request): 
   
     if request.method == "POST":  
        form = preguntasfrecuentes(request.POST)
        if form.is_valid():  
            try:  
                form.save() 
                form=preguntasfrecuentes()
                return render(request,'help/save.html',{'form':form}) 
            except:  
                pass 
         
            
     else:  
        form = preguntasfrecuentes()  
     return render(request,'help/save.html',{'form':form})

def showhelps(request):  
    queryset=request.GET.get("buscar")

    if queryset:
        form =PreguntasFrecuentes.objects.select_related("fk_tipo_pregunta_frecuente").filter(fk_tipo_pregunta_frecuente_id__desc_elemento__icontains= queryset)
        print(form)
        
       
        return render(request,"help/mostrarayudas.html",{'form':form})
           
          
    else:
        return render(request,"help/mostrarayudas.html")
def helpsedit(request,id):
    
    helps=PreguntasFrecuentes.objects.get(idpregunta_frecuente=id)
    if request.method=="POST":
     form=preguntasfrecuentes(request.POST, instance=helps)
     print(form)
     if form.is_valid():  
            form.save() 
            form=preguntasfrecuentes()
            
            return redirect('/help_app/ver/')
    
    form = preguntasfrecuentes(instance=helps)
    return render(request,'help/save.html', {'form':form})

def helpsdelete(request,id):
    helps=PreguntasFrecuentes.objects.get(idpregunta_frecuente=id)
    helps.delete()  
    return redirect('/help_app/Questions/')
 
def show_questions(request):
     
     form =TablasConfiguracion.obtenerHijos("Frecuente")
     return render(request,'help/showquestionsusers.html',{'form':form}) 
   

          

def questionask(request,id):
    
     
     form = PreguntasFrecuentes.objects.filter(fk_tipo_pregunta_frecuente_id=id).all 
     print(form)
     return render(request,'help/showanswers.html',{'form': form}) 
     







