from django.shortcuts import render, redirect
#from .forms import competenciaForm, perfilForm
#from .models import Perfil, CompetenciasReq
from django.http import HttpResponse, HttpRequest
from django.template.loader import get_template
import json
# Create your views here.



def helpSecurity(request):

    return render(request,'help/myhelp.htm')





