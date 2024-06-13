#!/usr/bin/env python3
'''
Sistema que hace Scraping sobre la informacion de pensionados 
de la pagina de hacienda
Pagina Principal:
https://www.mef.gov.py/portalspir/dpnc.jsp
'''

import pickle
from abc import ABCMeta, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import requests
import time

#------------------------------------------------------------------------------------

class Persona(metaclass=ABCMeta):
    """
    Clase diferida que abstrae a una persona
    """
    def __init__(self, ci):
        """
        Constructor base para inicializar los atributos comunes de una persona

        :param ci: numero de cedula de una persona
        """
        self.ci = ci

#------------------------------------------------------------------------------------

class Pensionado(Persona):
    """
    Clase que abstrae a un pensionado
    """
    def __init__(self, ci, categoria):
        """
        Constructor que hereda del init de persona

        :param ci: numero de cedula de una persona
        :param categoria: categoria a la que pertenece un pensionado
        """
        super().__init__(ci)
        self.categoria = categoria

    def buscar_categoria(self):
        """
        Operacion que realiza la busqueda del pensionado por su categoria

        :return: Busqueda por categoria
        """
        return self.categoria.buscar(self.ci)

#------------------------------------------------------------------------------------

class Categoria(metaclass=ABCMeta):
    """
    Clase diferida que abstrae una categoria de pensionado
    """
    @abstractmethod
    def buscar(self, ci):
        """
        Operacion diferida que debe ser implementado por las clases derivadas
        para buscar a una categoria de pensionado

        :param ci: numero de cedula de una persona
        """
        raise NotImplementedError("La operacion debe ser implementada")

#------------------------------------------------------------------------------------

class Regular(Categoria):
    """
    Clase que abstrae una categoria regular de pensionado
    """
    def buscar(self, ci):
        url = "https://www.mef.gov.py/portalspir/data_lam.json"
        response = requests.get(url)
        json_data = response.json()

        for row in json_data['rows']:
            if row[2] == ci:
                return row

        return None

#------------------------------------------------------------------------------------

class Honorifico(Categoria):
    """
    Clase que abstrae una categoria honorifico de pensionado
    """
    def __init__(self):
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)

    def buscar(self, ci):
        url = "https://www.mef.gov.py/portalspir/pensiondpnc.jsp"

        self.driver.get(url)

        try:
            ci_input = self.driver.find_element(By.NAME, "ci")
            ci_input.send_keys(ci)
            ci_input.send_keys(Keys.RETURN)
            time.sleep(8)

            ci = self.driver.find_element(
                By.CSS_SELECTOR, "td[aria-describedby='list_ci']").text
            nombre_apellido = self.driver.find_element(
                By.CSS_SELECTOR, "td[aria-describedby='list_nombre']").text
            departamento = self.driver.find_element(
                By.CSS_SELECTOR, "td[aria-describedby='list_depto']").text
            distrito = self.driver.find_element(
                By.CSS_SELECTOR, "td[aria-describedby='list_distrito']").text
            concepto_pension = self.driver.find_element(
                By.CSS_SELECTOR, "td[aria-describedby='list_concepto']").text
            fecha_ingreso = self.driver.find_element(
                By.CSS_SELECTOR,
                "td[aria-describedby='list_fechaIngreso']").text
            monto_pension = self.driver.find_element(
                By.CSS_SELECTOR, "td[aria-describedby='list_monto']").text

            print("Datos del pensionado:")
            print(f"CI: {ci}")
            print(f"Nombre: {nombre_apellido}")
            print(f"Departamento: {departamento}")
            print(f"Distrito: {distrito}")
            print(f"Concepto: {concepto_pension}")
            print(f"Fecha de Ingreso: {fecha_ingreso}")
            print(f"Monto de Pension: {monto_pension}")

            return (ci, nombre_apellido, departamento, distrito,
                    concepto_pension, fecha_ingreso, monto_pension)
        except NoSuchElementException:
            return None

#------------------------------------------------------------------------------------

class EnProceso(Categoria):
    """
    Clase que abstrae una categoria en proceso de pensionado
    """
    def buscar(self, ci):
        url = "https://www.mef.gov.py/portalspir/faltadoclam.json"
        response = requests.get(url)
        json_data = response.json()

        for row in json_data['rows']:
            if row[2] == ci:
                return row

        return None

#------------------------------------------------------------------------------------

class Candidato(Categoria):
    """
    Clase que abstrae una categoria candidato de pensionado
    """
    def buscar(self, ci):
        url = "https://www.mef.gov.py/portalspir/censolam.json"
        response = requests.get(url)
        json_data = response.json()

        for row in json_data['rows']:
            if row[2] == ci:
                return row

        return None

