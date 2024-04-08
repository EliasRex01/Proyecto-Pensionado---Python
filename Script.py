import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys

# clase base que abstrae a un pensionado (abstracta)
class Pensionado:

  def __init__(self):
    pass

  # operacion base de buscar que es usado por las otras subclases pero de multiples formas (polimorfica)
  def buscar(self, ci):
    raise NotImplementedError(
        "Este metodo debe ser implementado por las subclases")

# clase que abstrae a un pensionado regular 
class PensionadoRegular(Pensionado):

  #operacion para buscar datos de un pensionado regular, se usa directamente el json de la pagina
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
    #configurar las opciones del chromedriver
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')

    self.driver = webdriver.Chrome(options=options)
    self.driver.implicitly_wait(10)
    # implementacion de la operacion polimorfica buscar, en este caso se usa la captura de datos con selenium ya que la pagina no devuelve un tipo json o siquiera un archivo de tipo valido
  def buscar(self, ci):
    url = "https://www.mef.gov.py/portalspir/pensiondpnc.jsp"

    #abrir la pagina en el navegador
    self.driver.get(url)

    #encontrar el campo de ci y enviar el valor
    ci_input = self.driver.find_element(By.NAME, "ci")
    ci_input.send_keys(ci)
    ci_input.send_keys(Keys.RETURN)

    #esperar un tiempo suficiente para que los resultados se carguen
    time.sleep(8)

    #obtener los datos del formulario de filtro de busqueda de la pagina
    ci = self.driver.find_element(By.CSS_SELECTOR, "td[aria-describedby='list_ci']").text
    nombre_apellido = self.driver.find_element(By.CSS_SELECTOR, "td[aria-describedby='list_nombre']").text
    departamento = self.driver.find_element(By.CSS_SELECTOR, "td[aria-describedby='list_depto']").text
    distrito = self.driver.find_element(By.CSS_SELECTOR, "td[aria-describedby='list_distrito']").text
    concepto_pension = self.driver.find_element(By.CSS_SELECTOR, "td[aria-describedby='list_concepto']").text
    fecha_ingreso = self.driver.find_element(By.CSS_SELECTOR, "td[aria-describedby='list_fechaIngreso']").text
    monto_pension = self.driver.find_element(By.CSS_SELECTOR, "td[aria-describedby='list_monto']").text

    #mostrar los datos por pantalla
    print("Datos del pensionado:")
    print(f"CI: {ci}")
    print(f"Nombre: {nombre_apellido}")
    print(f"Departamento: {departamento}")
    print(f"Distrito: {distrito}")
    print(f"Concepto: {concepto_pension}")
    print(f"Fecha de Ingreso: {fecha_ingreso}")
    print(f"Monto de Pensión: {monto_pension}")

# clase que abstrae la consulta del pensionado y hace uso de la operacion buscar en sus operaciones consultar
class Consulta:

  def __init__(self):
    self.pensionado_regular = PensionadoRegular()
    self.pensionado_honorifico = PensionadoHonorifico()

  #operacion para consultar los datos del pensionado regular
  def consultar_regular(self, ci):
    dato = self.pensionado_regular.buscar(ci)
    if dato is None:
        print("")
    else:
        self.mostrar_datos_pensionado_regular(dato)

  #operacion para consultar los datos del pensionado honorifico
  def consultar_honorifico(self, ci):
    dato = self.pensionado_honorifico.buscar(ci)
    if dato is None:
        print("")


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

# llamada a la consulta
c = Consulta()
ci = input("Ingrese el numero de cedula del adulto mayor: ")

c.consultar_regular(ci)
c.consultar_honorifico(ci)