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
    nro_repeticiones = models.IntegerField(blank=True, null=True)
    duracion = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    fk_estructura_programa = models.OneToOneField(Estructuraprograma,on_delete=models.CASCADE,  default=None, null=True)
    fk_tipo_duracion = models.ForeignKey(TablasConfiguracion, on_delete=models.CASCADE, default=None, null=True, related_name="actividad_tipo_duracion")
    fk_escala_evaluacion = models.ForeignKey(EscalaEvaluacion, on_delete=models.CASCADE,  default=None, null=True)
    calificacion_aprobar = models.IntegerField()

    def __str__(self):
        return self.titulo


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

# aqui pueden ir todos los profesores si cambiamos la fk a estructuras programa
class ProgramaProfesores(models.Model):
    idprograma_profesores=models.AutoField(primary_key=True)
    fecha_autorizado = models.DateField(null=True)
    fecha_retiro = models.DateField(null=True)
    comentarios = models.TextField(null=True)
    fk_publico = models.ForeignKey(Publico, on_delete=models.CASCADE, default=None, null=True)
    fk_estructura_programa = models.ForeignKey(Estructuraprograma, on_delete=models.CASCADE, default=None, null=True)
    fk_situacion= models.ForeignKey(TablasConfiguracion, on_delete=models.CASCADE, default=None, null=True)

class CursosPrerequisitos(models.Model):
    idcurso_prerequisitos = models.SmallAutoField(primary_key=True)
    fk_estruc_programa = models.ForeignKey(Estructuraprograma, on_delete=models.CASCADE, default=None, null=True)
    fk_curso = models.ForeignKey(Cursos, on_delete=models.CASCADE, default=None, null=True)

class PreguntasOpciones(models.Model):
    idpreguntas_opciones=models.AutoField(primary_key=True)
    texto_opcion = models.TextField(null=True)
    tipo_condicion = models.BooleanField(default=False)
    puntos_porc=models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)


class EvaluacionInstrucciones(models.Model):
    idevaluacion_instrucciones=models.AutoField(primary_key=True)
    texto_instrucciones = models.TextField(null=True)
    fk_actividad_evaluaciones = models.ForeignKey(ActividadEvaluaciones, on_delete=models.CASCADE, default=None, null=True)

class EvaluacionesBloques(models.Model):
    idevaluaciones_bloques=models.AutoField(primary_key=True)
    titulo_bloque = models.TextField(null=True)
    comentario = models.TextField(null=True)
    fk_escala_bloque = models.ForeignKey(EscalaEvaluacion, on_delete=models.CASCADE, default=None, null=True)
    fk_actividad_evaluaciones = models.ForeignKey(ActividadEvaluaciones, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.titulo_bloque

class EvaluacionesPreguntas(models.Model):
    idevaluaciones_preguntas = models.AutoField(primary_key=True)
    texto_pregunta = models.TextField(null=True)
    puntos_pregunta = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    fk_evaluaciones_bloque = models.ForeignKey(EvaluacionesBloques, on_delete=models.CASCADE,  default=None, null=True)
    fk_tipo_pregunta_evaluacion = models.ForeignKey(TablasConfiguracion, on_delete=models.CASCADE,  default=None, null=True)

class Recurso(models.Model):
    id_recurso = models.AutoField(primary_key=True)
    titulo = models.TextField(null=True)
    descripcion = models.TextField(null=True)
    path = models.TextField(null=True)
    tipo_path = models.BooleanField(default=False)
    compartido = models.BooleanField(default=False)
    ordenamiento = models.SmallIntegerField(null=True)
    fk_tipo_recurso = models.ForeignKey(TablasConfiguracion,on_delete=models.CASCADE,  default=None, null=True)
    fk_publico_autor = models.ForeignKey(Publico, on_delete=models.CASCADE,  default=None, null=True)

class Tag(models.Model):
    id_tag = models.SmallIntegerField(primary_key=True)
    desc_tag = models.TextField(null=True)

class TagRecurso(models.Model):
    id_tag_recurso = models.AutoField(primary_key=True)
    fk_tag = models.ForeignKey(Tag,on_delete=models.CASCADE,  default=None, null=True)
    fk_recurso = models.ForeignKey(Recurso,on_delete=models.CASCADE,  default=None, null=True)

class RecursoPregunta(models.Model):
    id_recurso_pregunta = models.AutoField(primary_key=True)
    fk_recurso = models.ForeignKey(Recurso,on_delete=models.CASCADE,  default=None, null=True)
    fk_pregunta = models.ForeignKey(EvaluacionesPreguntas,on_delete=models.CASCADE,  default=None, null=True)

class ActividadLeccion(models.Model):
    id_actividad_leccion = models.AutoField(primary_key=True)
    disponible_desde = models.DateField(null=True)
    estatus = models.ForeignKey(TablasConfiguracion,on_delete=models.CASCADE,  default=None, null=True)
    fk_estructura_programa = models.OneToOneField(Estructuraprograma,on_delete=models.CASCADE,  default=None, null=True)

class Paginas(models.Model):
    id_pagina = models.AutoField(primary_key=True)
    titulo = models.TextField(null=True)
    ordenamiento = models.SmallIntegerField(null=True)
    fk_estructura_programa = models.ForeignKey(Estructuraprograma,on_delete=models.CASCADE,  default=None, null=True)

class RecursoPaginas(models.Model):
    id_recurso_pagina = models.AutoField(primary_key=True)
    fk_recurso = models.ForeignKey(Recurso,on_delete=models.CASCADE,  default=None, null=True)
    fk_pagina = models.ForeignKey(Paginas,on_delete=models.CASCADE,  default=None, null=True)

class ActividadTarea(models.Model):
    id_actividad_tarea = models.AutoField(primary_key=True)
    fecha_entrega = models.DateField(null=True)
    fk_estructura_programa = models.OneToOneField(Estructuraprograma,on_delete=models.CASCADE,  default=None, null=True)

class ActividadConferencia(models.Model):
    id_actividad_conferencia = models.AutoField(primary_key=True)
    fecha_hora = models.DateTimeField(null=True)
    enlace = models.TextField(null=True)
    clave = models.TextField(null=True)
    id_conferencia = models.TextField(null=True)
    fk_publico = models.ForeignKey(Publico, on_delete=models.CASCADE, default=None, null=True)
    fk_estructura_programa = models.OneToOneField(Estructuraprograma,on_delete=models.CASCADE,  default=None, null=True)

class EvaluacionPreguntaOpciones(models.Model):
    id_pregunta_opciones = models.AutoField(primary_key=True)
    opcion_texto = models.TextField(null=True)
    condicion = models.BooleanField(default=False)
    puntos = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    fk_evaluaciones_preguntas = models.ForeignKey(EvaluacionesPreguntas, on_delete=models.CASCADE, default=None, null=True)
