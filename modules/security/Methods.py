from datetime import datetime
from datetime import timedelta
from modules.communication.Methods import send_mail, create_mail
from modules.security.models import CtaUsuario


def get_default_ctausuario():
    pass

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
        return self.operaciones_dias_fecha(fecha_ult_cambio, dias_venc, False) == datetime.now().strftime(self.formato)
