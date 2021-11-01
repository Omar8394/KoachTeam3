import hashlib
from datetime import datetime
from datetime import timedelta
import random

from django.contrib.auth import update_session_auth_hash

from modules.app.models import TablasConfiguracion
from modules.communication.Methods import send_mail, create_mail
from modules.security.models import CtaUsuario, ExtensionUsuario, EnlaceVerificacion
from django.contrib.auth.models import User


def create_default_ctausuario(status_user, rol):
    fk_rol = TablasConfiguracion.objects.get(valor_elemento=rol)
    fk_status = TablasConfiguracion.objects.get(valor_elemento=status_user)
    fk_pregunta = TablasConfiguracion.objects.get(valor_elemento="question_color")
    cuenta = CtaUsuario.objects.create(
        intentos_fallidos=0,
        fk_status_cuenta=fk_status,
        fk_rol_usuario=fk_rol, dias_cambio=90,
        fk_pregunta_secreta=fk_pregunta, fecha_ult_cambio=datetime.today().strftime("%Y-%m-%d"))
    return cuenta


def change_password_link(enlace, password):
    enlace.usuario.user.set_password(password)
    enlace.save()
    # validar las claves anteriores
    restabler_cuenta(enlace)


def change_password(request, password):
    usuario = ExtensionUsuario.objects.get(user=request.user)
    request.user.set_password(password)
    update_session_auth_hash(request, request.user)
    request.user.save(update_fields=['password'])
    usuario.CtaUsuario.fecha_ult_cambio = datetime.today()
    usuario.CtaUsuario.intentos_fallidos = 0
    usuario.CtaUsuario.save()


def restabler_cuenta(enlace):
    enlace.usuario.user.is_active = True
    enlace.usuario.CtaUsuario.fk_status_cuenta = TablasConfiguracion.objects.get(
        valor_elemento="status_active")
    enlace.usuario.CtaUsuario.intentos_fallidos = 0
    enlace.usuario.CtaUsuario.fecha_ult_cambio = datetime.today()
    enlace.usuario.user.save()
    enlace.usuario.CtaUsuario.save()
    enlace.delete()


def getVerificationLink(ext_user, user_email, expirationtime):
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
                                                     usuario=ext_user)
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
        return datetime.today().strftime(self.formato) >= self.operaciones_dias_fecha(fecha_ult_cambio, dias_venc, True)
