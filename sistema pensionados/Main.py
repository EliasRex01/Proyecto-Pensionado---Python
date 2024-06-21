#!/usr/bin/env python3
'''
Clase que abstrae la invocacion del sistema
'''

from logging import root
import tkinter as tk
from Controlador import Menu
from Modelo import PostScraping
from Vista import GUI

#------------------------------------------------------------------------------------

def main():
    """
    Operacion main principal que invoca el sistema
    """
    root = tk.Tk()
    gui = GUI(root, None)
    ps = PostScraping(gui)
    objeto_menu = Menu(root, ps)
    gui.controller = objeto_menu
    objeto_menu.mostrar_menu()
    root.mainloop()

#------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()