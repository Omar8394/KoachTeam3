from django import template

register = template.Library()

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
   

   else:
	   return"error"