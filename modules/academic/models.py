from django.db import models
from ..app.models import TablasConfiguracion, Estructuraprograma, Publico


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
    maxima_puntuacion = models.DecimalField(max_digits=6, decimal_places=2)

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
    duracion = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    fk_tipo_duracion = models.ForeignKey(TablasConfiguracion, on_delete=models.CASCADE, default=None, null=True, related_name="actividad_tipo_duracion")
    fk_escala_calificacion = models.ForeignKey(EscalaCalificacion, on_delete=models.CASCADE,  default=None, null=True)
    calificacion_aprobar = models.IntegerField()

    def __str__(self):
        return self.titulo


class EvaluacionesPreguntas(models.Model):
    idevaluaciones_preguntas = models.AutoField(primary_key=True)
    texto_pregunta = models.TextField(null=True)
    puntos_pregunta = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    fk_actividad_evaluaciones = models.IntegerField(null=True)
    fk_tipo_pregunta_evaluacion = models.SmallIntegerField(null=True)

class Cursos(models.Model):
    idcurso = models.SmallAutoField(primary_key=True)
    abrev_curso = models.CharField(max_length=7, db_collation='utf8mb3_swedish_ci')
    codigo_curso = models.CharField(max_length=15, db_collation='utf8mb3_swedish_ci')
    disponible_desde = models.DateField(null=True)
    duracion = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    tipo_evaluacion = models.BooleanField(null=True)
    fk_estruc_programa = models.OneToOneField(Estructuraprograma, on_delete=models.CASCADE, default=None, null=True)
    fk_estatus_curso = models.ForeignKey(TablasConfiguracion, on_delete=models.CASCADE, default=None, null=True, related_name="estatus_curso")
    fk_tipo_duracion = models.ForeignKey(TablasConfiguracion, on_delete=models.CASCADE, default=None, null=True, related_name="tipo_duracion")

    def __str__(self):
        return self.desc_curso


class CursosTopicos(models.Model):
    idcurso_topico=models.AutoField(primary_key=True)
    nomb_topico = models.TextField(null=True)
    disponible_desde = models.DateField(null=True)
    fk_curso = models.ForeignKey(TablasConfiguracion, on_delete=models.CASCADE, default=None, null=True)

class TopicosProfesores(models.Model):
    idtopicos_profesores=models.AutoField(primary_key=True)
    fecha_autorizado = models.DateField(null=True)
    fecha_retiro = models.DateField(null=True)
    fk_publico = models.ForeignKey(Publico, on_delete=models.CASCADE, default=None, null=True)
    fk_cursos_topicos = models.ForeignKey(CursosTopicos, on_delete=models.CASCADE, default=None, null=True)
    fk_situacion= models.ForeignKey(TablasConfiguracion, on_delete=models.CASCADE, default=None, null=True)
