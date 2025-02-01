# se omite la configuracion manual del servicio chrome_service, permitiendo que Selenium maneje automaticamente la descarga y configuracion del chromedriver

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Configuracion de opciones para Chrome
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--headless')  # Ejecutar en modo headless 
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.ignore_local_proxy_environment_variables()

# Crear una nueva instancia de WebDriver con las opciones configuradas
driver = webdriver.Chrome(options=options)

# Define la URL para hacer scraping
url = 'https://www.example.com'  # Reemplaza con el sitio web objetivo

# Navega a la URL
driver.get(url)

# Espera explícita para que el contenido se cargue (ajusta el tiempo de espera según sea necesario)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'unique_element_id')))

# Localizar y extraer los datos deseados usando métodos de Selenium
view_details_buttons = driver.find_elements(By.CLASS_NAME, 'view_details_button')

# Cierra la ventana del navegador
driver.quit()


# https://github.com/EliasRex01/Paradigmas-Python-OOP.git