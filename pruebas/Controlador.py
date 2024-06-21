#!/usr/bin/env python3
'''
Clase controlador donde se definen las clases que actuan
como controladores, coordinando las interacciones
entre la vista y el modelo.
'''

from Excepcion import EntradaNoNumericaException
from Modelo import PostScraping
from Vista import Consola
import tkinter as tk
from tkinter import messagebox

#------------------------------------------------------------------------------------

class Menu:
    """
    Clase que abstrae la interfaz del sistema
    """
    def __init__(self, post_scraping):
        self.ps = post_scraping

    def mostrar_menu(self):
        """
        Operacion que muestra el menu y maneja excepciones
        """
        while True:
            Consola.mostrar_menu()
            opcion = input("Opcion: ")
            if opcion == "1":
                self.solicitar_ci()
            elif opcion == "2":
                print("Saliendo del sistema...")
                break
            else:
                print("Opcion no valida. Intente nuevamente.")
            
    def solicitar_ci(self):
        """
        Valida la entrada del numero de cedula

        :return: ci valido
        """
        ci = input("Ingrese el numero de cedula del adulto mayor: ")
        while True:
            try:
                if not ci.isdigit():
                    raise EntradaNoNumericaException("Ingrese solo numeros")
                self.ps.procesar(ci)
                break
            except EntradaNoNumericaException as e:
                print(e)
                ci = input("Ingrese el numero de cedula del adulto mayor: ")