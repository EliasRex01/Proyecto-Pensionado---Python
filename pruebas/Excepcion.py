#!/usr/bin/env python3
'''
Clase para definir excepciones personalizadas que 
manejen sucesos no contemplados en las espeficaciones
'''

#------------------------------------------------------------------------------------

class EntradaNoNumericaException(Exception):
  """
  Excepcion para una entrada que no es numerica
  """
  pass