# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http.response import JsonResponse
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from django.urls import reverse

from .forms import LoginForm, SignUpForm, ResetPasswordForm, LandingPage, FullRegistration, editProfiles
from modules.app.models import TablasConfiguracion
from modules.security.models import CtaUsuario, EnlaceVerificacion, LandPage
from modules.security import Methods
from ..communication.Methods import create_mail, send_mail
from modules.security.Methods import create_default_ctausuario
from modules.security.models import ExtensionUsuario
from modules.security.forms import RecoveryMethodForm, RecoveryMethodEmail, RecoveryMethodQuestion
from django.http import Http404
import uuid
import os
from core import settings
from pathlib import Path
from django.core.files.storage import FileSystemStorage
import imghdr
from django.contrib import messages
from ..app.models import Publico
import json
from django.contrib.auth.hashers import check_password


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        form = LoginForm(request.POST or None)
        msg = None
        if request.session.get("mensaje"):
            msg = request.session.get("mensaje")
            request.session.flush()
        status_cuenta = None
        rol = "rol_student"
        if request.method == "POST":

            if form.is_valid():
                tools = Methods.securityTools()
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    try:
                        cuenta = ExtensionUsuario.objects.get(user=user)
                        status_cuenta = cuenta.CtaUsuario.fk_status_cuenta.desc_elemento
                    except ExtensionUsuario.DoesNotExist:
                        respuesta = None
                        if request.user.is_superuser:
                            rol = "rol_admin"
                            respuesta = "koach"
                        publico_aux = Methods.create_default_public(user.email)
                        cuenta = Methods.create_default_ctausuario("status_active", rol)
                        status_cuenta = "active"
                        cuenta.respuesta_secreta = respuesta
                        cuenta.save()
                        cuenta = ExtensionUsuario.objects.create(CtaUsuario=cuenta, user=user, Publico=publico_aux)
                        # primera vez configurar la cuenta de usuario por defecto
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
                        code = str(Methods.getVerificationLink(cuenta, user.email, 1))
                        print("cambiar contraseña primera vez")
                        logout(request)
                        if code:
                            return redirect("/emailrecovery/" + code + "/")
                        else:
                            msg = "Error to generate code activaction"
                        return redirect("/emailrecovery/" + code + "/")
                    elif tools.exp_clave(str(cuenta.CtaUsuario.fecha_ult_cambio), cuenta.CtaUsuario.dias_cambio):
                        print("cambiar contraseña por expiracion")
                        logout(request)
                        code = str(Methods.getVerificationLink(cuenta, user.email, 1))
                        if code:
                            return redirect("/emailrecovery/" + code + "/")
                        else:
                            msg = "Error to generate code activaction"

                    elif status_cuenta == 'active':
                        print("entrando")
                        request.session['user_rol'] = cuenta.CtaUsuario.fk_rol_usuario.desc_elemento
                        cuenta.CtaUsuario.intentos_fallidos = 0
                        cuenta.CtaUsuario.save()
                        return redirect("/")
                    # registrar intentos fallidos.
                    # verificar si la cantidad de intentos es igual a la maxima y bloquear usuario
                    # registrar en el log
                else:
                    print("else")
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
        return render(request, "security/login.html", {"form": form, "msg": msg, "empresa": settings.EMPRESA_NOMBRE,
                                                       "urlimage": settings.EMPRESA_URL_LOGO,
                                                       "imagelocal": settings.EMPRESA_SRC_LOGO})


