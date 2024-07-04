from abc import ABC, abstractmethod
from persistent import Persistent
from Modelo.configuracion import Empresa


class QuimeraControlador(Persistent,ABC):
# Clase abstracta que representa una transacción

    def __init__(self, cliente, tienda, productos, factura=True):
        self.cliente = cliente
        self.tienda = tienda
        self.productos = productos
        self.factura = factura


    @abstractmethod
    def generar_comprobante(self):
        """Genera un comprobante de la transacción que se implementa en subclase."""
        pass

class Factura(QuimeraControlador):
    def __init__(self, cliente, tienda, productos, ruc_cliente):
        super().__init__(cliente, tienda, productos)
        self.ruc_cliente = ruc_cliente

    def calcular_iva(self, subtotal):
        #Calcula el IVA del subtotal."""
        return subtotal * 0.10

    def generar_comprobante(self):
    #Muestra los detalles de la factura, incluyendo la información de la empresa, el cliente, los productos,
    #comprados, el subtotal, el IVA y el total.
        subtotal = 0
        for producto_codigo, cantidad in self.productos.items():
            try:
                producto_codigo = int(producto_codigo)
                producto_objeto = self.tienda.inventario.get(producto_codigo)

                if producto_objeto:
                    precio_unitario = producto_objeto.precio
                    nombre_producto = producto_objeto.nombre
                    print(f"- {nombre_producto} x{cantidad}: Gs. {precio_unitario} c/u")
                    subtotal += precio_unitario * cantidad
                else:
                    print(f"El producto con código {producto_codigo} no está disponible en el inventario.")
                    return
            except ValueError:
                print(f"Error al convertir el código del producto {producto_codigo} a entero.")
                return

        iva = self.calcular_iva(subtotal)
        total = subtotal + iva

        print("------------------------------------------------------------")
        print("\t\t\t\t\t\t Factura ")
        print("------------------------------------------------------------")
        print("Nombre de la empresa:", Empresa.nombre_empresa)
        print("Dirección de la empresa:", Empresa.direccion_empresa)
        print("Teléfono de la empresa:", Empresa.telefono_empresa)
        print("RUC de la empresa:", Empresa.ruc_empresa)
        print("------------------------------------------------------------")
        print("Cliente:", self.cliente.nombre)
        print("Dirección del Cliente:", self.cliente.direccion)
        print("Teléfono del Cliente:", self.cliente.telefono)
        print("RUC del Cliente:", self.cliente.ruc)
        print("Productos:")

        for producto_codigo, cantidad in self.productos.items():
            try:
                producto_codigo = int(producto_codigo)
                producto_objeto = self.tienda.inventario.get(producto_codigo)

                if producto_objeto:
                    precio_unitario = producto_objeto.precio
                    nombre_producto = producto_objeto.nombre
                    print(f"- {nombre_producto} x{cantidad}: Gs. {precio_unitario} c/u")
                else:
                    print(f"El producto con código {producto_codigo} no está disponible en el inventario.")
                    return
            except ValueError:
                print(f"Error al convertir el código del producto {producto_codigo} a entero.")
                return

        print(f"Subtotal: Gs. {subtotal}")
        print(f"IVA (10%): Gs. {iva}")
        print(f"Total a pagar: Gs. {total}")

class Recibo(QuimeraControlador):
    def generar_comprobante(self):
    #Muestra los detalles del recibo.
        total = 0

        print("------------------------------------------------------------")
        print("\t\t\t\t\t\t Recibo ")
        print("------------------------------------------------------------")
        print("Nombre de la empresa:", Empresa.nombre_empresa)
        print("Dirección de la empresa:", Empresa.direccion_empresa)
        print("Teléfono de la empresa:", Empresa.telefono_empresa)
        print("RUC de la empresa:", Empresa.ruc_empresa)
        print("------------------------------------------------------------")
        print("Cliente:", self.cliente.nombre)
        print("Dirección del Cliente:", self.cliente.direccion)
        print("Teléfono del Cliente:", self.cliente.telefono)
        print("Productos:")

        # ...
        for producto_codigo, cantidad in self.productos.items():
            try:
                producto_codigo = int(producto_codigo)
                producto_objeto = self.tienda.inventario.get(producto_codigo)

                if producto_objeto:
                    precio_unitario = producto_objeto.precio
                    nombre_producto = producto_objeto.nombre
                    print(f"- {nombre_producto} x{cantidad}: Gs. {precio_unitario} c/u")
                    total += precio_unitario * cantidad
                else:
                    print(f"El producto con código {producto_codigo} no está disponible en el inventario.")
                    return
            except ValueError:
                print(f"Error al convertir el código del producto {producto_codigo} a entero.")
                return

            print(f"Total pagado: Gs. {total}")