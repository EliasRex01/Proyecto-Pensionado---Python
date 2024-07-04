from ZODB import DB
from ZODB.FileStorage import FileStorage
from BTrees._OOBTree import OOBTree
import transaction
import re


class InterfazUsuarioBasadaEnTexto:
    def __init__(self, app_facturacion_peluqueria,conexionBD):
        self.app_facturacion_peluqueria = app_facturacion_peluqueria
        self.conexion= conexionBD

#==================================================================================================================#
#                                       Metodos para control de sesion del usuario                                 #
#==================================================================================================================#

    def iniciar_sesion(self):
        self.app_facturacion_peluqueria.cargar_ruc_clientes()
        print(f"Bienvenido a la peluqueria {self.app_facturacion_peluqueria.peluqueria.nombre}")
        print("Ingrese la sesion con su nombre y contraseña de usuario.")
        while True:
            print("Seleccione una opción:")
            print("1 - Iniciar sesión")
            print("2 - Salir")
            opcion = input("Opción: ")

            if opcion == "1":
                usuario = input("Usuario: ")
                password = input("Contraseña: ")
                usuario_valido = self.app_facturacion_peluqueria.validar_usuario(usuario, password)

                if usuario_valido:
                    print("Inicio de sesión exitoso.")
                    self.app_facturacion_peluqueria.ingresar_usuario(usuario_valido)
                    if usuario_valido.permisos_administrador():
                        self.menu_administrador()
                    else:
                        self.menu_usuario()
                    break
                else:
                    print("Usuario o contraseña incorrectos. Intente nuevamente.")

            elif opcion == "2":
                print("Saliendo de la aplicación.") 
                self.conexion.actualizar_peluqueria(self.app_facturacion_peluqueria.peluqueria)
                self.conexion.cerrar_conexion()
                exit()                     
            else:
                print("Opción no válida. Intente nuevamente.")
              


    def cerrar_sesion(self):
        print("Cerrando sesión...")
        self.app_facturacion_peluqueria.usuario_activo = None  
        self.iniciar_sesion()  

#==================================================================================================================#
#                                       Menus dependiendo de tipo usuario.                                         #
#==================================================================================================================#

    def menu_administrador(self):
        while True:
            self.separador()
            print("Menú de Administrador")
            print("1 - Cobrar a cliente")
            print("2 - Agregar cliente nuevo")
            print("3 - Agregar usuario nuevo")
            print("4 - Agregar un nuevo corte de cabello")
            print("5 - Eliminar cliente existente")
            print("6 - Eliminar usuario existente")
            print("7 - Cerrar sesión")
            opcion = input("Opción: ")

            if opcion == "1":
                #Opcion de Cobrar a cliente, puede pedir factura o ticket
                seleccion_usuario = self.obtener_tipo_comprobante_pago()
                if seleccion_usuario == "1":
                    self.cobrar_con_factura()
                elif seleccion_usuario == "2":
                    self.cobrar_con_ticket()
                elif seleccion_usuario == "3":
                    break 

            elif opcion == "2":
                #Opcion de registrar un nuevo cliente.
                self.registrar_cliente()
            elif opcion == "3":
                #Opcion de registrar un nuevo empleado(usuario) o administrador.
                self.registrar_peluquero()
            elif opcion == "4":
                self.agregar_nuevo_corte_cabello()
            elif opcion == "5":
                #Opcion eliminar cliente existente del software.
                print("Eliminar un cliente existente")
                self.imprimir_clientes()
                cedula = input("Cédula del cliente a eliminar: ")
                self.app_facturacion_peluqueria.eliminar_cliente(cedula)
            elif opcion == "6":
                #Opcion eliminar usuario existente del software.
                self.imprimir_usuarios()
                print("Eliminar un usuario existente")
                nombre_usuario = input("Nombre de usuario del usuario a eliminar: ")       
                self.app_facturacion_peluqueria.eliminar_peluquero(nombre_usuario)
            elif opcion == "7":
                self.cerrar_sesion() 
            else:
                print("Opción no válida. Intente nuevamente.")

    def menu_usuario(self):
        while True:
            self.separador()
            print("Menú de Administrador")
            print("1 - Cobrar a cliente")
            print("2 - Agregar cliente nuevo")
            print("3 - Cerrar sesión")
            opcion = input("Opción: ")
            if opcion == "1":
                #Opcion de Cobrar a cliente, puede pedir factura o ticket
                seleccion_usuario = self.obtener_tipo_comprobante_pago()
                if seleccion_usuario == "1":
                    self.cobrar_con_factura()
                elif seleccion_usuario == "2":
                    self.cobrar_con_ticket()
                elif seleccion_usuario == "3":
                    break 

            elif opcion == "2":
                #Opcion de registrar un nuevo cliente.
                self.registrar_cliente()

            elif opcion == "3":
                #Opcion para cerrar sesion del usuario.
                self.cerrar_sesion() 

