# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm, ResetPasswordForm, LandingPage
from modules.app.models import TablasConfiguracion

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    

    return render(request, "security/login.html", {"form": form, "msg" : msg})

def register_user(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg     = 'User created - please <a href="/login">login</a>.'
            success = True
            
            #return redirect("/login/")

        else:
            msg = 'Form is not valid'    
    else:
        form = SignUpForm()

    return render(request, "security/register.html", {"form": form, "msg" : msg, "success" : success })

def forgot_password(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")

            msg     = 'Password reset email sent! - please check your email inbox'
            success = True
            
            #return redirect("/login/")
        else:
            msg = 'Form is not valid'    
    else:
        form = ResetPasswordForm()

    return render(request, "security/passwordReset.html", {"form": form, "msg" : msg, "success" : success })

def lang_page(request):
    form = LandingPage(request.POST or None)
    msg = None
    success = False
    tipo_telefono = None
    if request.method == "POST":
            if form.is_valid():
                print(form)
                form.save()
                success = True
                msg = "tu solicitud ha sido enviada."
            else:
                print(form)
                tipo_telefono = TablasConfiguracion.obtenerHijos("tipTelefono")
                msg = 'Error validating the form'
    else:
        tipo_telefono = TablasConfiguracion.obtenerHijos("tipTelefono")
        form = LandingPage()
        print("tipo Telefono:", tipo_telefono)

    return render(request, "security/landPage.html", {"form": form, "msg": msg, 'success': success,
                                                      "tipoTelefono": tipo_telefono})
