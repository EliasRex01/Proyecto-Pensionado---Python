#!/usr/bin/env python3
'''
Clase modelo que contiene la logica de definicion de las clases que representan
el modelo de datos, como Persona, Pensionado, Categoria y las respectivas
categorias de pensionado.
Las clases obtienen informacion de pensionados de la pagina de hacienda
https://www.mef.gov.py/portalspir/dpnc.jsp
'''

from abc import ABCMeta, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pickle
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
        Operacion diferida que debe ser implementada por las clases derivadas
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
    Clase que abstrae una categoria honorifica de pensionado
    """
    def __init__(self):
        self.driver = None

    def setup_driver(self):
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)

    def buscar(self, ci):
        if self.driver is None:
            self.setup_driver()

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

            return HonorificoData(ci, nombre_apellido, departamento, distrito,
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

class HonorificoData:
    """
    Clase auxiliar para recuperar los datos de los pensionados honorificos
    """
    def __init__(self, ci, nombre_apellido, departamento, distrito,
                 concepto_pension, fecha_ingreso, monto_pension):
        self.ci = ci
        self.nombre_apellido = nombre_apellido
        self.departamento = departamento
        self.distrito = distrito
        self.concepto_pension = concepto_pension
        self.fecha_ingreso = fecha_ingreso
        self.monto_pension = monto_pension

#------------------------------------------------------------------------------------

class PostScraping:
    """
    Clase que abstrae un proceso de post scraping
    """
    def __init__(self, gui):
        self.ps_regular = Regular()
        self.ps_faltadoc = EnProceso()
        self.ps_candidato = Candidato()
        self.ps_honorifico = Honorifico()
        self.datos_honorificos = []
        self.gui = gui
    
    def procesar(self, ci):
        self.procesar_regular(ci)
        self.procesar_faltadoc(ci)
        self.procesar_candidato(ci)
        self.procesar_honorifico(ci)
        self.guardar_datos(ci)

    def procesar_regular(self, ci):
        pensionado = Pensionado(ci, self.ps_regular)
        dato = pensionado.buscar_categoria()
        if dato:
            self.gui.mostrar_datos(dato, 'regular')

    def procesar_faltadoc(self, ci):
        p = Pensionado(ci, self.ps_faltadoc)
        dato_faltadoc = p.buscar_categoria()
        if dato_faltadoc:
            if self.ps_regular.buscar(ci) or self.ps_candidato.buscar(ci):
                return
            self.gui.mostrar_datos(dato_faltadoc, 'faltadoc')

    def procesar_candidato(self, ci):
        p = Pensionado(ci, self.ps_candidato)
        dato = p.buscar_categoria()
        if dato:
            self.gui.mostrar_datos(dato, 'candidato')

    def procesar_honorifico(self, ci):
        p = Pensionado(ci, self.ps_honorifico)
        dato = p.buscar_categoria()
        if dato:
            self.datos_honorificos.append(dato)
            self.gui.mostrar_datos(dato, 'honorifico')

    def guardar_datos(self, ci):
        """
        Hace la persistencia de datos mediante pickle
        :param filename: Nombre del archivo donde estaran los datos
        """
        filename = f"datos_{ci}.pickle"
        dato_a_guardar = {
            'datos_honorificos': self.datos_honorificos
        }
        with open(filename, 'wb') as file:
            pickle.dump(dato_a_guardar, file)

    @staticmethod
    def carga_datos(filename):
        """
        Carga los datos de un archivo usando pickle
        :param filename: Nombre del archivo donde estan los datos
        :return: Instancia de un PostScraping cargada con los datos
        """
        with open(filename, 'rb') as file:
            data = pickle.load(file)
        ps = PostScraping()
        ps.datos_honorificos = data['datos_honorificos']
        return ps