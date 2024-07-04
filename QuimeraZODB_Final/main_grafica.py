
from Modelo.tienda import Tienda
from Vista.interfaz_grafica import QuimeraBoutiqueApp,BaseDeDatosZODB
from tkinter import Tk
from tkinter import messagebox
import transaction

class main_grafica:
    def __init__(self):
        self.nombre_db = 'quimera_boutique.fs'
        self.base_de_datos = BaseDeDatosZODB(self.nombre_db)  # Inicializa la conexión a ZODB
        self.tienda = Tienda(self.base_de_datos)  # Pasa la conexión a la tienda
        self.app = None

    def ejecutar(self):
        root = Tk()
        root.title("Quimera Boutique")
        self.app = QuimeraBoutiqueApp(root, self.tienda, self.base_de_datos)
        root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
        root.mainloop()

    def cerrar_aplicacion(self):
        try:
            # Mostrar un mensaje de confirmación antes de salir
            resultado = messagebox.askquestion("Salir", "¿Está seguro que desea salir?", icon='warning')

            if resultado == 'yes':
                # Confirmar cualquier transacción pendiente
                transaction.commit()

                # Cerrar la conexión de la base de datos
                self.base_de_datos.cerrar_conexion()
                # Salir de la aplicación
                self.app.master.destroy()
        except Exception as e:
            print(f"Error al cerrar la aplicación: {e}")



if __name__ == "__main__":
    main = main_grafica()
    main.ejecutar()
