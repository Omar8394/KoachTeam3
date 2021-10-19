from django import template
from modules.academic.models import EvaluacionesPreguntas, ExamenActividad,ExamenRespuestas,EscalaCalificacion
import random
import json
from django.core import serializers

register = template.Library()


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
  
   else:
	   return"error"