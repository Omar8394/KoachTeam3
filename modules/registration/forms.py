# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.forms import widgets
from modules.registration.models import MatriculaAlumnos


class MatriculaForm(forms.ModelForm):

    class Meta:
        model=MatriculaAlumnos
        fields = ['fk_estruc_programa','fk_tipo_matricula']
        