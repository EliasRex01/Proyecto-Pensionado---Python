from exception import EntradaNoNumericaException

class Menu:
    def __init__(self, post_scraping):
        self.ps = post_scraping

    def mostrar_menu(self):
        while True:
            print(" ____________________________")
            print("|   Sistema de Pensionados   |")
            print(" ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
            print("Seleccione una opción:")
            print("1. Ingresar número de cédula")
            print("2. Salir")
            opcion = input("Opción: ")

            if opcion == "1":
                self.solicitar_ci()
            elif opcion == "2":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción no válida. Intente nuevamente.")

    def solicitar_ci(self):
        ci = input("Ingrese el número de cédula del adulto mayor: ")
        while True:
            try:
                if not ci.isdigit():
                    raise EntradaNoNumericaException("Ingrese sólo números")
                self.ps.procesar(ci)
                break
            except EntradaNoNumericaException as e:
                print(e)
                ci = input("Ingrese el número de cédula del adulto mayor: ")