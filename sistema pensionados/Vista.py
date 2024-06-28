#!/usr/bin/env python3
'''
Clase vista que contiene la clase Consola que maneja la interfaz
de usuario del sistema mostrada en la linea de comandos.
'''

#------------------------------------------------------------------------------------

class Consola:
    @staticmethod
    def mostrar_menu():
        """
        Operacion que define el contenido del menu del sistema
        """
        print(" ____________________________")
        print("|   Sistema de Pensionados   |")
        print(" ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
        print("Seleccione una opcion:")
        print("1. Ingresar numero de cedula")
        print("2. Salir")