def register_user(request):
    if request.user.is_authenticated:
        return redirect("/login/")
    if settings.LAND_PAGE_MODE == "ON":
        return redirect("/landpage/")
    msg = None
    success = False
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            cuenta = Methods.create_default_ctausuario("status_verification", "rol_student")
            publico = Methods.create_default_public(user.email)
            user_ext = ExtensionUsuario.objects.create(CtaUsuario=cuenta, user=user, Publico=publico)
            code = str(Methods.getVerificationLink(user_ext, form.email, 2))
            enlace = request.get_raw_uri().split("//")[0] + "//" + \
                     request.get_host() + "/verificationaccount/" + code + "/"
            context = {"titulo": "Account Verification", "user": form.username,
                       "content": "Thank you for joining the " + str(
                           settings.EMPRESA_NOMBRE) + " team, to verify your account click on the following link: ",
                       "enlace": enlace, "enlaceTexto": "click here!", "empresa": settings.EMPRESA_NOMBRE,
                       "urlimage": settings.EMPRESA_URL_LOGO}
            send_mail(
                create_mail(form.email, "Account Verification Request", "security/base_email_template_pro.html",
                            context))
            information = {"mensaje": "We have sent you an account verification link to the email provided. Remember to check the spam folder",
                           "titulo": "Registration link has been send", "urlimage": settings.EMPRESA_URL_LOGO,
                           "imagelocal": settings.EMPRESA_SRC_LOGO}
            return render(request, "security/information_view.html", information)
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "security/register.html",
                  {"form": form, "msg": msg, "success": success, "empresa": settings.EMPRESA_NOMBRE,
                   "urlimage": settings.EMPRESA_URL_LOGO, "imagelocal": settings.EMPRESA_SRC_LOGO})


def register_user_new(request, activation_key, registertype, id):
    msg = None
    email = None
    form = SignUpForm()
    if request.user.is_authenticated:
        return redirect("/login/")
    try:
        enlace = EnlaceVerificacion.objects.get(activation_key=activation_key)
        if enlace.usuario.CtaUsuario.fk_status_cuenta == "suspend":
            raise Http404("This account is locked, please contact support")
        elif Methods.verificarenlace(enlace.key_expires):
            print("enlace valido", activation_key)
            if registertype == "landpage":
                lang_page_user = LandPage.objects.get(pk=id)
                email = json.loads(lang_page_user.correos)['emailPrincipal']
            elif registertype == "adminregister":
                email = json.loads(enlace.usuario.Publico.correos)['emailPrincipal']
            if request.method == "GET":
                form = SignUpForm(initial={'email': email})
            elif request.method == "POST":
                form = SignUpForm(request.POST or None, initial={'email': email})
                if form.is_valid():
                    user = form.save()
                    if registertype == "landpage":
                        cuenta = create_default_ctausuario("status_active", "rol_student")
                        id_land = form.cleaned_data.get("id_request")
                        land_page = LandPage.objects.get(pk=id_land)
                        publico_aux = Publico.objects.create(nombre=land_page.nombre,
                                                             apellido=land_page.apellido, direccion=land_page.direccion,
                                                             docto_identidad="No found", correos=land_page.correos,
                                                             telefonos="{}",
                                                             fecha_registro=datetime.today())
                        ExtensionUsuario.objects.create(CtaUsuario=cuenta, Publico=publico_aux, user=user)
                        enlace.delete()
                    elif registertype == "adminregister":
                        enlace.usuario.user = user
                        enlace.usuario.save()
                        enlace.delete()
                    request.session['mensaje'] = "You has been register successfully, Now try login in!"
                    return redirect("/login/")

                else:
                    form = SignUpForm(request.POST or None, initial={'email': email})
                    msg = 'Form is not valid'
        else:
            raise Http404("This link has expired please request another link")
    except EnlaceVerificacion.DoesNotExist:
        raise Http404("This verification link is invalid or has expired")

    return render(request, "security/register_new.html", {"form": form, "msg": msg, "id_request": id,
                                                          "registertype": registertype, "email": email
        , "empresa": settings.EMPRESA_NOMBRE, "urlimage": settings.EMPRESA_URL_LOGO,
                                                          "imagelocal": settings.EMPRESA_SRC_LOGO})


