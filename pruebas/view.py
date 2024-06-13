class MenuView:
    def mostrar_menu(self):
        """
        Muestra el menú y retorna la opción seleccionada por el usuario
        """
        print(" ____________________________")
        print("|   Sistema de Pensionados   |")
        print(" ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
        print("Seleccione una opción:")
        print("1. Ingresar número de cédula")
        print("2. Salir")
        return input("Opción: ")

    def solicitar_ci(self):
        """
        Solicita y retorna la entrada del número de cédula
        """
        return input("Ingrese el número de cédula del adulto mayor: ")

    def opcion_invalida(self):
        """
        Muestra un mensaje de opción inválida
        """
        print("Opción no válida. Intente nuevamente.")

    def mostrar_mensaje(self, mensaje):
        """
        Muestra un mensaje al usuario
        """
        print(mensaje)