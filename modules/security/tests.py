# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.test import TestCase
from modules.security.Methods import create_mail, send_mail


# Create your tests here.
message = create_mail("kassandra.arellano17@gmail.com", "hola amor", "", {'user': 'Kassandra'})
send_mail(message)