#==================================================================================================================#
#                               Metodos para registros dentro del software                                         #
#==================================================================================================================#

    def registrar_peluquero(self):
        print("Usted desea registrar un nuevo peluquero")
        cedula = input("Cédula del peluquero: ")
        nombres = input("Nombres del peluquero: ")
        apellidos = input("Apellidos del peluquero: ")
        telefono = input("Teléfono del cliente (formato: 09xx-xxx-xxx): ")
        telefono = self.validar_formato_telefono(telefono)
        while True:
            nickname= input(f"Ingrese un nombre de usuario para {nombres} {apellidos}: ")
            if not self.nickname_existente(nickname):
                break
            else:
                print("El nickname ya está en uso. Elija otro.")
        password= input(f"Ingrese una contraseña para el usuario {nickname}: ")

        while True:
            print("El nuevo peluquero, sera un usuario tipo \n1- Administrador\n2- Tipo cajero:")
            rol = input("Opcion(Ingrese 1 o 2): ")
            if rol in ("1", "2"):
                break
            else:
                print("Opción no válida. Intente nuevamente.")

        self.app_facturacion_peluqueria.agregar_usuario(rol,cedula, nombres, apellidos, telefono, nickname, password)
        print("Peluquero registrado exitosamente.")

    def registrar_cliente(self):
        print("Usted desea registrar un nuevo cliente dentro del sistema:")
        cedula = input("Cédula del cliente: ")
        nombres = input("Nombres del cliente: ")
        apellidos = input("Apellidos del cliente: ")
        telefono = input("Teléfono del cliente (formato: 09xx-xxx-xxx): ")
        telefono = self.validar_formato_telefono(telefono)
        ruc = input("RUC del cliente: ")
        if self.app_facturacion_peluqueria.verificar_ruc(ruc):
            print(f"El RUC '{ruc}' ya existe en la lista de clientes. No se puede registrar el cliente.")
        else:
            self.app_facturacion_peluqueria.agregar_cliente(cedula, nombres, apellidos, telefono, ruc)
            print(f"Cliente registrado exitosamente con RUC: {ruc}")
    
    def agregar_nuevo_corte_cabello(self):
        print("Agregar un nuevo corte de cabello. Debera elegir un peluquero.\nEstos son cortes existentes: ")
        self.app_facturacion_peluqueria.ver_cortes()
        self.separador()
        print("Cree un nuevo corte: ")
        codigo_corte = input("Código del corte: ")
        nombre_corte = input("Nombre del corte: ")
        descripcion_corte = input("Descripción del corte: ")
        peluqueros = self.app_facturacion_peluqueria.peluqueria.usuarios
        print("Selecciona un peluquero para agregar el corte:")
        self.app_facturacion_peluqueria.ver_usuarios()
        while True:
            opcion_peluquero = input("Elige un peluquero (número): ")
            if opcion_peluquero.isnumeric() and 1 <= int(opcion_peluquero) <= len(peluqueros):
                peluquero_seleccionado = peluqueros[int(opcion_peluquero) - 1]
                break
            else:
                print("Opción no válida. Intente nuevamente.")
    
        if self.app_facturacion_peluqueria.verificar_codigo_corte(codigo_corte):
            print(f"El código del corte '{codigo_corte}' ya existe en el catálogo de un peluquero.")
        else:
            self.app_facturacion_peluqueria.agregar_corte_cabello(peluquero_seleccionado, codigo_corte, nombre_corte, descripcion_corte)

        

