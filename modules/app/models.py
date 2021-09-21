from django.db import models
# from django.contrib.auth.models import User

class TablasConfiguracion(models.Model):
    id_tabla = models.SmallAutoField(primary_key=True)
    desc_elemento = models.CharField(max_length=70, blank=True, null=True)
    fk_tabla_padre = models.ForeignKey('self', on_delete=models.CASCADE)
    tipo_elemento = models.CharField(max_length=1, blank=True, null=True)
    permite_cambios = models.IntegerField()
    valor_elemento = models.TextField(blank=True, null=True)
    mostrar_en_combos = models.IntegerField(blank=True, null=True)  # Field name made lowercase.
    maneja_lista = models.IntegerField(blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.desc_elemento

    def obtenerHijos(valor):
        lista = None
        try:
            padre = TablasConfiguracion.objects.get(valor_elemento=valor)
            padre.id_tabla
            lista = TablasConfiguracion.objects.get(fk_tabla_padre=padre.id_tabla)
        except:
            return None
        return lista

class Contratantes(models.Model):
    idcontratantes = models.SmallAutoField(primary_key=True)
    siglas = models.TextField(blank=True, null=True)
    nombre_contratante = models.TextField()  # Field name made lowercase.
    apellido_contratante = models.TextField(blank=True, null=True)
    rif_contratante = models.CharField(max_length=20)
    slogan = models.TextField(blank=True, null=True)
    codigo_contrato = models.TextField(blank=True, null=True)
    fecha_contrato = models.DateField(blank=True, null=True)
    mes_inicio_ejerc_fiscal = models.IntegerField()  # Field name made lowercase.
    direccion = models.TextField()
    paginas_web = models.TextField()
    correos = models.TextField()
    telefonnos = models.TextField()
    nombre_comercial = models.TextField()
    personas_contacto = models.TextField(blank=True, null=True)
    representante_legal = models.TextField()

class Publico(models.Model):
    idpublico = models.AutoField(primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=45)  # Field name made lowercase.
    apellido = models.CharField(db_column='Apellido', max_length=45)  # Field name made lowercase.
    direccion = models.TextField()
    procedencia = models.CharField(max_length=1)
    docto_identidad = models.TextField()
    fk_ciudad = models.SmallIntegerField()
    fk_contratante = models.ForeignKey(Contratantes, on_delete=models.CASCADE)
    correos = models.TextField()
    telefonos = models.TextField()
    fecha_registro = models.DateField(null=True)

class Partners(models.Model):
    idpartner = models.AutoField(primary_key=True)
    fk_relacion = models.SmallIntegerField()
    fk_publico = models.IntegerField()
    fk_sitaucion_relacion = models.SmallIntegerField()
    datos_partner = models.TextField(blank=True, null=True)
    paginas_web = models.TextField(blank=True, null=True)  # Field name made lowercase.

class PublicoRelacion(models.Model):
    idpublico_rol = models.SmallAutoField(primary_key=True)
    fk_publico = models.ForeignKey(Publico, on_delete=models.CASCADE)
    fk_relacion = models.ForeignKey(TablasConfiguracion, on_delete=models.CASCADE)

class Aplicaciones(models.Model):
    idaplicaciones = models.SmallAutoField(primary_key=True)  # Field name made lowercase.
    desc_aplicaciones = models.TextField()
    cod_aplicacion = models.CharField(max_length=25)

class AplicacionesContratante(models.Model):
    idaplicaciones_contratante = models.SmallAutoField(primary_key=True)
    fk_contratante = models.SmallIntegerField()
    fk_aplicacion = models.SmallIntegerField()
    cod_status_apli_contrat = models.SmallIntegerField()

class Estructuraprograma(models.Model):
    idestructuraprogrmas = models.SmallAutoField(primary_key=True)
    descripcion = models.TextField()
    fk_estructura_padre = models.ForeignKey('self', on_delete=models.CASCADE)
    peso_creditos = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

class Nivelesprog(models.Model):
    idprogniveles = models.SmallAutoField(primary_key=True)
    programa = models.TextField()
    proceso = models.TextField()
    unidad = models.TextField()
    curso = models.TextField()
    topico = models.TextField()
    actividad = models.TextField()

class Programascap(models.Model):
    idprogramascap = models.AutoField(primary_key=True)  # Field name made lowercase.
    desc_programas = models.TextField()  # Field name made lowercase.
    objetivo = models.TextField()
    alcance = models.TextField()
    fecha_apertura = models.DateField()
