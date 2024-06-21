#!/usr/bin/env python3
'''
Clase que invoca al sistema
'''

from Controlador import Menu
from Modelo import PostScraping

#------------------------------------------------------------------------------------

def main():
    """
    Operacion main principal que invoca el sistema
    """
    ps = PostScraping()
    objeto_menu = Menu(ps)
    objeto_menu.mostrar_menu()

#------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()