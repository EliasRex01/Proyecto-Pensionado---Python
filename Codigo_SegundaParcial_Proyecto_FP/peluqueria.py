import datetime

class Factura:
    #Representa la factura que tiene la peluqueria a la que se le añade. No existe si no esta dentro de una pelqueria.
    def __init__(self, timbrado, fecha_valida_hasta):
        self.timbrado = timbrado
        self.fecha_valida_hasta = fecha_valida_hasta

    def obtener_fecha_dia(self):
        fecha_actual = datetime.date.today()
        fecha_formateada = fecha_actual.strftime("%d de %B %Y")
        return fecha_formateada

class Peluqueria:
    #Representa un local, en el sistema puede a ver varias peluquerias pero solo un progamador con acceso al codigo
    #   puede instanciar nuevas.
    def __init__(self, nombre, ruc, direccion, factura):
        self.nombre = nombre
        self.ruc = ruc
        self.direccion = direccion
        self.clientes = []
        self.usuarios = []
        self.factura_para_peluqueria = factura

    def agregar_cliente(self, cliente):
        self.clientes.append(cliente)

    def agregar_usuarios(self, peluquero):
        self.usuarios.append(peluquero)