def forgot_password(request):
    msg = None
    success = False
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
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
        return render(request, "security/passwordReset.html",
                      {"form": form, "msg": msg, "success": success, "empresa": settings.EMPRESA_NOMBRE,
                       "urlimage": settings.EMPRESA_URL_LOGO, "imagelocal": settings.EMPRESA_SRC_LOGO})


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
                    ext_user = ExtensionUsuario.objects.get(user__exact=User.objects.get(email__exact=user_email))
                    code = str(Methods.getVerificationLink(ext_user, user_email, 2))
                    if code:
                        enlace = request.get_raw_uri().split("//")[0] + "//" + \
                                 request.get_host() + "/emailrecovery/" + code + "/"
                        context = {"titulo": "Account Recovery Request", "user": user_email,
                                   "content": "We have received an account recovery request, to restore your account click on the following link: ",
                                   "enlace": enlace, "enlaceTexto": "click here!", "empresa": settings.EMPRESA_NOMBRE,
                                   "urlimage": settings.EMPRESA_URL_LOGO}
                        send_mail(
                            create_mail(user_email, "Account Recovery Request", "security/base_email_template_pro.html",
                                        context))
                        request.session.flush()
                        information = {"mensaje": "We have sent an email with a recovery link to your account.",
                                       "titulo": "Verification email sending", "urlimage": settings.EMPRESA_URL_LOGO,
                                       "imagelocal": settings.EMPRESA_SRC_LOGO}
                        return render(request, "security/information_view.html", information)
                    else:
                        print("codigo nulo")

                elif typemethod == 2:
                    request.session['user_email'] = user_email
                    return redirect("/recoverymethodquestion/")
                    pass
            else:
                return redirect("/passwordReset/")
            pass
    return render(request, "security/recoverymethod.html", context)


def recovery_method_question(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.session.get("user_email"):
            email = request.session.get("user_email")
            context = {"user_email": email}
            request.session.flush()
            try:
                user = User.objects.get(email__exact=email)
                ext_user = ExtensionUsuario.objects.get(user=user)
                if ext_user.CtaUsuario.fk_status_cuenta.desc_elemento == "suspended":
                    raise Http404("This account is suspended, please contact support")
                elif ext_user.CtaUsuario.respuesta_secreta is None:
                    information = {"mensaje": "This recovery method has not been established in the account.",
                                   "titulo": "Method not configured", "urlimage": settings.EMPRESA_URL_LOGO,
                                   "imagelocal": settings.EMPRESA_SRC_LOGO}
                    return render(request, "security/information_view.html", information)
                else:
                    msg = None
                    if request.method == "GET":
                        request.session['user_email'] = email
                    elif request.method == "POST":
                        form = RecoveryMethodQuestion(request.POST or None)
                        if form.is_valid():
                            answer = form.cleaned_data.get("secrettext")
                            if answer == ext_user.CtaUsuario.respuesta_secreta:
                                code = str(Methods.getVerificationLink(ext_user, email, 1))
                                if code:
                                    return redirect("/emailrecovery/" + code + "/")
                                else:
                                    msg = "Error to generate code activaction"
                            else:
                                msg = "The secret answer is wrong please try again"
                        else:
                            msg = "form invalid please fill all fields"
                    context = {"question": ext_user.CtaUsuario.fk_pregunta_secreta.desc_elemento, "msg": msg,
                               "empresa": settings.EMPRESA_NOMBRE, "urlimage": settings.EMPRESA_URL_LOGO,
                               "imagelocal": settings.EMPRESA_SRC_LOGO}
                    return render(request, "security/questionrecovery.html", context)

            except User.DoesNotExist:
                raise Http404("The email entered is not associated with any account or this account is suspended")
        else:
            return redirect("/passwordReset/")


def lang_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    if settings.LAND_PAGE_MODE == "OFF":
        return redirect("/register/")
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
                  {"form": form, "reason": True, "emailposition": True, "mensajeland": True, "msg": msg,
                   'success': success,
                   "tipoTelefono": tipo_telefono, "empresa": settings.EMPRESA_NOMBRE,
                   "urlimage": settings.EMPRESA_URL_LOGO, "imagelocal": settings.EMPRESA_SRC_LOGO})


