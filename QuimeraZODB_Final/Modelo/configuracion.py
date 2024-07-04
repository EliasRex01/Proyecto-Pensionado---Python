from persistent import Persistent

class Empresa:
    #Representa la información de la empresa que será impresa en la factura. Son atributos estáticos.
    nombre_empresa = "Quimera Boutique"
    direccion_empresa = "Julia Miranda Cueto c/ España, 452"
    telefono_empresa = "021485763"
    ruc_empresa = "1234567890"


class Cliente(Persistent):
    #Representa a un cliente con nombre, dirección y teléfono. Ruc es opcional en el caso que se haga una factura"""

    def __init__(self, nombre, direccion, telefono, ruc=None):
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.ruc = ruc

class Producto(Persistent):
    def __init__(self, nombre, precio, stock):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock