import requests
from model import Categoria, HonorificoData

class Regular(Categoria):
    def buscar(self, ci):
        url = "https://www.mef.gov.py/portalspir/data_lam.json"
        response = requests.get(url)
        json_data = response.json()

        for row in json_data['rows']:
            if row[2] == ci:
                return row

        return None

class Honorifico(Categoria):
    def __init__(self):
        self.driver = None

    def setup_driver(self):
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

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

        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        from selenium.common.exceptions import NoSuchElementException
        import time

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

class EnProceso(Categoria):
    def buscar(self, ci):
        url = "https://www.mef.gov.py/portalspir/faltadoclam.json"
        response = requests.get(url)
        json_data = response.json()

        for row in json_data['rows']:
            if row[2] == ci:
                return row

        return None

class Candidato(Categoria):
    def buscar(self, ci):
        url = "https://www.mef.gov.py/portalspir/censolam.json"
        response = requests.get(url)
        json_data = response.json()

        for row in json_data['rows']:
            if row[2] == ci:
                return row

        return None
