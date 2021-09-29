from django.db import models
from ..app.models import TablasConfiguracion, Publico

class CtaUsuario(models.Model):
    idcta_usuario = models.AutoField(primary_key=True)  # Field name made lowercase.
    codigo_cta = models.CharField(max_length=15)  # Field name made lowercase.
    clave = models.TextField(blank=True, null=True)  # Field name made lowercase.
    fk_rol_usuario = models.ForeignKey(TablasConfiguracion, on_delete=models.CASCADE, related_name='rol_usuario')  # Field name made lowercase.
    fk_publico = models.ForeignKey(Publico, on_delete=models.CASCADE)
    fk_pregunta_secreta = models.ForeignKey(TablasConfiguracion, on_delete=models.CASCADE, related_name='pregunta')
    intentos_fallidos = models.IntegerField()  # Field name made lowercase.
    fecha_ult_cambio = models.DateField(blank=True, null=True)
    respuesta_secreta = models.TextField(blank=True, null=True)
    fk_status_cuenta = models.SmallIntegerField()
    dias_cambio = models.IntegerField()

class ContratantesRol(models.Model):
    idcontratantes_rol = models.AutoField(primary_key=True)
    desc_rol = models.CharField(max_length=30)  # Field name made lowercase.
    fk_contratante = models.IntegerField()
    valor_rol = models.CharField(max_length=16, blank=True, null=True)


class LogSeguridad(models.Model):
    idlog_seguridad = models.AutoField(primary_key=True)
    fk_cta_usuario = models.SmallIntegerField()
    fecha_transaccion = models.DateField()  # Field name made lowercase.
    fk_tipo_operacion = models.SmallIntegerField()
    valor_dato = models.TextField(blank=True, null=True)
