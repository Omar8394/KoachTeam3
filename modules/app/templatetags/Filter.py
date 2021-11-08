from django import template
from modules.academic.models import EvaluacionesPreguntas, ExamenActividad,ExamenRespuestas,EscalaCalificacion, ProgramaProfesores
from modules.app.models import Estructuraprograma, HistoricoUser, TablasConfiguracion
from modules.planning.models import cursos_prerequisitos
from modules.registration.models import MatriculaAlumnos
from modules.security.models import ExtensionUsuario, CtaUsuario

import random
from django.utils import timezone
import json
from django.core import serializers

register = template.Library()

@register.filter(name='isAdmin')
def isAdmin(user):
    _isAdmin = False
    user = user.extensionusuario
    rol = user.CtaUsuario.fk_rol_usuario.valor_elemento
    if rol == 'rol_admin':
        _isAdmin = True
    return _isAdmin

@register.filter(name='isClosed')
def isClosed(estructura,user):
    _isClosed = False
    user = user.extensionusuario
    publico = user.Publico
    estatus = TablasConfiguracion.obtenerHijos(valor='EstMatricula').get(valor_elemento='EstatusVencido')
    if estatus:
        matriculas = MatriculaAlumnos.objects.filter(fk_estruc_programa=estructura, fk_publico=publico, fk_status_matricula=estatus)
        if matriculas.exists():
            _isClosed=True
    return _isClosed

@register.filter(name='isEnrolled')
def isLocked(estructura, user):
    locked = False
    user = user.extensionusuario
    rol = user.CtaUsuario.fk_rol_usuario.valor_elemento
    publico = user.Publico
    if rol == 'rol_student':
        estatus = TablasConfiguracion.obtenerHijos(valor='EstMatricula').get(valor_elemento='EstatusAprovado')
        matriculas = MatriculaAlumnos.objects.filter(fk_estruc_programa=estructura, fk_publico=publico, fk_status_matricula=estatus)
        if matriculas.exists():
            locked=False
        else:
            locked=True
    return locked

@register.filter(name='locked')
def isNeeded(activity, user):
    isRequired = False
    user = user.extensionusuario
    rol = user.CtaUsuario.fk_rol_usuario.valor_elemento
    publico = user.Publico
    if rol == 'rol_student':
        requisitos = cursos_prerequisitos.objects.filter(fk_estructura_programa=activity)
        if requisitos.exists():
            for requisito in requisitos:
                visto = HistoricoUser.objects.filter(fk_publico = publico, fk_estructura_programa=requisito.fk_estructura_programa_pre, estado=True)
                if not visto.exists():
                    isRequired=True
                    break
    return isRequired

@register.filter(name='getLibrary')
def getLibrary(user):
    response = None
    user = user.extensionusuario
    rol = user.CtaUsuario.fk_rol_usuario.valor_elemento
    publico = user.Publico
    if rol == "rol_admin":
        response = Estructuraprograma.objects.filter(valor_elemento="program")
    if rol == "rol_teacher":
        response = []
        today = timezone.now().date()
        programas = ProgramaProfesores.objects.filter(fk_publico=publico, fecha_retiro__gt=today)
        if programas.exists():
            for programa in programas:
                response.append(programa.fk_estructura_programa)
        else:
            response = None
    if rol == "rol_student":
        response = []
        estatus = TablasConfiguracion.obtenerHijos("EstMatricula").get(valor_elemento="EstatusAprovado")
        programas = MatriculaAlumnos.objects.filter(fk_publico=publico, fk_status_matricula=estatus)
        if programas.exists():
            for programa in programas:
                response.append(programa.fk_estruc_programa)
        else:
            response = None
    return response

@register.filter(name='editableCourse')
def editableCourse(curso, teacher):
  response = False
  publico = teacher
  today = timezone.now().date()
  activo = ProgramaProfesores.objects.filter(fk_publico=publico, fecha_retiro__gt=today, fk_estructura_programa=curso)
  if activo.exists():
      response = True
  return response

@register.filter(name='jsonTlf')
def jsonTlf(datos):
  tlf=None
  data = json.loads(datos)

  
  print(data)
  return data['telefonoPrincipal']

@register.filter(name='jsonEmail')
def jsonEmail(datos):
  tlf=None
  data = json.loads(datos)

  
  print(data)
  return data['emailPrincipal']

@register.filter(name='OrigenMatricula')
def OrigenMatricula(id):
   if id == 1:
	   return"Manual"
   elif id == 2:
	   return"Administrator"
   elif id == 3:
	    return"Planning"
   elif id == 4:
	   return"Expert System"

   else:
	   return"error"
