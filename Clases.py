from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from fpdf import FPDF
import time

class Scraper:
    def __init__(self):
        # Configurar el navegador Selenium
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)  # Esperar hasta 10 segundos para que los elementos aparezcan en la página

    def scrape_and_save_pdf(self, ci):
        url = "https://www.mef.gov.py/portalspir/pensiondpnc.jsp"
        
        # Abrir la página en el navegador
        self.driver.get(url)

        # Encontrar el campo de CI y enviar el valor
        ci_input = self.driver.find_element(By.NAME, "ci")
        ci_input.send_keys(ci)
        ci_input.send_keys(Keys.RETURN)

        # Esperar un tiempo suficiente para que los resultados se carguen
        time.sleep(10)  # Esperar 10 segundos (ajusta este tiempo según sea necesario)

        # Crear un archivo PDF y agregar la información
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Obtener los datos de la tabla
        ci_text = self.driver.find_element(By.CSS_SELECTOR, "td[aria-describedby='list_ci']").text
        nombre_text = self.driver.find_element(By.CSS_SELECTOR, "td[aria-describedby='list_nombre']").text
        departamento_text = self.driver.find_element(By.CSS_SELECTOR, "td[aria-describedby='list_depto']").text
        distrito_text = self.driver.find_element(By.CSS_SELECTOR, "td[aria-describedby='list_distrito']").text
        concepto_text = self.driver.find_element(By.CSS_SELECTOR, "td[aria-describedby='list_concepto']").text
        fecha_ingreso_text = self.driver.find_element(By.CSS_SELECTOR, "td[aria-describedby='list_fechaIngreso']").text
        monto_text = self.driver.find_element(By.CSS_SELECTOR, "td[aria-describedby='list_monto']").text

        # Agregar los datos al PDF
        pdf.cell(200, 10, txt="Datos del pensionado", ln=True, align="C")
        pdf.cell(200, 10, ln=True)
        pdf.cell(200, 10, txt=f"CI: {ci_text}", ln=True)
        pdf.cell(200, 10, txt=f"Nombre: {nombre_text}", ln=True)
        pdf.cell(200, 10, txt=f"Departamento: {departamento_text}", ln=True)
        pdf.cell(200, 10, txt=f"Distrito: {distrito_text}", ln=True)
        pdf.cell(200, 10, txt=f"Concepto: {concepto_text}", ln=True)
        pdf.cell(200, 10, txt=f"Fecha de Ingreso: {fecha_ingreso_text}", ln=True)
        pdf.cell(200, 10, txt=f"Monto de Pensión: {monto_text}", ln=True)

        # Guardar el PDF
        pdf_output = f"data_{ci}.pdf"
        pdf.output(pdf_output)

        print(f"Datos capturados y guardados en {pdf_output}")

# Uso de la clase Scraper
scraper = Scraper()
scraper.scrape_and_save_pdf("1234567")  # Reemplaza "1234567" con el CI que deseas buscar
