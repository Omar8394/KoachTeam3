from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest,JsonResponse
from django.template.loader import get_template
from ..app.models import TablasConfiguracion,PreguntasFrecuentes
from .forms import preguntasfrecuentes
from django.contrib.auth.decorators import login_required

from ..security import Methods
from ..security.models import LandPage
from django.db.models import Q
from ..communication.Methods import create_mail, send_mail
from django.template.loader import get_template
from django.template import loader
from ..security.forms import SignUpForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from core import settings
import json

# Create your views here.


def helpSecurity(request):
    context = {}
    context['segment'] = 'help'
    context['subsegment'] = 'help'

    return render(request,'help/myhelp.html', context)

def myHelp(request):
    context = {}
    context['segment'] = 'help'

    return render(request,'help/myhelp.html', context)
@login_required(login_url="/login/")   
def save_Q (request): 
 if(request.user.is_staff): 
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
 else:
        
        return redirect('/')   

def showhelps(request): 
 if(request.user.is_staff):    
    queryset=request.GET.get("buscar")

    if queryset:
        form =PreguntasFrecuentes.objects.select_related("fk_tipo_pregunta_frecuente").filter(fk_tipo_pregunta_frecuente_id__desc_elemento__icontains= queryset)
        print(form)
        
       
        return render(request,"help/mostrarayudas.html",{'form':form})
           
          
    else:
        return render(request,"help/mostrarayudas.html")
 else:
        
        return redirect('/') 
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
    return redirect('/help_app/ver/')
@login_required(login_url="/login/")
def show_questions(request):
     
     form =TablasConfiguracion.obtenerHijos("Frecuente")
     return render(request,'help/showquestionsusers.html',{'form':form}) 
def questionask(request,id):
    
     
     form = PreguntasFrecuentes.objects.filter(fk_tipo_pregunta_frecuente_id=id).all 
     print(form)
     return render(request,'help/showanswers.html',{'form': form})


#@login_required(login_url="/login/")
#def landingshow(request):
#    if request.user.is_superuser:
#        queryset = request.GET.get("buscar")
#        form = LandPage.objects.all()
#        if queryset:
#            form = LandPage.objects.filter(
 #               Q(nombre__icontains=queryset) |
 #               Q(apellido__icontains=queryset) |
  #              Q(correos__icontains=queryset)
   #         ).distinct()
    #        print(form)

     #       return render(request, "help/landpageaprobar.html", {'form': form})


      #  else:
       #     return render(request, "help/landpageaprobar.html")
   # else:

    #    return redirect('/')

@login_required(login_url="/login/")   
def landingshow (request): 
#  if(request.user.is_superuser):  
#     queryset=request.GET.get("buscar")
#     form =LandPage.objects.all()
#     if queryset:
#         form =LandPage.objects.filter(
#           Q(nombre__icontains=queryset) |
#           Q(apellido__icontains=queryset) |
#           Q(correos__icontains=queryset)
#         ).distinct()
#         print(form)
        
       
#         return render(request,"help/landpageaprobar.html",{'form':form})
           
          
#     else:
#         return render(request,"help/landpageaprobar.html")
#  else:
        
#         return redirect('/') 
 if(request.user.is_superuser):  
   form =LandPage.objects.filter(status_solicitud=0).order_by('-fecha_solicitud')
     
   return render(request,"help/landpageaprobar.html",{'form':form})
   
 else:
        
    return redirect('/') 

# def sending(request):
#     if request.method == "POST":
#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             modelo = {}
#             context = {}
#             if request.body:
#                 context = {}
#                 data = json.load(request)

#                 if data["id"]:
#                     form = LandPage.objects.filter(id_solicitud=data["id"])
#                     helps = LandPage.objects.filter(id_solicitud=data["id"])
#                     for obj in helps:
#                         obj.status_solicitud = 1
#                         obj.save()
#                     print(helps)

#                     context = {"form": form}

#                     html_template = (loader.get_template('help/modalmail.html'))

#                     return HttpResponse(html_template.render(context, request))


#                 elif data["data"]:
#                     email = data["data"]["email"]
#                     landpage = LandPage.objects.get(pk=data["id"])
#                     code = str(Methods.getVerificationLink(None, email, 2))
#                     enlace = request.get_raw_uri().split("//")[0] + "//" + \
#                              request.get_host() + "/register_new/" + code + "/" + "landpage/" \
#                              + str(landpage.id_solicitud) + "/"
#                     context = {"titulo": "Account Registration Link",
#                                "user": landpage.nombre + " " + landpage.apellido,
#                                "content": "Thank you for joining the energy solar team, follow the link below to register  your account:",
#                                "enlace": enlace, "enlaceTexto": "click here!", "empresa": settings.EMPRESA_NOMBRE,
#                                "urlimage": settings.EMPRESA_URL_LOGO}
#                     send_mail(
#                         create_mail(email, "Account Registration Link", "security/base_email_template_pro.html",
#                                     context))

#                     return JsonResponse({"message": "Perfect"})

#                 else:

#                     context = {}
#                     html_template = (loader.get_template('help/modalmail.html'))

#                     return HttpResponse(html_template.render(context, request))

 
def sending(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                modelo = {}
                context = {}
                if request.body:
                    context={}
                    data = json.load(request)
                    
                    
                   
                    if data["correo"] == "find":
                     form =LandPage.objects.filter(id_solicitud=data["id"])
                     for obj in form:
                      mail= obj.correos
                      

                      context={"form":form,'correos': json.loads(mail)['emailPrincipal'] if 'emailPrincipal' in json.loads(mail) else None}
                      print(context)
                      html_template = (loader.get_template('help/modalmail.html')) 
        
                      return HttpResponse(html_template.render(context, request))
                    

                    elif data["correo"] == "send":
                      email = data["data"]["email"]
                     
                      print(email)
                     
                      landpage = LandPage.objects.get(pk=data["id"])
                      code = str(Methods.getVerificationLink(None,email, 2))
                     
                      print(code)
                      enlace = request.get_raw_uri().split("//")[0] + "//" + \
                               request.get_host() + "/register_new/" + code + "/" + "landpage/" \
                               + str(landpage.id_solicitud) + "/"
                      context = {"titulo": "Account Registration Link",
                                 "user": landpage.nombre + " " + landpage.apellido,
                                 "content": "Thank you for joining the energy solar team, follow the link below to register  your account:",
                                 "enlace": enlace, "enlaceTexto": "click here!", "empresa": settings.EMPRESA_NOMBRE,"urlimage":settings.EMPRESA_URL_LOGO}
                      print(context)
                      send_mail(
                      create_mail(email, "Account Registration Link", "security/base_email_template_pro.html",
                                    context))
                      helps=LandPage.objects.filter(id_solicitud=data["id"])
                      for obj in helps:
                          obj.status_solicitud = 1
                          obj.save()
                          print(helps)
                          return JsonResponse({"message":"Perfect"})
                        
                    else:
                        context={}
                        html_template = (loader.get_template('help/modalmail.html')) 
        
                        return HttpResponse(html_template.render(context, request))