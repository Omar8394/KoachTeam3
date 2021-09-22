from django.db import models
from ..app.models import TablasConfiguracion, Estructuraprograma


class TipoRecursos(models.Model):
    idtipo_recurso = models.SmallAutoField(primary_key=True)
    ruta_icono = models.TextField()
    desc_recurso = models.TextField()
    tipo = models.CharField(max_length=1, blank=True, null=True)

    def __str__(self):
        return self.desc_recurso

class EscalaEvaluacion(models.Model):
    idescala_evaluacion = models.SmallAutoField(primary_key=True)
    desc_escala = models.TextField()
    maxima_puntuacion = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.desc_escala

class EscalaCalificacion(models.Model):
    idescala_calificacion = models.SmallAutoField(primary_key=True)
    desc_calificacion = models.TextField()
    puntos_maximo = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    fk_calificacion = models.ForeignKey(TablasConfiguracion, on_delete=models.CASCADE, default=None, null=True)
    fk_escala_evaluacion = models.ForeignKey(EscalaEvaluacion, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.desc_calificacion

class ActividadEvaluaciones(models.Model):
    idactividad_evaluaciones = models.AutoField(primary_key=True)
    titulo = models.TextField()
    fk_curso_actividad = models.SmallIntegerField(null=True)
    nro_repeticiones = models.IntegerField(blank=True, null=True)
    fk_escala_calificacion = models.ForeignKey(EscalaCalificacion, on_delete=models.CASCADE,  default=None, null=True)
    calificacion_aprobar = models.IntegerField()

    def __str__(self):
        return self.titulo



class Cursos(models.Model):
    idcurso = models.SmallAutoField(primary_key=True)
    desc_curso = models.TextField(db_collation='utf8mb3_swedish_ci')
    abrev_curso = models.CharField(max_length=7, db_collation='utf8mb3_swedish_ci')
    codigo_curso = models.CharField(max_length=15, db_collation='utf8mb3_swedish_ci')
    fk_estruc_programa = models.ForeignKey(Estructuraprograma, on_delete=models.CASCADE, default=None, null=True)
    fk_categoria = models.ForeignKey(TablasConfiguracion, on_delete=models.CASCADE, default=None, null=True)
    disponible_desde = models.DateField()

    def __str__(self):
        return self.desc_curso
