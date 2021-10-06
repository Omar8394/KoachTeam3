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