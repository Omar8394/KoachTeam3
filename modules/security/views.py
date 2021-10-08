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
from .forms import LoginForm, SignUpForm, ResetPasswordForm, LandingPage, FullRegistration
from modules.app.models import TablasConfiguracion
from modules.security.models import CtaUsuario
from modules.security import Methods
from ..communication.Methods import create_mail, send_mail


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        form = LoginForm(request.POST or None)

        msg = None

        if request.method == "POST":

            if form.is_valid():
                # tools = Methods.securityTools()
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                # cuenta = CtaUsuario.objects.filter(codigo_cta=username)[0]
                # cuenta = CtaUsuario.objects.get(cuenta.idcta_usuario)
                # traer preferencias de usuario para comparar atributos
                # bajo cualquier caso registrar en el log
                """if cuenta:
                    if cuenta.fk_status_cuenta == 0:  # ejemplo cambiar a valor y verificar clave foranea
                        # usuario bloqueado
                        # redirigir a pantalla bloqueo
                        pass
                    elif cuenta.intentos_fallidos < 3:  # depende de las preferecnias del usuario

                        pass
                    elif cuenta.fecha_ult_cambio is None:
                        # primer ingreso debe cambiar contraseña si la cuenta fue creada
                        # por el administrador
                        pass
                    elif tools.exp_clave(cuenta.fecha_ult_cambio, cuenta.dias_cambio):
                        # redireccionar a pantalla de cambiar clave
                        pass
                    else:"""
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("/")
                else:
                    msg = 'Invalid credentials'
                    # registrar intentos fallidos.
                    # verificar si la cantidad de intentos es igual a la maxima y bloquear usuario
                    # registrar en el log
            else:
                msg = 'Error validating the form'
        return render(request, "security/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            msg = 'User created - please <a href="/login">login</a>.'
            success = True
            return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "security/register.html", {"form": form, "msg": msg, "success": success})


def forgot_password(request):
    msg = None
    success = False

    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")

            msg = 'Password reset email sent! - please check your email inbox'
            success = True

            # return redirect("/login/")
        else:
            msg = 'Form is not valid'
    else:
        form = ResetPasswordForm()

    return render(request, "security/passwordReset.html", {"form": form, "msg": msg, "success": success})


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
            msg = "Your access request has been sent."
        else:
            print(form)
            tipo_telefono = TablasConfiguracion.obtenerHijos("tipTelefono")
            msg = 'Error validating the form'
    else:
        tipo_telefono = TablasConfiguracion.obtenerHijos("tipTelefono")
        form = LandingPage()
        print("tipo Telefono:", tipo_telefono)

    return render(request, "security/landPage.html",
                  {"form": form, "reason": True, "emailposition": True, "msg": msg, 'success': success,
                   "tipoTelefono": tipo_telefono})


def full_registration(request):
    msg = None
    success = False
    full_registration_form = FullRegistration(request.POST or None)
    form_registration = SignUpForm(request.POST or None)
    tipo_telefono = None
    if request.method == "POST":
        print("form lanpage:", full_registration_form)
        print("form registro:", form_registration)
        if full_registration_form.is_valid() and form_registration.is_valid():
            publico = full_registration_form.save()
            form_registration.save()

            tabla = TablasConfiguracion.objects.get(pk=203)
            CtaUsuario.objects.create(
                intentos_fallidos=3,
                fk_status_cuenta=tabla,
                fk_rol_usuario_id=tabla, dias_cambio=90,
                fk_pregunta_secreta_id=tabla)

            success = True
            msg = "Registration has been completed successfully."


        else:
            tipo_telefono = TablasConfiguracion.obtenerHijos("tipo_telefono")
            msg = 'Error validating the form'
    else:
        tipo_telefono = TablasConfiguracion.obtenerHijos("tipo_telefono")
        full_registration_form = LandingPage()
        form_registration = SignUpForm()
    return render(request, "security/full_registration.html",
                  {"msg": msg, "reason": False, 'success': success, "tipoTelefono": tipo_telefono})


def prueba(request):
    message = create_mail("tadifred@gmail.com", "hola", "security/base_email_template.html",
                          {'user': 'freddy'})
    send_mail(message)
