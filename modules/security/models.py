from django.db import models
from ..app.models import TablasConfiguracion, Publico

from django.contrib.auth.models import User





class CtaUsuario(models.Model):
    idcta_usuario = models.AutoField(primary_key=True)  # Field name made lowercase.
    #codigo_cta = models.CharField(max_length=15)  # Field name made lowercase.
   # clave = models.TextField(blank=True, null=True)  # Field name made lowercase.
    fk_rol_usuario = models.ForeignKey(TablasConfiguracion, on_delete=models.CASCADE, related_name='rol_usuario')  # Field name made lowercase.
    #fk_publico = models.ForeignKey(Publico, on_delete=models.CASCADE)
    #user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, null=True)
    fk_pregunta_secreta = models.ForeignKey(TablasConfiguracion, on_delete=models.CASCADE, related_name='pregunta')
    intentos_fallidos = models.IntegerField()  # Field name made lowercase.
    fecha_ult_cambio = models.DateField(blank=True, null=True)
    respuesta_secreta = models.TextField(blank=True, null=True)
    fk_status_cuenta = models.ForeignKey(TablasConfiguracion, on_delete=models.CASCADE, related_name='estado_cuenta')
    dias_cambio = models.IntegerField()

class ContratantesRol(models.Model):
    idcontratantes_rol = models.AutoField(primary_key=True)
    desc_rol = models.CharField(max_length=30)  # Field name made lowercase.
    fk_contratante = models.IntegerField()
    valor_rol = models.CharField(max_length=16, blank=True, null=True)

class LandPage(models.Model):
    id_solicitud = models.AutoField(primary_key=True)
    nombre = models.CharField(db_column='Nombre', max_length=45)  # Field name made lowercase.
    apellido = models.CharField(db_column='Apellido', max_length=45)  # Field name made lowercase.
    fk_ciudad = models.SmallIntegerField(null=True)
    direccion = models.TextField()
    correos = models.TextField()
    motivo_solicitud = models.TextField()
    status_solicitud = models.BooleanField(default=False)
    codigo_aprobacion = models.IntegerField(null=True)
    fecha_solicitud = models.DateField(auto_now_add=True, null=True)
    fec_cod_expiracion= models.DateField(null=True)

class LogSeguridad(models.Model):
    idlog_seguridad = models.AutoField(primary_key=True)
    fk_cta_usuario = models.SmallIntegerField()
    fecha_transaccion = models.DateField()  # Field name made lowercase.
    fk_tipo_operacion = models.SmallIntegerField()
    valor_dato = models.TextField(blank=True, null=True)

class ExtensionUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, null=True)
    CtaUsuario = models.OneToOneField(CtaUsuario, on_delete=models.CASCADE, default=None, null=True)
    Publico = models.OneToOneField(Publico, on_delete=models.CASCADE, default=None, null=True)

class EnlaceVerificacion(models.Model):
    id_verificacion = models.AutoField(primary_key=True)
    activation_key = models.TextField(blank=True)
    key_expires = models.DateTimeField(auto_now_add=True)
    usuario = models.OneToOneField(ExtensionUsuario, on_delete=models.CASCADE)
