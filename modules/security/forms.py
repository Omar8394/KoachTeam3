# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User

from ..app.models import Publico
from ..security.models import LandPage


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control",
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))


class RecoveryMethodForm(ResetPasswordForm):
    typeMethod = forms.CharField(widget=forms.NumberInput)


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LandingPage(forms.ModelForm):
    class Meta:
        model = LandPage
        exclude = (
            'fk_ciudad', 'fecha_solicitud', 'status_solicitud', 'codigo_aprobacion', 'fec_cod_expiracion')


class FullRegistration(forms.ModelForm):
    telefonos = forms.CharField(widget=forms.NumberInput)

    class Meta:
        model = Publico
        exclude = (
            'procedencia', 'cuenta_telegram', 'cuenta_whatsapp', 'fk_ciudad', 'fk_contratante', 'fecha_registro')


class editProfiles(forms.ModelForm):

    nombre = forms.CharField(label='Name',
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Add your name",                
                "class": "form-control form-control-line", 
                'maxlength':15,

            }
        ))

    apellido = forms.CharField(label='Last Name',
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Add your last name",                
                "class": "form-control form-control-line",
                'maxlength':100,
                "name":"Last Name"
            }
        ))

        
    # procedencia = forms.CharField(label='Country',
    #     widget=forms.TextInput(
    #         attrs={
    #             "placeholder" : "Add a adress",                
    #             "class": "form-control form-control-line",
    #             'maxlength':200
    #         }
    #     ))

    direccion = forms.CharField(label='Adress',
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Add a adress",                
                "class": "form-control form-control-line",
                'maxlength':200
            }
        ))

    telefonos = forms.CharField(label='Alternative phone', required=False,
        widget=forms.NumberInput(
            attrs={
                "placeholder" : "Add a alternative phone number",                
                "class": "form-control form-control-line",
                'maxlength':100
            }
        ))

    correos = forms.CharField(label='Alternative email', required=False,
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Add a alternative email",                
                "class": "form-control form-control-line",
                'maxlength':100
            }
        ))


    class Meta:
        model = Publico
        exclude = (
            'procedencia', 'cuenta_telegram', 'cuenta_whatsapp', 'fk_ciudad', 'fk_contratante', 'fecha_registro', 'docto_identidad')