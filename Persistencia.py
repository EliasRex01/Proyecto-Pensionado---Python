# logica adaptada a la persistencia de datos

        
import requests
import time
from abc import ABC, ABCMeta, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# clase base que abstrae a un pensionado (abstracta)
class Pensionado:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    # operacion base de buscar que es usado por las otras subclases pero de
    # multiples formas (polimorfica)
    @abstractmethod
    def buscar(self, ci):
        raise NotImplementedError(
            "Este metodo debe ser implementado por las subclases")

# clase que abstrae a un pensionado regular


class PensionadoRegular(Pensionado):

    # operacion para buscar datos de un pensionado regular,
    # se usa directamente el json de la pagina
    def buscar(self, ci):
        url = "https://www.mef.gov.py/portalspir/data_lam.json"
        response = requests.get(url)
        json_data = response.json()

        for row in json_data['rows']:
            if row[2] == ci:
                return row

        return None

# clase que abstrae a un pensionado que es honorifico


class PensionadoHonorifico(Pensionado):
    def __init__(self):
        # configurar las opciones del chromedriver
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)

    # implementacion de la operacion polimorfica buscar, en este caso se usa la captura
    # de datos con selenium ya que la pagina no devuelve un tipo json o siquiera un
    # archivo de tipo valido
    def buscar(self, ci):
        url = "https://www.mef.gov.py/portalspir/pensiondpnc.jsp"

        # abrir la pagina en el navegador
        self.driver.get(url)

        try:
            # Encontrar el campo de ci y enviar el valor
            ci_input = self.driver.find_element(By.NAME, "ci")
            ci_input.send_keys(ci)
            ci_input.send_keys(Keys.RETURN)

            # Esperar un tiempo suficiente para que los resultados se carguen
            time.sleep(8)

            # Obtener los datos del formulario de filtro de búsqueda de la
            # página
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
                By.CSS_SELECTOR, "td[aria-describedby='list_fechaIngreso']").text
            monto_pension = self.driver.find_element(
                By.CSS_SELECTOR, "td[aria-describedby='list_monto']").text

            # Mostrar los datos por pantalla
            print("Datos del pensionado:")
            print(f"CI: {ci}")
            print(f"Nombre: {nombre_apellido}")
            print(f"Departamento: {departamento}")
            print(f"Distrito: {distrito}")
            print(f"Concepto: {concepto_pension}")
            print(f"Fecha de Ingreso: {fecha_ingreso}")
            print(f"Monto de Pensión: {monto_pension}")

            # Retornar los datos encontrados
            return (
                ci, nombre_apellido, departamento, distrito, concepto_pension,
                fecha_ingreso, monto_pension)
        except NoSuchElementException:
            # Si no se encuentra el elemento, retorna None
            return None

# clase que abstrae a un pensionado al cual se falta algun documento


class PensionadoEnProceso(Pensionado):

    def buscar(self, ci):
        url = "https://www.mef.gov.py/portalspir/faltadoclam.json"
        response = requests.get(url)
        json_data = response.json()

        for row in json_data['rows']:
            if row[2] == ci:
                return row

        return None

# clase que abstrae a un candidato a pensionado


class PensionadoCandidato(Pensionado):

    # operacion para buscar datos de un candidato a pensionado,
    # se usa directamente el json de la pagina
    def buscar(self, ci):
        url = "https://www.mef.gov.py/portalspir/censolam.json"
        response = requests.get(url)
        json_data = response.json()

        for row in json_data['rows']:
            if row[2] == ci:
                return row

        return None

# clase que abstrae la consulta del pensionado y hace uso de la operacion
# buscar en sus operaciones consultar


class Consulta:

    def __init__(self):
        self.pensionado_regular = PensionadoRegular()
        self.pensionado_honorifico = PensionadoHonorifico()
        self.pensionado_faltadoc = PensionadoEnProceso()
        self.pensionado_candidato = PensionadoCandidato()

    # operacion para consultar los datos del pensionado regular
    def consultar_regular(self, ci):
        dato = self.pensionado_regular.buscar(ci)
        if dato is None:
            print("")
        else:
            self.mostrar_datos_pensionado_regular(dato)

    # operacion para consultar los datos del pensionado honorifico
    def consultar_honorifico(self, ci):
        dato = self.pensionado_honorifico.buscar(ci)
        if dato is None:
            print("")

    # operacion para consultar los datos del pensionado al cual le faltan
    # documentos
    def consultar_faltadoc(self, ci):
      dato_faltadoc = self.pensionado_faltadoc.buscar(ci)
      if dato_faltadoc:
          # Verificar si el pensionado tambien aparece en otras listas
          if (self.pensionado_regular.buscar(ci) or
              self.pensionado_honorifico.buscar(ci) or
              self.pensionado_candidato.buscar(ci)):
              return
  
          self.mostrar_datos_faltadoc(dato_faltadoc)

    # operacion para consultar los datos del candidato a pensionado
    def consultar_candidato(self, ci):
        dato = self.pensionado_candidato.buscar(ci)
        if dato is None:
            print("")
        else:
            self.mostrar_datos_candidato(dato)

    # operacion que muestra en pantalla los datos del pensionado regular
    def mostrar_datos_pensionado_regular(self, data):
        print("")
        print("Datos Del Pensionado:")
        print(f"CI: {data[2]}")
        print(f"Nombre y Apellido: {data[3]}")
        print(f"Departamento: {data[0]}")
        print(f"Distrito: {data[1]}")
        print(f"Sexo: {data[4]}")
        print(f"Estado: {data[5]}")
        print(f"Fecha de Ingreso: {data[6]}")
        print(f"Com. Indigena: {data[7]}")
        print("")

    # operacion que muestra en pantalla los datos del pensionado con
    # documentos faltantes
    def mostrar_datos_faltadoc(self, data):
        print("")
        print("Datos Del Adulto Mayor:")
        print(f"CI: {data[2]}")
        print(f"Nombre y Apellido: {data[3]}")
        print(f"Departamento: {data[0]}")
        print(f"Distrito: {data[1]}")
        print("El Adulto Mayor Necesita Completar Su Documentacion")
        print("")

    # operacion que muestra en pantalla los datos del candidato a pensionado
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


# llamada a la consulta
c = Consulta()
ci = input("Ingrese el numero de cedula del adulto mayor: ")

# Validar si la entrada es un número de cedula valido
while not ci.isdigit():
    print("Por favor, ingrese solo números para el número de cédula.")
    ci = input("Ingrese el numero de cedula del adulto mayor: ")

c.consultar_regular(ci)
c.consultar_honorifico(ci)
c.consultar_faltadoc(ci)
c.consultar_candidato(ci)
