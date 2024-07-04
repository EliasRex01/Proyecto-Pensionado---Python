from BTrees.OOBTree import OOBTree
from persistent import Persistent
from Modelo.configuracion import Producto
import transaction

class Tienda(Persistent):

    #Clase para gestionar la tienda y su inventario.

    def __init__(self,db):
        self.inventario = OOBTree()
        self.db = db

    def agregar_producto(self, producto):
        """Agrega un nuevo producto al inventario."""
        codigo = len(self.inventario) + 1
        self.inventario[codigo] = producto


    # Permite a los clientes devolver productos al inventario.
    def devolver_producto(self, producto_codigo, cantidad):
        try:
            # Convertir el código del producto a int si es una cadena
            producto_codigo = int(producto_codigo)

            producto_en_inventario = self.inventario.get(producto_codigo)

            if producto_en_inventario:
                producto_en_inventario.stock += cantidad
                return True
            else:
                return False
        except (KeyError, ValueError):
            return False


    # Imprime el inventario de productos.
    def obtener_inventario(self):
     return self.inventario

