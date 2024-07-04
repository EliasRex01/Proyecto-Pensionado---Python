from ControladorFP import AplicacionFP as controlador
from IUBasadaEnTexto import InterfazUsuarioBasadaEnTexto as vista, ConexionZODB as conexion
from peluqueria import *
from persona import *

def main():
    conexionBD = conexion("datos_persistentes/datos_de_FP.fs")
    conexionBD.abrir_conexion()
    peluquerias_disponibles= conexionBD.cargar_peluquerias()

    if not peluquerias_disponibles:
        print("No se encontraron peluquerías existentes. Pide a alguna administrador que cree una.")
        return

    print("Peluquerías disponibles:")
    for i, peluqueria in enumerate(peluquerias_disponibles, 1):
        print(f"{i}: Nombre: {peluqueria.nombre} Ruc: ({peluqueria.ruc}) Direccion: {peluqueria.direccion}")

    seleccion = input("Elige una peluquería por su número: ")
    if seleccion.isnumeric():
        seleccion = int(seleccion)
        if 1 <= seleccion <= len(peluquerias_disponibles):
            peluqueria_seleccionada = peluquerias_disponibles[seleccion - 1]
        else:
            print("Selección no válida.")
            return
    else:
        print("Ingrese un dato valido.")
        return

    controladorFP = controlador(peluqueria_seleccionada)
    vistaFP = vista(controladorFP,conexionBD)
    vistaFP.iniciar_sesion()




if __name__ == "__main__":
    main()

