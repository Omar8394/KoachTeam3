# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm, ResetPasswordForm, LandingPage, FullRegistration
from modules.app.models import TablasConfiguracion
from modules.security.models import CtaUsuario, EnlaceVerificacion
from modules.security import Methods
from ..communication.Methods import create_mail, send_mail
from modules.security.Methods import create_default_ctausuario
from modules.security.models import ExtensionUsuario
from modules.security.forms import RecoveryMethodForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        form = LoginForm(request.POST or None)

        msg = None

        if request.method == "POST":

            if form.is_valid():
                tools = Methods.securityTools()
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    cuenta = ExtensionUsuario.objects.get(user=user)
                    status_cuenta = cuenta.CtaUsuario.fk_status_cuenta.desc_elemento
                    print(status_cuenta)
                    if status_cuenta == 'suspended':
                        msg = 'Your account has been suspended for more information contact support.'
                        logout(request)
                    elif status_cuenta == 'locked':
                        # usuario bloqueado
                        msg = 'This account is locked, please contact support or try some recovery method.'
                        logout(request)
                        # redirigir a pantalla bloqueo
                    elif status_cuenta == 'verification':
                        msg = 'This account has not been verified, please enter your email and click on the verification link.'
                        logout(request)
                    elif cuenta.CtaUsuario.fecha_ult_cambio is None:
                        # primer ingreso debe cambiar contraseña si la cuenta fue creada
                        # por el administrador
                        print("cambiar contraseña primera vez")
                        logout(request)
                        pass
                    elif tools.exp_clave(cuenta.CtaUsuario.fecha_ult_cambio, cuenta.CtaUsuario.dias_cambio):
                        # redireccionar a pantalla de cambiar clave
                        logout(request)
                        pass
                    elif status_cuenta == 'active':
                        cuenta.CtaUsuario.intentos_fallidos = 0
                        cuenta.CtaUsuario.save()
                        return redirect("/")

                    # registrar intentos fallidos.
                    # verificar si la cantidad de intentos es igual a la maxima y bloquear usuario
                    # registrar en el log
                else:
                    try:
                        user = User.objects.get(username=username)
                        cuenta = ExtensionUsuario.objects.get(user=user)
                        cuenta.CtaUsuario.intentos_fallidos = cuenta.CtaUsuario.intentos_fallidos + 1
                        cuenta.CtaUsuario.save()
                        status_cuenta = cuenta.CtaUsuario.fk_status_cuenta.desc_elemento
                        if not cuenta.user.is_active:
                            if status_cuenta == 'verification':
                                msg = 'This account has not been verified, please enter your email and click on the verification link.'
                            else:
                                msg = 'This account is locked, please contact support or try some recovery method'
                        elif cuenta.CtaUsuario.intentos_fallidos >= 3 and status_cuenta != "locked":  # depende de las preferecnias del usuario
                            cuenta.CtaUsuario.fk_status_cuenta = TablasConfiguracion.objects.get(
                                valor_elemento="status_locked")
                            cuenta.user.is_active = False
                            cuenta.user.save()
                            msg = 'your account has been blocked for security reasons'
                        else:
                            msg = 'Invalid credentials Remember that if you exceed the maximum number of wrong attempts' \
                                  ' your account will be blocked'
                    except Exception as ex:
                        print("excepcion:", ex)
                        msg = 'the username or password combination is incorrect'
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
        if request.user.is_authenticated:
            return redirect("/")
        else:
            request.session.flush()
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get("email")
                try:
                    user = User.objects.get(email__exact=email)
                    ext_user = ExtensionUsuario.objects.get(user=user)
                    if ext_user.CtaUsuario.fk_status_cuenta.desc_elemento == "suspended":
                        msg = "Your account has been suspended for more information contact support."
                        success = False
                    else:
                        request.session['user_email'] = user.email
                        return redirect("/recoverymethod/")
                except Exception as e:
                    msg = "The email entered is not associated with any account or this account is suspended"
                    success = False
            else:
                msg = 'Form is not valid'
                success = False
    else:
        form = ResetPasswordForm()
    return render(request, "security/passwordReset.html", {"form": form, "msg": msg, "success": success})


def recovery_method(request):
    context = None
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "GET":
            if request.session.get("user_email"):
                context = {"user_email": request.session.get("user_email")}
                request.session.flush()
            else:
                return redirect("/passwordReset/")
        elif request.method == "POST":
            form = RecoveryMethodForm(request.POST or None)
            if form.is_valid():
                typemethod = int(form.cleaned_data.get("typeMethod"))
                user_email = form.cleaned_data.get("email")
                if typemethod == 1:
                    code = str(Methods.getVerificationLink(user_email, request.get_host(), "emailrecovery", 2))
                    if code:
                        enlace = "http://"+code
                        context = {"titulo": "Account Recovery Request", "user": user_email,
                                   "content": "We have received an account recovery request, to restore your account click on the following link: ",
                                   "enlace": enlace, "enlaceTexto": "click here!"}
                        send_mail(create_mail(user_email, "Account Recovery Request", "security/base_email_template_pro.html",
                                              context))
                        print("verificationlink has been sent:", enlace)
                    else:
                        print("codigo nulo")

                elif typemethod == 2:
                    pass
            else:
                return redirect("/passwordReset/")
            pass
    return render(request, "security/recoverymethod.html", context)


def recovery_method_link(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "GET":

            pass
        else:
            pass


def recovery_method_question(request):
    pass


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
            user = form_registration.save()
            user.is_active = False
            user.save()
            cuenta = create_default_ctausuario()
            ExtensionUsuario.objects.create(CtaUsuario=cuenta, user=user, Publico=publico)
            # send verification email
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


def emailrecovery(request, activation_key):

    if request.method == "GET":
        try:
            enlace = EnlaceVerificacion.objects.get(activation_key=activation_key)
            if Methods.verificarenlace(enlace.key_expires):
                print("enlace valido", activation_key)
                pass
            else:
                print("enlace invalido")
                pass
        except Exception as e:
            print("error al validar enlace:", e)
    else:
        print("otro metodo")