#==================================================================================================================#
#                                       Metodos para impresiones varias                                            #
#==================================================================================================================#

    def imprimir_clientes(self):
        self.app_facturacion_peluqueria.ver_clientes()

    def imprimir_usuarios(self):
        self.app_facturacion_peluqueria.ver_usuarios()

    def imprimir_catalogo_cortes_de_peluqueros(self):
        self.app_facturacion_peluqueria.ver_cortes()

    def ver_factura(self,cliente,venta,precio):
        peluqueria= self.app_facturacion_peluqueria.peluqueria
        vendedor= self.app_facturacion_peluqueria.usuario_activo
        factura= peluqueria.factura_para_peluqueria
        self.separador()
        print(f"Factura de {peluqueria.nombre}")
        print(f"Timbrado: {factura.timbrado} valido hasta {factura.fecha_valida_hasta}")
        print(f"Fecha: {factura.obtener_fecha_dia()}")
        print(f"RUC de la empresa: {peluqueria.ruc}")
        print(f"{peluqueria.direccion}")
        print(f"Cliente: {cliente.nombres} {cliente.apellidos}")
        print(f"RUC cliente: {cliente.ruc}")
        print(f"Vendedor {vendedor.peluquero.nombres} {vendedor.peluquero.apellidos}")
        print(f"Detalle\tPrecio")
        for datos in venta:
            print(datos)
        print(f"Total: {precio}")
        self.separador()


    def ver_ticket(self,venta,precio):
        peluqueria= self.app_facturacion_peluqueria.peluqueria
        vendedor= self.app_facturacion_peluqueria.usuario_activo
        factura= peluqueria.factura_para_peluqueria
        self.separador()
        print(f"{peluqueria.nombre}")
        print(f"RUC de la empresa: {peluqueria.ruc}")
        print(f"Fecha: {factura.obtener_fecha_dia()}")
        print(f"{peluqueria.direccion}")
        print(f"Cliente: SIN NOMBRE")
        print(f"Vendedor {vendedor.peluquero.nombres} {vendedor.peluquero.apellidos}")
        print(f"Detalle\tPrecio")
        for datos in venta:
            print(datos)
        print(f"Total: {precio}")

#==================================================================================================================#
#                                      Metodos varios para comprobantes                                            #
#==================================================================================================================#

    def obtener_tipo_comprobante_pago(self):
        while True:
            tipo_documento = input("Seleccione el tipo de documento \n1 - Factura\n2 - Ticket\n3 - Volver al menú\nOpcion: ")
            if tipo_documento in ["1", "2", "3"]:
                return tipo_documento
            else:
                print("Opción no válida. Intente nuevamente.")

    def obtener_datos_venta(self):
        precio_total = 0
        cortes_seleccionados = []
        datos_venta = []

        while True:
            # Parte de seleccion del peluquero
            peluqueros = self.app_facturacion_peluqueria.peluqueria.usuarios

            print("Peluqueros de este local:")
            for i, peluquero in enumerate(peluqueros, start=1):
                print(f"{i} - {peluquero.peluquero.nombres} {peluquero.peluquero.apellidos}")

            while True:
                opcion_peluquero = input("Eliga el peluquero que atendio al cliente: ")
                if opcion_peluquero.isnumeric() and 1 <= int(opcion_peluquero) <= len(peluqueros):
                    peluquero_seleccionado = peluqueros[int(opcion_peluquero) - 1].peluquero
                    break
                else:
                    print("Opción no válida. Intente nuevamente.")

            # Parte de seleccion del corte o cortes de cabello
            catalogo_cortes = peluquero_seleccionado.catalogo_personal_cortes

            print(f"Seleccione qué corte se hizo el cliente con {peluquero_seleccionado.nombres} {peluquero_seleccionado.apellidos}:")
            for i, corte in enumerate(catalogo_cortes, start=1):
                print(f"{i} - {corte.nombre}")

            while True:
                opcion_corte = input("Corte (número) o '0' para finalizar: ")
                if opcion_corte == "0":
                    break  
                if opcion_corte.isnumeric() and 1 <= int(opcion_corte) <= len(catalogo_cortes):
                    corte_seleccionado = catalogo_cortes[int(opcion_corte) - 1]
                    cortes_seleccionados.append(corte_seleccionado)
                    precio_total += corte_seleccionado.calcular_precio()
                    datos_venta.append(f"{corte_seleccionado.nombre}\t{corte_seleccionado.calcular_precio()} Gs.")
                else:
                    print("Opción no válida. Intente nuevamente.")

            if not cortes_seleccionados:
                print("Debe seleccionar al menos un corte.")
            else:
                return datos_venta, precio_total

