

class origenPago:
  def __init__(self, id, origen):
    self.id = id
    self.origen = origen


class origenMatricula:
  def __init__(self, id, origen):
    self.id = id
    self.origen = origen


class MyMethod:




 def ReturnOrigenMatricula(id):
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

def OrigenPagoCodigo(id):
   if id == 1:
	   return"Paypal"
   elif id == 2:
	   return"Credit Card"
   elif id == 3:
	    return"Bank Transfer"
   

   else:
	   return"error"

def OrigenPagoNombre(code):
   if code == "Paypal":
	   return 1
   elif code == "Credit Card":
	   return 2
   elif code == "Bank Transfer":
	    return 3
  

   else:
	   return None


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

def OrigenPreguntaTipo(code):
   if code == "Simple":
	   return 1
   elif code == "Multiple":
	   return 2
   elif code == "Completation":
	    return 3
   elif code == "Association":
	    return 4
   elif code == "True or False":
	    return 5
   elif code == "Expert":
	    return 6
    
  

   else:
	   return None


def TipoExamen(id):
   if id == 1:
	   return"Start"
   elif id == 2:
	   return"in Progress"
   elif id == 3:
	    return"Finished"
  
   else:
	   return"error"

def OrigenTipoExamen(code):
   if code == "Start":
	   return 1
   elif code == "in Progress":
	   return 2
   elif code == "Finished":
	    return 3

    
  

   else:
	   return None

def getOrigenes():

  Origenes = []

  for i in range(3):
    Origenes.append( origenPago(i+1,OrigenPagoCodigo(i+1)) )
    

  return Origenes

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

def ReturnCodeMatricula(code):
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

def getOrigenesMatricula():
  Origenes = []

  for i in range(4):
    Origenes.append( origenMatricula(i+1, ReturnOrigen(i+1)) )
  
  return Origenes