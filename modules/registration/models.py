from django.db import models
from django.db.models.fields import DateField
from ..app.models import Estructuraprograma, TablasConfiguracion, Publico
import datetime

# Create your models here.
class PreciosFormacion(models.Model):
    idprograma_precios = models.AutoField(primary_key=True)
    fk_estruc_programa = models.ForeignKey(Estructuraprograma, on_delete=models.CASCADE, default=None, null=True, related_name='prize')
    fecha_registro = models.DateField()
    precio = models.DecimalField(max_digits=11, decimal_places=2, default=None, null=True)
    PorcentajeDescuento = models.DecimalField(max_digits=5, decimal_places=2, default=None, null=True)

    fk_tipo_moneda = models.ForeignKey(TablasConfiguracion, on_delete=models.CASCADE,  default=None, null=True)
    fecha_habilitado = models.DateField(default=None, null=True)
    def LastStructura(id):
        
        try:
            
            ultimoValor = PreciosFormacion.objects.filter(fk_estruc_programa=id)
            ultimoValor =ultimoValor.last()
           
            
            return ultimoValor

        except:
            print("hubo un error ")
            return None



class MatriculaAlumnos(models.Model):
    idmatricula_alumnos = models.AutoField(primary_key=True)
    fk_publico = models.ForeignKey(Publico, on_delete=models.CASCADE, default=None, null=True)
    fk_estruc_programa = models.ForeignKey(Estructuraprograma, on_delete=models.CASCADE, default=None, null=True)
    fecha_matricula = models.DateField()
    fk_tipo_matricula = models.ForeignKey(TablasConfiguracion, on_delete=models.CASCADE, related_name='tipo', default=None, null=True)
    fk_status_matricula = models.ForeignKey(TablasConfiguracion , on_delete=models.CASCADE, related_name='status', default=None, null=True)
    fecha_aprobada = models.DateField(null=True)
    origenSolicitud = models.SmallIntegerField(default=0)
