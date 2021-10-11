import hashlib
from datetime import datetime
from datetime import timedelta
import random

from modules.app.models import TablasConfiguracion
from modules.communication.Methods import send_mail, create_mail
from modules.security.models import CtaUsuario, ExtensionUsuario, EnlaceVerificacion
from django.contrib.auth.models import User


def create_default_ctausuario():
    fk_rol = TablasConfiguracion.objects.get(valor_elemento="rol_student")
    fk_status = TablasConfiguracion.objects.get(valor_elemento="status_verification")
    fk_pregunta = TablasConfiguracion.objects.get(valor_elemento="question_color")
    cuenta = CtaUsuario.objects.create(
        intentos_fallidos=0,
        fk_status_cuenta=fk_status,
        fk_rol_usuario=fk_rol, dias_cambio=90,
        fk_pregunta_secreta=fk_pregunta)
    return cuenta


def getVerificationLink(user_email, host, viewname, expirationtime):
    try:
        user = User.objects.get(email__exact=user_email)
        ext_user = ExtensionUsuario.objects.get(user=user)
        enlacev = EnlaceVerificacion.objects.filter(usuario=ext_user)
        if not enlacev:
            code = generateVerificationLink(ext_user, user.email, expirationtime)
            if code:
                return host + "/" + viewname + "/" + code + "/"
        else:
            print("Este usuario ya posee un enlace de verificacion activo")
    except Exception as e:
        print("Error verification link:", e)


def generateVerificationLink(user, user_email, expirationtime):
    try:
        x = random.randint(0, 999)
        user_email += str(x)
        h = hashlib.sha1(user_email.encode())
        salt = h.hexdigest()
        activation_key = hashlib.sha1(str(salt + user_email).encode()).hexdigest()
        key_expires = datetime.today() + timedelta(days=expirationtime)
        # key_expires = datetime.strptime(key_expires, '%Y-%m-%d %H:%M:%S')
        print("keyexpires:", key_expires)
        generate = EnlaceVerificacion.objects.create(activation_key=activation_key, key_expires=key_expires,
                                                     usuario=user)
        generate.save()
        return activation_key
    except Exception as e:
        print("error generate link:", e)
    return None


def verificarenlace(key_expires):
    formato = "%Y-%m-%d %H:%M:%S"
    return datetime.strftime(key_expires, formato) >= datetime.now().strftime(formato)


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
        return self.operaciones_dias_fecha(fecha_ult_cambio, dias_venc, True) >= datetime.now().strftime(self.formato)
