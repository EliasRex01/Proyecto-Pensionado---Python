from persona import *
from peluqueria import *

class AplicacionFP:
    def __init__(self, peluqueria):
        self.peluqueria = peluqueria 
        self.usuario_activo = None
        self.ruc_existentes = []

#==================================================================================================================#
                                        #Metodos de adjuncion#
#==================================================================================================================#

    def agregar_cliente(self, cedula, nombres, apellidos, telefono, ruc):
        nuevo_cliente = Cliente(cedula, nombres, apellidos, telefono, ruc)
        self.ruc_existentes.append(nuevo_cliente.ruc)  
        self.peluqueria.agregar_cliente(nuevo_cliente)
        

    def agregar_usuario(self, rol, cedula, nombres, apellidos, telefono, nickname, password):
        nuevo_peluquero= Peluquero(cedula, nombres, apellidos, telefono)
        if rol == "1":
            nuevo_usuario = Administrador(nuevo_peluquero, nickname, password)
        else:
            nuevo_usuario = Cajero(nuevo_peluquero, nickname, password)

        self.peluqueria.agregar_usuarios(nuevo_usuario)

    def agregar_corte_cabello(self, peluquero_seleccionado, codigo_corte, nombre_corte, descripcion_corte):
        if peluquero_seleccionado:
            print("¿Qué tipo de corte es?\n1 - Corte Clásico\n2 - Corte Moderno\n3 - Corte Infantil")
            tipo_corte = input("Seleccione el tipo de corte (1/2/3): ")

            if tipo_corte == "1":
                corte = CorteClasico(codigo_corte, nombre_corte, descripcion_corte)
            elif tipo_corte == "2":
                corte = CorteModerno(codigo_corte, nombre_corte, descripcion_corte)
            elif tipo_corte == "3":
                corte = CorteInfantil(codigo_corte, nombre_corte, descripcion_corte)
            else:
                print("Opción no válida. No se agregó el corte.")

            peluquero_seleccionado.peluquero.agregar_corte_a_catalogo(corte)

    
#==================================================================================================================#
                                        #Metodos de carga de datos#
#==================================================================================================================#
    
    def cargar_ruc_clientes(self):
        ruc_clientes = []
        for cliente in self.peluqueria.clientes:
            ruc_clientes.append(cliente.ruc)
        
        self.ruc_existentes.extend(ruc_clientes)

#==================================================================================================================#
                                        #Metodos de separacion#
#==================================================================================================================#

    def eliminar_cliente(self, cedula_cliente):
        clientes = self.peluqueria.clientes
        cliente_eliminado = None
        for cliente in clientes:
            if cliente.cedula == cedula_cliente:
                cliente_eliminado = cliente
                break
        if cliente_eliminado:
            self.peluqueria.clientes.remove(cliente_eliminado)
            print(f"Cliente con cédula {cedula_cliente} eliminado.")
        else:
            print(f"No se encontró un cliente con cédula {cedula_cliente}.")


    def eliminar_peluquero(self, nombre_usuario):
        peluqueros = self.peluqueria.usuarios
        peluquero_eliminado = None
        for peluquero in peluqueros:
            if peluquero.nombre_usuario == nombre_usuario:
                peluquero_eliminado = peluquero
                break
        if peluquero_eliminado:
            self.peluqueria.usuarios.remove(peluquero_eliminado)
            print(f"El usuario llamado {nombre_usuario} eliminado.")
        else:
            print(f"No se encontró un peluquero con nombre {nombre_usuario}.")


#==================================================================================================================#
                                        #Metodos para manejo de usuario#
#==================================================================================================================#

    def ingresar_usuario(self, usuario):
        self.usuario_activo = usuario


    def validar_usuario(self, nombre_usuario, password):
        for usuario in self.peluqueria.usuarios:
            if usuario.nombre_usuario == nombre_usuario and usuario.password == password:
                return usuario
        return None  

#==================================================================================================================#
                                        #Metodos para impresion#
#==================================================================================================================#

    def ver_clientes(self):
        print("Lista de clientes:")
        for i, cliente in enumerate(self.peluqueria.clientes, start=1):
            print(f"{i}- Cédula: {cliente.cedula}, Nombre: {cliente.nombres} {cliente.apellidos}")
            print(f"Telefono de contacto: {cliente.telefono}, RUC: {cliente.ruc}\n")

    def ver_usuarios(self):
        if self.peluqueria:
            print("Lista de usuarios:")
            for i, peluquero in enumerate(self.peluqueria.usuarios, start=1):
                print(f"{i}- Nombre de Usuario: {peluquero.nombre_usuario}")
                print(f"Cédula: {peluquero.peluquero.cedula}, Nombre: {peluquero.peluquero.nombres} {peluquero.peluquero.apellidos}")
                print(f"Telefono de contacto: {peluquero.peluquero.telefono}\n")
        else:
            print("Error: No se ha configurado una instancia de Peluquería.")

    def ver_cortes(self):
        print("Catálogo de cortes:")
        for i, peluquero in enumerate(self.peluqueria.usuarios, start=1):
            print(f"{i}- Peluquero: {peluquero.peluquero.nombres} {peluquero.peluquero.apellidos}")
            for corte in peluquero.peluquero.catalogo_personal_cortes:
                print(f"Código: {corte.codigocorte}, Nombre: {corte.nombre}, Precio: {corte.calcular_precio()}")


#==================================================================================================================#
                                        #Metodos de control, para verificar que no haya repetidos#
#==================================================================================================================#    

    def verificar_ruc(self, ruc):
        if ruc in self.ruc_existentes:
            return True
        else:
            return False

    def verificar_codigo_corte(self, codigo_corte):
        if self.peluqueria:
            for peluquero in self.peluqueria.usuarios:
                for corte in peluquero.peluquero.catalogo_personal_cortes:
                    if corte.codigocorte == codigo_corte:
                        return True
        return False

    def buscar_cliente_por_ruc(self, ruc):
        for cliente in self.peluqueria.clientes:
            if cliente.ruc == ruc:
                return cliente
        return None