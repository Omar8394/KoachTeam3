from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.forms.utils import to_current_timezone
# from django.contrib.auth.models import User

class TablasConfiguracion(models.Model):
    id_tabla = models.SmallAutoField(primary_key=True)
    desc_elemento = models.CharField(max_length=70, blank=True, null=True)
    fk_tabla_padre = models.ForeignKey('self', on_delete=models.CASCADE, default=None, null=True)
    tipo_elemento = models.CharField(max_length=1, blank=True, null=True)
    permite_cambios = models.IntegerField()
    valor_elemento = models.TextField(blank=True, null=True)
    mostrar_en_combos = models.IntegerField(blank=True, null=True)  # Field name made lowercase.
    maneja_lista = models.IntegerField(blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.desc_elemento

    def obtenerHijos(valor):
        
        try:
            
            padre = TablasConfiguracion.objects.filter(valor_elemento=valor)
           
            lista = TablasConfiguracion.objects.filter(fk_tabla_padre=padre[0].id_tabla)
            return lista

        except:
            print("hubo un error al obtener los valores de la tabla padre, valor=", valor)
            return None

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, null=True)
    procedencia = models.CharField(max_length=1)
    docto_identidad = models.TextField()
    fk_ciudad = models.SmallIntegerField(null=True)
    fk_contratante = models.ForeignKey(Contratantes, on_delete=models.CASCADE, default=None, null=True)
    correos = models.TextField()
    telefonos = models.TextField()
    cuenta_telegram = models.CharField(max_length=45, null=True) #telegram id or null
    cuenta_whatsapp = models.CharField(max_length=20, null=True)# whatsapp number or null
    fecha_registro = models.DateField(auto_now_add=True, null=True)
      
    def __str__(self):
        return self.nombre +" " +self.apellido

class Partners(models.Model):
    idpartner = models.AutoField(primary_key=True)
    fk_relacion = models.SmallIntegerField()
    fk_publico = models.IntegerField()
    fk_sitaucion_relacion = models.SmallIntegerField()
    datos_partner = models.TextField(blank=True, null=True)
    paginas_web = models.TextField(blank=True, null=True)  # Field name made lowercase.

class PublicoRelacion(models.Model):
    idpublico_rol = models.SmallAutoField(primary_key=True)
    fk_publico = models.ForeignKey(Publico, on_delete=models.CASCADE, default=None, null=True)
    fk_relacion = models.ForeignKey(TablasConfiguracion, on_delete=models.CASCADE, default=None, null=True)

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
    resumen = models.TextField(null=True)
    valor_elemento = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    peso_creditos = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    fk_categoria = models.ForeignKey(TablasConfiguracion, on_delete=models.CASCADE, default=None, null=True)
    fk_estructura_padre = models.ForeignKey('self', on_delete=models.CASCADE, default=None, null=True)
    def __str__(self):
        return self.descripcion



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

class PreguntasFrecuentes(models.Model):
    idpregunta_frecuente = models.AutoField(primary_key=True)
    texto_pregunta = models.TextField(null=True)
    texto_respuesta = models.TextField(null=True)
    fk_tipo_pregunta_frecuente = models.ForeignKey(TablasConfiguracion, on_delete=models.CASCADE, default=None, null=True)
