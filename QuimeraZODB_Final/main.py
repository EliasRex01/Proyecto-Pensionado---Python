
from Vista.interfaz import InterfazUsuario,BaseDeDatosZODB

def main():
    nombre_db = 'quimera_boutique.fs'
    bd = BaseDeDatosZODB(nombre_db)
    bd.abrir_conexion()

    interfaz = InterfazUsuario(bd.root.tienda)
    interfaz.ejecutar()

    bd.cerrar_conexion()

if __name__ == "__main__":
    main()
