import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuración de opciones para Chrome
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--headless')  # Ejecutar en modo headless (sin interfaz gráfica)
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.ignore_local_proxy_environment_variables()

# Crear una nueva instancia de WebDriver con las opciones configuradas
driver = webdriver.Chrome(options=options)

# Define la URL para hacer scraping
url = 'https://www.example.com'  # Reemplaza con el sitio web objetivo

try:
    # Navegar a la URL
    driver.get(url)
    logging.info(f"Navegando a la URL: {url}")

    # Espera explícita para que el contenido se cargue (ajusta el tiempo de espera según sea necesario)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'unique_element_id')))
    logging.info("Elemento encontrado en la página")

    # Localizar y extraer los datos deseados usando métodos de Selenium
    view_details_buttons = driver.find_elements(By.CLASS_NAME, 'view_details_button')

except TimeoutException:
    logging.error("No se pudo encontrar el elemento dentro del tiempo especificado. Asegúrate de que el elemento existe y la página se haya cargado correctamente.")
except Exception as e:
    logging.error(f"Ocurrió un error inesperado: {e}")
finally:
    # Cierra la ventana del navegador
    driver.quit()
    logging.info("Navegador cerrado")
