from ZODB import FileStorage, DB
import transaction
from Modelo.configuracion import Cliente
from Controlador.quimeracontrolador import Factura,Recibo
from Modelo.tienda import Tienda


class InterfazUsuario:
    def __init__(self, tienda):
        self.tienda = tienda

    def mostrar_menu(self):
        print("Bienvenido a Quimera Boutique")
        print("1. Ver inventario")
        print("2. Agregar productos al inventario")
        print("3. Realizar una venta")
        print("4. Devolver producto")
        print("5. Salir")

    def ejecutar(self):
        while True:
            self.mostrar_menu()
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.imprimir_inventario()
            elif opcion == "2":
                self.agregar_producto()
            elif opcion == "3":
                self.realizar_venta()
            elif opcion == "4":
                self.realizar_devolucion()
            elif opcion == "5":
                print("Gracias por usar Quimera Boutique. ¡Hasta luego!")
                break
            else:
                print("Opción no válida. Por favor, seleccione una opción válida.")

    def imprimir_inventario(self):
        print("------------------------------------------------------------")
        print("\t\t\t\t\t\t INVENTARIO ")
        print("------------------------------------------------------------")
        inventario = self.tienda.obtener_inventario()
        for codigo, producto in inventario.items():
            print(
                f'Código: {codigo}, Nombre: {producto.nombre}, Precio: {producto.precio} Gs , Stock: {producto.stock}')
        print("\n")


    def realizar_venta(self):
        print("Productos en el inventario:")
        inventario = self.tienda.obtener_inventario()
        for codigo, producto in inventario.items():
            print(
                f'Código: {codigo}, Nombre: {producto.nombre}, Precio: {producto.precio}, Stock: {producto.stock}')

        while True:
            tipo_comprobante = input("Seleccione el tipo de comprobante (1: Factura, 2: Recibo): ")
            if tipo_comprobante not in ["1", "2"]:
                print("Opción no válida. Por favor, seleccione 1 para Factura o 2 para Recibo.")
            else:
                break

        transaccion = []

        nombre_cliente = input("Nombre del cliente: ")
        direccion_cliente = input("Dirección del cliente: ")
        telefono_cliente = input("Teléfono del cliente: ")

        cliente = Cliente(nombre_cliente, direccion_cliente, telefono_cliente)

        # Inicializa el diccionario de productos vendidos
        productos_vendidos = {}

        # Solicita el RUC antes de seleccionar productos si se elige Factura
        if tipo_comprobante == "1":
            cliente.ruc = input("RUC del Cliente: ")

        while True:
            producto_codigo = input("Seleccione el código del producto para vender (0 para finalizar): ")
            if producto_codigo == "0":
                break

            try:
                producto_codigo = int(producto_codigo)
            except ValueError:
                print("El código del producto debe ser un número entero.")
                continue

            if producto_codigo not in inventario:
                print("El código del producto no existe en el inventario. Verifique el código.")
                continue

            producto = inventario[producto_codigo]
            stock_disponible = producto.stock

            # Solicita la cantidad después de verificar el producto y antes de restarla del stock
            cantidad = int(input("Cantidad a vender: "))

            if cantidad <= 0 or cantidad > stock_disponible:
                print("Cantidad no válida. Verifique la cantidad en stock del producto.")
                continue

            # Resta la cantidad vendida del stock
            producto.stock -= cantidad

            # Agrega el producto y la cantidad vendida al diccionario
            productos_vendidos[producto_codigo] = cantidad
        # ...

        if tipo_comprobante == "1":
            # Genera una factura
            ruc_cliente = cliente.ruc if cliente.ruc else None
            factura = Factura(cliente, self.tienda, productos_vendidos, ruc_cliente)
            factura.generar_comprobante()
        elif tipo_comprobante == "2":
            # Genera un recibo
            recibo = Recibo(cliente, self.tienda, productos_vendidos)
            recibo.generar_comprobante()


        print("¡Venta completada!\n")

    def realizar_devolucion(self):
        print("Productos en el inventario:")
        inventario = self.tienda.obtener_inventario()
        for codigo, producto in inventario.items():
            print(
                f'Código: {codigo}, Nombre: {producto.nombre}, Precio: {producto.precio} Gs , Stock: {producto.stock}')


        while True:
            producto_codigo = input("\nSeleccione el código del producto para devolver (0 para finalizar): ")
            if producto_codigo == "0":
                break

            try:
                producto_codigo = int(producto_codigo)
            except ValueError:
                print("El código del producto debe ser un número entero.")
                continue

            if producto_codigo not in inventario:
                print("El código del producto no existe en el inventario. Verifique el código.")
                continue

            cantidad = int(input("Cantidad a devolver: "))

            if cantidad <= 0:
                print("Cantidad no válida. La cantidad debe ser mayor que cero.")
                continue

            producto_objeto = inventario[producto_codigo]

            if cantidad > producto_objeto.stock:
                print("Error: La cantidad a devolver es mayor que el stock actual del producto.")
                continue

            # Realiza la devolución
            if self.tienda.devolver_producto(producto_codigo, cantidad):
                print(f"Devolución de {cantidad} unidades de {producto_objeto.nombre} realizada con éxito.")
            else:
                print("Error al procesar la devolución.")

        print("¡Devolución completada!\n")


class BaseDeDatosZODB:
    def __init__(self, archivo_bd):
        self.archivo_bd = archivo_bd
        self.connection = None
        self.root = None

    def abrir_conexion(self):
        storage = FileStorage.FileStorage(self.archivo_bd)
        db = DB(storage)
        self.connection = db.open()
        self.root = self.connection.root

        # Crear una instancia de la Tienda si no existe en la base de datos
        if not hasattr(self.root, 'tienda'):
            self.root.tienda = Tienda()


    def cerrar_conexion(self):
        transaction.commit()
        self.connection.close()
