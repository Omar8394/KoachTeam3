# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import hashlib

from datetime import datetime
from datetime import timedelta
import random


class securityTools:
    formato = "%Y-%m-%d"

    def operaciones_dias_fecha(self, fechabase, cantidad, operacion):

        fechabase = datetime.strptime(fechabase, self.formato)
        if operacion:  # true suma
            fechabase = fechabase + timedelta(days=cantidad)
        else:  # false resta
            fechabase = fechabase - timedelta(days=cantidad)
        return fechabase.strftime(self.formato)

    def exp_clave(self, fecha_ult_cambio, dias_venc):
        return datetime.today().strftime(self.formato) >= self.operaciones_dias_fecha(fecha_ult_cambio, dias_venc, True)


tool = securityTools()
print(tool.exp_clave("2021-10-17", 90))
