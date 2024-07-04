from abc import ABC as objetoAbstracto, abstractmethod as metodoAbstracto

#==================================================================================================================#
#==================================================================================================================#

class Persona(objetoAbstracto):
    #Es un objeto abstracto que representa a una persona dentro del software.
    def __init__(self, cedula, nombres, apellidos, telefono):
        self.cedula = cedula
        self.nombres = nombres
        self.apellidos = apellidos
        self.telefono = telefono


class Cliente(Persona):
    #Es un objeto que hereda de Persona sus atributos y añade uno para representar a un Cliente de la peluqueria.
    def __init__(self, cedula, nombres, apellidos, telefono, ruc):
        super().__init__(cedula, nombres, apellidos, telefono)
        self.ruc = ruc

class Peluquero(Persona):
    #Es un trabajador o dueño de la peluqueria, hereda de Persona.
    def __init__(self, cedula, nombres, apellidos, telefono):
        super().__init__(cedula, nombres, apellidos, telefono)
        self.catalogo_personal_cortes = []

    def agregar_corte_a_catalogo(self, corte):
        self.catalogo_personal_cortes.append(corte)

#==================================================================================================================#
#==================================================================================================================#

class Usuario(objetoAbstracto):
    #El usuario es la forma que tienen los Peluqueros para interactuar con el software FP. 
    #   Es abstracto por lo que no se puede instanciar y esta compuesto por un Peluquero.
    def __init__(self, peluquero,nombre_usuario,password_usuario):
        self.peluquero = peluquero
        self.nombre_usuario= nombre_usuario
        self.password= password_usuario

    @metodoAbstracto
    def permisos_administrador(self):
        pass


class Administrador(Usuario):
    #Hereda de Usuario sus atributos, esté objeto tiene un menu diferente que el de Cajero
    def permisos_administrador(self):
        return True


class Cajero(Usuario):
    #Hereda de Usuario sus atributos, esté objeto tiene un menu diferente que el de Administrador
    def permisos_administrador(self):
        return False

#==================================================================================================================#
#==================================================================================================================#

class Corte(objetoAbstracto):
    #Objeto abstracto que representa un corte de pelo, tiene un precio estandar y se divide en 3 categorias
    #   corte moderno, corte clasico y corte infantil. Cada uno con su precio correspondiente por dificultad.
    #   cabe aclarar que esos son sus hijos.
    def __init__(self, codigocorte, nombre, descripcion):
        self.codigocorte = codigocorte
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = 25000
        self.iva = 0.10

    @metodoAbstracto
    def calcular_precio(self):
        pass

    def calcular_iva(self):
        return self.precio * self.iva


class CorteClasico(Corte):
    def calcular_precio(self):
        return (self.precio) + self.calcular_iva()


class CorteModerno(Corte):
    def calcular_precio(self):
        return (self.precio * 1.5) + self.calcular_iva()


class CorteInfantil(Corte):
    def calcular_precio(self):
        return (self.precio * 2) + self.calcular_iva()