@register.filter(name='shuffleA')
def shuffleColumA(arg):
    aux = list(arg)[:]
    random.shuffle(aux)
    filtered = filter(lambda PreguntasOpciones: PreguntasOpciones.columnaPregunta == 1, aux)
  
    return filtered


@register.filter(name='scalaPuntuacion')
def scalaPuntuacion(id):
    examen=ExamenActividad.objects.get(pk=id)
    escala=examen.fk_Actividad.fk_escala_evaluacion
    resultado=''
    escalasMenor=EscalaCalificacion.objects.filter(fk_escala_evaluacion=escala).order_by("puntos_maximo")
    for scale in escalasMenor:
        if examen.PuntuacionFinal<=scale.puntos_maximo:
            resultado=scale.desc_calificacion
            return resultado

    return resultado
@register.filter(name='RespuestaElegida')
def RespuestaElegida(id):
    respuesta=''
    opcion=ExamenRespuestas.objects.filter(fk_Opcion=id)
    if opcion.count()>0:

        respuesta='checked'
  
    return respuesta

@register.filter(name='RespuestaElegidaTrue')
def RespuestaElegidaTrue(id):
    respuesta=''
    opcion=ExamenRespuestas.objects.filter(fk_Opcion=id)
    if opcion.count()>0:
        if opcion[0].respuetaCorrecta==True:
         respuesta='checked'
  
    return respuesta
@register.filter(name='RespuestaElegidaFalse')
def RespuestaElegidaFalse(id):
    respuesta=''
    opcion=ExamenRespuestas.objects.filter(fk_Opcion=id)
    if opcion.count()>0:
          if opcion[0].respuetaCorrecta==False:
             respuesta='checked'
  
    return respuesta

@register.filter(name='RespuestaElegidaSelect')
def RespuestaElegidaSelect(id):
    respuesta=''
    opcion=ExamenRespuestas.objects.filter(fk_Opcion=id)
    if opcion.count()>0:
        respuesta='selected'
  
    return respuesta
@register.filter(name='RespuestaElegidaRelacionada')
def RespuestaElegidaRelacionada(id, pk2):
    respuesta=''
    opcion=ExamenRespuestas.objects.filter(fk_Opcion=id)
    if opcion.count()>0:
        if opcion[0].fk_OpcionRelacionada.pk==pk2:
         respuesta='selected'
  
    return respuesta

@register.filter(name='Nuller')
def shuffleColumA(obj):
    if(obj==None):
     return 'null'
    else:
     return obj 


@register.filter(name='tf')
def tf(obj):
    if(obj==None):
     return 'null'
    if(obj==True):
     return 'true'
    else:
     return 'false' 

@register.filter(name='JsonList')
def JsonList(arg):
    aux = list(arg)[:]
    print(arg)
    print(aux)
    data = serializers.serialize('json', aux)
    print(data)
    return data
    return JsonList({"data":aux})

@register.filter(name='shuffle')
def shuffle(arg):
    aux = list(arg)[:]
    random.shuffle(aux)
    return aux

@register.filter(name='textoCompletar')
def textoCompletar(id):
   pregunta=EvaluacionesPreguntas.objects.get(pk=id)
   texto=pregunta.texto_pregunta.split()
   texto[pregunta.indicePalabra]='________________'
   nuevoTexto=' '.join(texto)

   return nuevoTexto


@register.filter(name='Origen')
def OrigenPagoCodigo(id):
   if id == 1:
	   return"Paypal"
   elif id == 2:
	   return"Credit Card"
   elif id == 3:
	    return"Bank Transfer"
   

   else:
	   return"error"

@register.filter(name='tipoPregunta')
def TipoPregunta(id):
   if id == 1:
	   return"Simple"
   elif id == 2:
	   return"Multiple"
   elif id == 3:
	    return"Completation"
   elif id == 4:
	    return"Association"
   elif id == 5:
	    return"True or False"
   elif id == 6:
	    return"Expert"

   else:
	   return"error"

@register.filter(name='tipoExamen')
def TipoExamen(id):
   if id == 1:
	   return"Start"
   elif id == 2:
	   return"in Progress"
   elif id == 3:
	    return"Finished"
   elif id == 4:
	    return"TimeOut"
  
   else:
	   return"error"

@register.filter(name='Sidebar')
def Sidebar(usuario):
   rol=ExtensionUsuario.objects.get(user=usuario).CtaUsuario.fk_rol_usuario.valor_elemento
  
   
   return rol