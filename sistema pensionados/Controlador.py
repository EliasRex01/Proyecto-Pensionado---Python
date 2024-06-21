#!/usr/bin/env python3
'''
Clase controlador donde se definen las clases que actuan
como controladores, coordinando las interacciones
entre la vista y el modelo.
'''

from Excepcion import EntradaNoNumericaException
from Modelo import PostScraping
from Vista import GUI
import tkinter as tk
from tkinter import messagebox

#------------------------------------------------------------------------------------

class Menu:
    """
    Clase que abstrae el proceso interno del menu del sistema
    """
    def __init__(self, root, post_scraping):
        self.ps = post_scraping
        self.gui = GUI(root, self)

    def mostrar_menu(self):
        """
        Operacion que muestra el menu
        """
        self.gui.mostrar_menu()
            
    def solicitar_ci(self, entrada):
        """
        Operacion que solicita y valida la entrada del numero de cedula
        """
        ci = entrada.get()
        while True:
            try:
                if not ci.isdigit():
                    raise EntradaNoNumericaException("Ingrese solo numeros")
                self.ps.procesar(ci)
                break
            except EntradaNoNumericaException as e:
                self.gui.mostrar_error(e)