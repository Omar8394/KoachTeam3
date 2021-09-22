from modules.app.models import TablasConfiguracion, Aplicaciones, AplicacionesContratante, Contratantes
from modules.security.models import ContratantesRol
from django.core import settings
#Seeder de configuraciones
settings.configure()

TablasConfiguracion(id_tabla=1, desc_elemento='Registro padre', fk_tabla_padre_id=1, tipo_elemento='1', permite_cambios=1, valor_elemento='Padre', mostrar_en_combos=0, maneja_lista=1)
TablasConfiguracion(id_tabla=2, desc_elemento='Rol sistema', fk_tabla_padre_id=1, tipo_elemento='1', permite_cambios=1, valor_elemento='Roles', mostrar_en_combos=1, maneja_lista=1)
TablasConfiguracion(id_tabla=3, desc_elemento='Situacion cuenta usuario', fk_tabla_padre_id=1, tipo_elemento='1', permite_cambios=0, valor_elemento='Situsua', mostrar_en_combos=1, maneja_lista=1)
TablasConfiguracion(id_tabla=4, desc_elemento='Preguntas Secretas', fk_tabla_padre_id=1, tipo_elemento='1', permite_cambios=1, valor_elemento='pregSecreta', mostrar_en_combos=1, maneja_lista=1)
TablasConfiguracion(id_tabla=5, desc_elemento='Relaciones publico', fk_tabla_padre_id=1,tipo_elemento='1', permite_cambios=1, valor_elemento='Relacion', mostrar_en_combos=1, maneja_lista=1)
TablasConfiguracion(id_tabla=6, desc_elemento='Tipo matricula', fk_tabla_padre_id=1, tipo_elemento='1', permite_cambios=1, valor_elemento='Tipo matricula	', mostrar_en_combos=1, maneja_lista=1)
TablasConfiguracion(id_tabla=7, desc_elemento='Situacion Matricula', fk_tabla_padre_id=1, tipo_elemento='1', permite_cambios=1, valor_elemento='Situacion matricula', mostrar_en_combos=1, maneja_lista=1)
TablasConfiguracion(id_tabla=8, desc_elemento='Tipo Competencia', fk_tabla_padre_id=1, tipo_elemento='1', permite_cambios=1, valor_elemento='Tipo competencia	', mostrar_en_combos=1, maneja_lista=1)
TablasConfiguracion(id_tabla=9, desc_elemento='Tipo Actividad', fk_tabla_padre_id=1, tipo_elemento='1', permite_cambios=1, valor_elemento='Tipo actividad', mostrar_en_combos=1, maneja_lista=1)
TablasConfiguracion(id_tabla=10, desc_elemento='Tipo Recurso', fk_tabla_padre_id=1, tipo_elemento='1', permite_cambios=1, valor_elemento='Recurso', mostrar_en_combos=1, maneja_lista=1)
TablasConfiguracion(id_tabla=11, desc_elemento='Tipo pregunta', fk_tabla_padre_id=1, tipo_elemento='1', permite_cambios=1, valor_elemento='PregEvalua', mostrar_en_combos=1, maneja_lista=1)
TablasConfiguracion(id_tabla=12, desc_elemento='Tipo de adiestramiento', fk_tabla_padre_id=1, tipo_elemento='1', permite_cambios=1, valor_elemento='TipoAdiest', mostrar_en_combos=1, maneja_lista=1)
TablasConfiguracion(id_tabla=13, desc_elemento='Tipo duracion ', fk_tabla_padre_id=1, tipo_elemento='1', permite_cambios=1, valor_elemento='Duracion', mostrar_en_combos=1, maneja_lista=1)
TablasConfiguracion(id_tabla=14, desc_elemento='Situacion Plan ', fk_tabla_padre_id=1, tipo_elemento='1', permite_cambios=1, valor_elemento='SituPlan', mostrar_en_combos=1, maneja_lista=1)
TablasConfiguracion(id_tabla=15, desc_elemento='Ramas', fk_tabla_padre_id=1, tipo_elemento='1', permite_cambios=1, valor_elemento='Rama', mostrar_en_combos=1, maneja_lista=1)
TablasConfiguracion(id_tabla=16, desc_elemento='Prioridad', fk_tabla_padre_id=1, tipo_elemento='1', permite_cambios=1, valor_elemento='Prioridad', mostrar_en_combos=1, maneja_lista=1)
TablasConfiguracion(id_tabla=17, desc_elemento='Nivel Competencia', fk_tabla_padre_id=1, tipo_elemento='1', permite_cambios=1, valor_elemento='NivelComp', mostrar_en_combos=1, maneja_lista=1)
TablasConfiguracion(id_tabla=18, desc_elemento='Calificaciones escala', fk_tabla_padre_id=1, tipo_elemento='1', permite_cambios=1, valor_elemento='calif', mostrar_en_combos=1, maneja_lista=1)
TablasConfiguracion(id_tabla=19, desc_elemento='Tipos de moneda', fk_tabla_padre_id=1, tipo_elemento='1', permite_cambios=1, valor_elemento='Moneda', mostrar_en_combos=1, maneja_lista=1)

#Seeder de contratantes
Contratantes(idcontratantes=2, siglas='JC Energy ', nombre_contratante='JC Energy Solar, Corp', apellido_contratante	= None, rif_contratante='1234', slogan = None, codigo_contrato= None, fecha_contrato='2021-08-30', mes_inicio_ejerc_fiscal=1, direccion='Austin, Texas', paginas_web='JC Energy.com', correos='n/a', telefonnos='n/a', nombre_comercial='JC Energy Solar', personas_contacto=None, representante_legal='Jose Carucci');

#Seeder de contratantes rol
ContratantesRol(idcontratantes_rol=1, desc_rol='Profesores', fk_contratante=2, valor_rol='profe')
ContratantesRol(idcontratantes_rol=2, desc_rol='Alumnos', fk_contratante=2, valor_rol='alum')
ContratantesRol(idcontratantes_rol=3, desc_rol='Asistentes', fk_contratante=2, valor_rol='asis')
ContratantesRol(idcontratantes_rol=4, desc_rol='Planificadores', fk_contratante=2, valor_rol='planif')
ContratantesRol(idcontratantes_rol=5, desc_rol='Autores', fk_contratante=2, valor_rol='autor')
ContratantesRol(idcontratantes_rol=6, desc_rol='Administrador', fk_contratante=2, valor_rol='admin')
ContratantesRol(idcontratantes_rol=7, desc_rol='Control estudio', fk_contratante=2, valor_rol='control')

#Seeder de aplicaciones
Aplicaciones(idaplicaciones=9, desc_aplicaciones='Sistema Formacion y capacitacion E-Learning', cod_aplicacion='KOACH_E-Learning')

#Seeder de aplicaciones contratante
AplicacionesContratante(idaplicaciones_contratante=6, fk_contratante=2, fk_aplicacion=9, cod_status_apli_contrat=1)

