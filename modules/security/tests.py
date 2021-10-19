# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import hashlib

from datetime import datetime
from datetime import timedelta
import random



def operaciones_dias_fecha(fechabase, cantidad, operacion):
    formato = "%Y-%m-%d"
    fechabase = datetime.strptime(fechabase,formato)
    if operacion:  # true suma
        fechabase = fechabase + timedelta(days=cantidad)
    else:  # false resta
        fechabase = fechabase - timedelta(days=cantidad)
    return fechabase.strftime(formato)

print(operaciones_dias_fecha("2021-10-13", 90, True))