def full_registration(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    if request.session.get("user_rol") != "Admin":
        return HttpResponse("Access Denied, this option its only for admin users", 403)
    msg = None
    success = False
    full_registration_form = FullRegistration(request.POST or None)
    tipo_telefono = None
    tipo_rol = None
    if request.method == "POST":
        if full_registration_form.is_valid():
            rol = request.POST.get("cb_tipo_rol")
            publico = full_registration_form.save()
            cuenta = create_default_ctausuario("status_active", rol)
            ext_user = ExtensionUsuario.objects.create(CtaUsuario=cuenta, user=None, Publico=publico)
            email = json.loads(publico.correos)['emailPrincipal']
            # send verification email
            success = True
            code = str(Methods.getVerificationLink(ext_user, email, 2))
            if code:
                enlace = request.get_raw_uri().split("//")[0] + "//" + \
                         request.get_host() + "/register_new/" + code + "/" + "adminregister/" \
                         + str(ext_user.id) + "/"
                context = {"titulo": "Account Registration Link", "user": publico.nombre + " " + publico.apellido,
                           "content": "Thank you for joining the " + str(
                               settings.EMPRESA_NOMBRE) + " team, follow the link below to register  your account:",
                           "enlace": enlace, "enlaceTexto": "click here!", "empresa": settings.EMPRESA_NOMBRE,
                           "urlimage": settings.EMPRESA_URL_LOGO}
                send_mail(
                    create_mail(email, "Account Registration Link", "security/base_email_template_pro.html",
                                context))
                msg = "Registration has been completed successfully."
                information = {"mensaje": "We have sent the account registration link successfully",
                               "titulo": "Registration link has been send", "urlimage": settings.EMPRESA_URL_LOGO,
                               "imagelocal": settings.EMPRESA_SRC_LOGO}
                return render(request, "security/information_view.html", information)
            else:
                msg = "Error to generate code link verification"

        else:
            tipo_telefono = TablasConfiguracion.obtenerHijos("tipo_telefono")
            tipo_rol = TablasConfiguracion.obtenerHijos("Roles")
            msg = 'Error validating the form'

    else:
        tipo_telefono = TablasConfiguracion.obtenerHijos("tipo_telefono")
        tipo_rol = TablasConfiguracion.obtenerHijos("Roles")
    return render(request, "security/full_registration.html",
                  {"msg": msg, "reason": False, 'success': success, "tipoTelefono": tipo_telefono,
                   "tipoRol": tipo_rol, "empresa": settings.EMPRESA_NOMBRE,
                   "urlimage": settings.EMPRESA_URL_LOGO, "imagelocal": settings.EMPRESA_SRC_LOGO})


def verificationaccount(request, activation_key):
    try:
        enlace = EnlaceVerificacion.objects.get(activation_key=activation_key)
        if enlace.usuario.CtaUsuario.fk_status_cuenta != "suspend":
            if Methods.verificarenlace(enlace.key_expires):
                print("enlace valido", activation_key)
                context = {"user": enlace.usuario.user.username}
                if request.method == "GET":
                    Methods.restabler_cuenta(enlace)
                    loginlink = request.get_raw_uri().split("//")[0] + "//" + \
                                request.get_host() + "/login/"
                    information = {"mensaje": "Thanks for verifying your account, now you can login" + loginlink,
                                   "titulo": "Your account has been verified", "urlimage": settings.EMPRESA_URL_LOGO,
                                   "imagelocal": settings.EMPRESA_SRC_LOGO}
                    return render(request, "security/information_view.html", context)
            else:
                raise Http404("This link has expired please request another link")
        else:
            raise Http404("This account is locked, please contact support")
    except EnlaceVerificacion.DoesNotExist:
        raise Http404("This verification link is invalid or has expired")


def emailrecovery(request, activation_key):
    try:
        enlace = EnlaceVerificacion.objects.get(activation_key=activation_key)
        if enlace.usuario.CtaUsuario.fk_status_cuenta != "suspend":
            if Methods.verificarenlace(enlace.key_expires):
                print("enlace valido", activation_key)
                context = {"user": enlace.usuario.user.username, "urlimage": settings.EMPRESA_URL_LOGO,
                           "imagelocal": settings.EMPRESA_SRC_LOGO}
                if request.method == "POST":
                    form = RecoveryMethodEmail(request.POST or None)
                    if form.is_valid():
                        print("form is valid and key link is valid")
                        Methods.change_password_link(enlace, form.cleaned_data['password1'])
                        return redirect("/login/", kwargs={'msg':
                                                               'Your credentials have been changed correctly, '
                                                               'try to login'})
                    else:
                        print(form)
                        print("invalid form")
            else:
                raise Http404("This link has expired please request another link")
        else:
            raise Http404("This account is locked, please contact support")
    except EnlaceVerificacion.DoesNotExist:
        raise Http404("This verification link is invalid or has expired")
    return render(request, "security/emailrecovery.html", context)


@login_required(login_url="/login/")
def changePassword(request):
    if request.method == 'POST':
        actual_password = request.POST.get('password')
        new_password = request.POST.get('password1')
        # verificar encriptacion
        if actual_password != new_password:
            if check_password(actual_password, request.user.password):
                Methods.change_password(request, new_password)
                response = {
                    'mensaje': 'Your password has been changed correctly',
                    'tipo': 4,
                    'titulo': 'Password changed successfully',
                    'code': 'changed'
                }
            else:
                response = {
                    'mensaje': 'the current password entered is incorrect, please verify your password and try again to change your password',
                    'tipo': 5,
                    'titulo': 'Incorrect Password'
                }
        else:
            response = {
                'mensaje': 'the password you want to change cannot be the same as the current password', 'tipo': 5,
                'titulo': 'Same password'
            }
        return JsonResponse(response)
    elif request.method == 'GET':
        return render(request, "security/cambiarclave.html")


@login_required(login_url="/login/")
def changeSecretQuestion(request):
    usuario = ExtensionUsuario.objects.get(user=request.user)
    if request.method == 'POST':
        respuesta = request.POST.get('respuesta')
        id_pregunta = request.POST.get('cb_tipo_pregunta')
        actual_password = request.POST.get('password')
        # verificar encriptacion
        if check_password(actual_password, request.user.password):
            usuario.CtaUsuario.fk_pregunta_secreta_id = id_pregunta
            usuario.CtaUsuario.respuesta_secreta = respuesta
            usuario.CtaUsuario.save()
            response = {
                'mensaje': 'Your secret question has been changed correctly',
                'tipo': 4,
                'titulo': 'Password changed successfully',
                'code': 'changed'
            }
        else:
            response = {
                'mensaje': 'the current password entered is incorrect, please verify your password and try again to change your secret question',
                'tipo': 5,
                'titulo': 'Incorrect Password'
            }

        return JsonResponse(response)
    elif request.method == 'GET':
        tipo_pregunta = TablasConfiguracion.obtenerHijos("pregSecreta")
        context = {'preguntas': tipo_pregunta, 'pregunta_id': usuario.CtaUsuario.fk_pregunta_secreta_id,
                   'respuesta': usuario.CtaUsuario.respuesta_secreta}
        return render(request, "security/cambiarpregunta.html", context)


def editProfile(request):
    nuevo = ExtensionUsuario.objects.get(user=request.user)
    if not nuevo.Publico:
        publicoNew = Publico.objects.create()
        nuevo.Publico = publicoNew
        nuevo.save()

    profile = Publico.objects.get(idpublico=ExtensionUsuario.objects.get(user=request.user).Publico.idpublico)
    telefono = profile.telefonos
    correo = profile.correos
    img = CtaUsuario.objects.get(
        idcta_usuario=ExtensionUsuario.objects.get(user=request.user).CtaUsuario.idcta_usuario).url_imagen

    if request.method == "POST":

        form = editProfiles(request.POST, instance=profile)

        if form.is_valid():

            obj = form.save(commit=False)

            if obj.telefonos:

                telefonoAlt = {} if not telefono else json.loads(telefono)
                telefonoAlt['telefonoAlternativo'] = obj.telefonos
                obj.telefonos = json.dumps(telefonoAlt)

            elif telefono and 'telefonoAlternativo' in json.loads(telefono):

                telefonoAlt = json.loads(telefono)
                telefonoAlt.pop('telefonoAlternativo')
                obj.telefonos = json.dumps(telefonoAlt)

            else:

                obj.telefonos = telefono

            if obj.correos:

                correoAlt = {} if not correo else json.loads(correo)
                correoAlt['emailAlternativo'] = obj.correos
                obj.correos = json.dumps(correoAlt)

            elif correo and 'emailAlternativo' in json.loads(correo):

                correoAlt = json.loads(correo)
                correoAlt.pop('emailAlternativo')
                obj.correos = json.dumps(correoAlt)

            else:

                obj.correos = correo

            obj.save()

            messages.info(request, 'Changes applied successfully')

            return render(request, "security/profilePage.html", {'form': form, 'telefono': None if not telefono else
            json.loads(telefono)['telefonoPrincipal'] if 'telefonoPrincipal' in json.loads(telefono) else None,
                                                                 'img': img if img and img != "" else None})

        else:

            messages.warning(request, 'An error has occurred!')
            return render(request, "security/profilePage.html", {'form': form, 'telefono': json.loads(telefono)[
                'telefonoPrincipal'] if 'telefonoPrincipal' in json.loads(telefono) else None,
                                                                 'img': img if img and img != "" else None})

    form = editProfiles(instance=profile, initial={'telefonos': None if not telefono else json.loads(telefono)[
        'telefonoAlternativo'] if 'telefonoAlternativo' in json.loads(telefono) else None,
                                                   'correos': None if not correo else json.loads(correo)[
                                                       'emailAlternativo'] if 'emailAlternativo' in json.loads(
                                                       correo) else None})
    return render(request, "security/profilePage.html", {'form': form,
                                                         'telefono': None if not telefono else json.loads(telefono)[
                                                             'telefonoPrincipal'] if 'telefonoPrincipal' in json.loads(
                                                             telefono) else None,
                                                         'img': img if img and img != "" else None})


def images(request):
    if request.method == "POST":

        myfile = request.FILES['file-input']

        fs = FileSystemStorage(location=settings.UPLOAD_ROOT)
        nombreImagen = str(request.user.id) + ".png"
        Ruta = settings.UPLOAD_ROOT + '/user'
        RutaUrl = settings.UPLOAD_URL + '/user'
        try:

            os.mkdir(os.path.join(Ruta))

        except:

            pass

        fs.delete(Ruta + '/' + nombreImagen)
        fs.save(Ruta + '/' + nombreImagen, myfile)

        ctauser = CtaUsuario.objects.filter(
            idcta_usuario=ExtensionUsuario.objects.get(user=request.user).CtaUsuario.idcta_usuario)

        if ctauser:
            ctauser.update(url_imagen=nombreImagen)

        return JsonResponse({'mensaje': 'Changes applied successfully', 'ruta': (RutaUrl + '/' + nombreImagen)})


def rootImages(request):
    if request.method == "POST":

        ctauser = CtaUsuario.objects.get(
            idcta_usuario=ExtensionUsuario.objects.get(user=request.user).CtaUsuario.idcta_usuario)

        if (ctauser.url_imagen):

            Ruta = settings.UPLOAD_URL + 'user/' + ctauser.url_imagen if ctauser else None
            root = settings.UPLOAD_ROOT + '/user/' + ctauser.url_imagen if ctauser else None

            if not os.path.exists(root):
                Ruta = None

        else:

            Ruta = None
            root = None

    response = {
        'ruta': Ruta
    }

    return JsonResponse(response)


def borrarImages(request):
    if request.method == "POST":

        ctauser = CtaUsuario.objects.filter(
            idcta_usuario=ExtensionUsuario.objects.get(user=request.user).CtaUsuario.idcta_usuario)

        if ctauser[0].url_imagen and ctauser[0].url_imagen != '':

            fs = FileSystemStorage(location=settings.UPLOAD_ROOT)
            nombreImagen = ctauser[0].url_imagen
            Ruta = settings.UPLOAD_ROOT + '/user'

            fs.delete(Ruta + '/' + nombreImagen)

            if ctauser:
                ctauser.update(url_imagen=None)

            return JsonResponse({'mensaje': 'Image deleted'})

        else:

            return JsonResponse({'mensaje': 'There is no image to remove'})