#==================================================================================================================#
#                   Metodos para cobrar al cliente segun comprobante requerido                                     #
#==================================================================================================================#

    def cobrar_con_factura(self):
        self.separador()
        self.app_facturacion_peluqueria.ver_clientes()
        self.separador()
        while True:
            ruc = input("Ingrese el RUC del cliente: ")
            cliente = self.app_facturacion_peluqueria.buscar_cliente_por_ruc(ruc)
            if cliente:
                datos_venta, precio = self.obtener_datos_venta()
                self.ver_factura(cliente, datos_venta, precio)
                break
            else:
                print(f"El RUC '{ruc}' no se encuentra en la lista de clientes.")
                opcion = input("1- Ingresar nuevamente el RUC.\n2- Registrar un nuevo cliente.\nOpcion: ")
                if opcion == "2":
                    self.registrar_cliente()
                elif opcion != "1":
                    print("Opción no válida. Intente nuevamente.")

    def cobrar_con_ticket(self):
        datos_venta, precio = self.obtener_datos_venta()
        self.ver_ticket(datos_venta, precio)

#==================================================================================================================#
                                        #EXTRAS#
#==================================================================================================================#

    def validar_formato_telefono(self, telefono):
        while not re.match(r'^09\d{2}-\d{3}-\d{3}$', telefono):
            print("Formato de teléfono no válido. Intente nuevamente.")
            telefono = input("Teléfono del cliente (formato: 09xx-xxx-xxx): ")
        return telefono
    
    def nickname_existente(self, nickname):
        for usuario in self.app_facturacion_peluqueria.peluqueria.usuarios:
            if usuario.nombre_usuario == nickname:
                return True
        return False

    def separador(self):
        print("\n╰──────────────────────✧─────────────────────────╮\n")

class ConexionZODB:
    def __init__(self, directorio_bd):
        self.directorio_bd = directorio_bd
        self.db = None

    def abrir_conexion(self):
        # Establece la conexión con la BD y permite obtener, añadir o actualizar datos.
        storage = FileStorage(self.directorio_bd)
        self.db = DB(storage)
        self.conn = self.db.open()
        self.root = self.conn.root()

        # Hoja para guardar una instancia de peluqueria
        if 'peluquerias' not in self.root:
            self.root['peluquerias'] = OOBTree()

    def guardar_peluqueria(self, peluqueria):
        # Inicia una transacción
        peluquerias = self.root['peluquerias']
        peluquerias[peluqueria.nombre] = peluqueria
        transaction.commit()

    def cargar_peluquerias(self):
        peluquerias = self.root['peluquerias']
        return list(peluquerias.values())

    def cerrar_conexion(self):
        if self.conn:
            self.conn.close()

    def actualizar_peluqueria(self, peluqueria):
        print("Se esta guardando datos.")
        transaction.begin()
        self.root['peluquerias'][peluqueria.nombre] = peluqueria
        transaction.commit()

    