#------------------------------------------------------------------------------------

class PostScraping:
    """
    Clase que abstrae un proceso de post scraping
    """
    def __init__(self):
        self.ps_regular = Regular()
        self.ps_honorifico = Honorifico()
        self.ps_faltadoc = EnProceso()
        self.ps_candidato = Candidato()

    def procesar(self, ci):
        self.procesar_regular(ci)
        self.procesar_honorifico(ci)
        self.procesar_faltadoc(ci)
        self.procesar_candidato(ci)

    def procesar_regular(self, ci):
        pensionado = Pensionado(ci, self.ps_regular)
        dato = pensionado.buscar_categoria()
        if dato:
            self.mostrar_datos_regular(dato)

    def procesar_honorifico(self, ci):
        p = Pensionado(ci, self.ps_honorifico)
        dato = p.buscar_categoria()
        if dato is None:
            print("")

    def procesar_faltadoc(self, ci):
        p = Pensionado(ci, self.ps_faltadoc)
        dato_faltadoc = p.buscar_categoria()
        if dato_faltadoc:
            if (self.ps_regular.buscar(ci) or self.ps_candidato.buscar(ci)):
                return
            self.mostrar_datos_faltadoc(dato_faltadoc)

    def procesar_candidato(self, ci):
        p = Pensionado(ci, self.ps_candidato)
        dato = p.buscar_categoria()
        if dato:
            self.mostrar_datos_candidato(dato)

    def mostrar_datos_regular(self, data):
        print("")
        print("Datos Del Pensionado:")
        print(f"CI: {data[2]}")
        print(f"Nombre y Apellido: {data[3]}")
        print(f"Departamento: {data[0]}")
        print(f"Distrito: {data[1]}")
        print(f"Sexo: {data[4]}")
        print(f"Estado: {data[5]}")
        print(f"Fecha de Ingreso: {data[6]}")
        print(f"Comunidad Indigena: {data[7]}")
        print("")

    def mostrar_datos_faltadoc(self, data):
        print("")
        print("Datos Del Adulto Mayor:")
        print(f"CI: {data[2]}")
        print(f"Nombre y Apellido: {data[3]}")
        print(f"Departamento: {data[0]}")
        print(f"Distrito: {data[1]}")
        print("El Adulto Mayor Necesita Completar Su Documentacion")
        print("")

    def mostrar_datos_candidato(self, data):
        print("")
        print("Datos Del Adulto Mayor:")
        print(f"CI: {data[2]}")
        print(f"Nombre y Apellido: {data[3]}")
        print(f"Departamento: {data[0]}")
        print(f"Distrito: {data[1]}")
        print(f"Año Del Censo: {data[5]}")
        print(f"Institucion: {data[6]}")
        print(f"Situacion: {data[4]}")
        print("")

    def guardar_datos(self, filename):
        """
        Hace la persistencia de datos mediante pickle
        :param filename: Nombre del archivo donde estaran los datos
        """
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def carga_datos(filename):
        """
        Carga los datos de un archivo usando pickle
        :param filename: Nombre del archivo donde estan los datos
        :return: Instancias de un PostScraping cargada con los datos
        """
        with open(filename, 'rb') as file:
            return pickle.load(file)

#------------------------------------------------------------------------------------

class EntradaNoNumericaException(Exception):
    """
    Excepcion para una entrada que no es numerica
    """
    pass

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
            print(" ____________________________")
            print("|   Sistema de Pensionados   |")
            print(" ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
            print("Seleccione una opcion:")
            print("1. Ingresar numero de cedula")
            print("2. Guardar datos")
            print("3. Cargar datos")
            print("4. Salir")
            opcion = input("Opcion: ")

            if opcion == "1":
                self.solicitar_ci()
            elif opcion == "2":
                self.guardar_datos()
            elif opcion == "3":
                self.cargar_datos()
            elif opcion == "4":
                print("Saliendo del sistema...")
                break
            else:
                print("Opcion no valida. Intente nuevamente.")

    def solicitar_ci(self):
        """
        Solicita y valida la entrada del numero de cedula

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

    def guardar_datos(self):
        """
        Operacion para poner nombre al archivo donde se persistencia con pickle
        """
        filename = input("Ingrese el nombre del archivo donde guardar datos: ")
        self.ps.guardar_datos(filename)
        print("Datos guardados en" + filename)

    def cargar_datos(self):
        """
        Operacion que carga datos de un archivo de persistencia usando pickle
        """
        filename = input("Ingrese el nombre del archivo para cargar: ")
        self.ps = PostScraping.carga_datos(filename)
        print("Datos cargados desde" + filename)

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