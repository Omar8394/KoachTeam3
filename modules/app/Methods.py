
class MyMethod:
 def ReturnOrigen(id):
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

 def ReturnCode(code):
   if code == "Manual":
	   return 1
   elif code == "Administrator":
	   return 2
   elif code == "Planning":
	    return 3
   elif code == "Expert System":
	   return 4

   else:
	   return None