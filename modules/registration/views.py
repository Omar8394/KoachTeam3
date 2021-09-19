from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django import template
from django.template import loader
from modules.registration import forms
from modules.app.models import Estructuraprograma
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

    if request.method == "POST":
     
        if form.is_valid():
          forms.save()
           
        else:    
                msg = 'Invalid Data'    
            
    context = {}
   # context['segment'] = 'index'

    html_template = loader.get_template( 'registration/Matriculacion.html' )

    #return HttpResponse(html_template.render(context, request))
    return render(request, 'registration/Matriculacion.html', {"form": form, "msg" : msg,'structuraProg':structuraProg})

