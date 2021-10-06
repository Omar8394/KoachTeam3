from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.template.loader import get_template
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



