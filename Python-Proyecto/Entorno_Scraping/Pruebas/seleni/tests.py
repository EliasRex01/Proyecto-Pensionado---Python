from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from colorama import Fore, Back, Style, init
import time
import requests
import platform
import json
import sys
import os
import shutil
from datetime import datetime

# Inicializar colorama
init(autoreset=True)
fecha_actual = datetime.now().strftime('%d/%m/%Y')
tiempo_inicio = time.time()
sistema_operativo = platform.system()

# Configuración de opciones para Chrome
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--headless')  # Ejecutar en modo headless (sin interfaz gráfica)
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.ignore_local_proxy_environment_variables()

# Crear una nueva instancia de WebDriver con las opciones configuradas
driver = webdriver.Chrome(options=options)

# FUNCION WAIT TRUE
def action(path='', value='click'):
    while True:
        try:
            if '/' in path:
                element = driver.find_element(By.XPATH, path)
            else:
                element = driver.find_element(By.ID, path)
            if value == 'click':
                element.click()
            else:
                element.send_keys(value)
        except Exception as x:
            time.sleep(1)
            continue
        break

# CARGAR EL NUMERO DE JUICIO
juicio = input(Back.WHITE + Fore.RED + "Ingresa Nro de juicio: ")
print(Back.WHITE + Fore.BLUE + "🚀 Iniciar proceso !!")

# Obtener datos del juicio
url = f'https://unionnegocios.com.py/sistema/juicios/datos/{juicio}'
try:
    headers = {"Accept": "application/json"}
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        cedula = data['ci1']
        monto = data['monto']
        print(Back.WHITE + Fore.BLACK + f"--- CI: {data['ci1']} | DEM: {data['dem1']} | MONTO: {data['monto']}")
    else:
        print(f"\x1b[⚠️ Error.... {response.status_code}\x1b[0m")
        sys.exit()
except Exception as e:
    print(f"Error: {str(e)}")
    sys.exit()
print(Back.WHITE + Fore.BLUE + "⌛ procesando....")

# URL del sitio web que deseas procesar
url = 'https://ingresosjudiciales.csj.gov.py/LiquidacionesWeb/loginAbogados.seam'
driver.get(url)

wait = WebDriverWait(driver, 10)

# Acciones automatizadas en la web
action('j_id3:username', '1591666')
action('j_id3:password', 'estudioAmarillaCloss2')
action('j_id3:submit', 'click')
action('iconabogadosFormId:j_id17', 'click')
action('iconabogadosFormId:j_id18', 'click')
action('juicioFormId:fechaIdInputDate', fecha_actual)

# Agregar Demandante
wait.until(EC.element_to_be_clickable((By.ID, 'juicioFormId:j_id59'))).click()
tipo_doc_demandante = Select(wait.until(EC.element_to_be_clickable((By.ID, 'juicioFormId:demandantesListId:0:tipoDocumentoContribuyenteId'))))
tipo_doc_demandante.select_by_value('1')
time.sleep(1)
nro_doc_demandante = driver.find_element(By.ID, 'juicioFormId:demandantesListId:0:numeroDocumentoContribuyenteId')
nro_doc_demandante.send_keys('80111738-0')

# Agregar demandado
wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[5]/td/div/div/table/tbody/tr/td[2]/table/tbody/tr[6]/td/table/tbody/tr[2]/td[1]/table/tbody/tr/td/form/span/table[1]/tbody/tr[6]/td/table/tbody/tr/td[2]/a'))).click()
nro_doc_demandado = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[5]/td/div/div/table/tbody/tr/td[2]/table/tbody/tr[6]/td/table/tbody/tr[2]/td[1]/table/tbody/tr/td/form/span/table[1]/tbody/tr[7]/td/table/tbody/tr/td[2]/input')))
nro_doc_demandado.send_keys(cedula)

if data.get('ci2') and data['ci2'].isdigit():
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[5]/td/div/div/table/tbody/tr/td[2]/table/tbody/tr[6]/td/table/tbody/tr[2]/td[1]/table/tbody/tr/td/form/span/table[1]/tbody/tr[6]/td/table/tbody/tr/td[2]/a'))).click()
    nro_doc_demandado2 = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[5]/td/div/div/table/tbody/tr/td[2]/table/tbody/tr[6]/td/table/tbody/tr[2]/td[1]/table/tbody/tr/td/form/span/table[1]/tbody/tr[7]/td/table/tbody/tr[2]/td[2]/input')))
    nro_doc_demandado2.send_keys(data['ci2'])

# Agregar concepto y monto
agregarConcepto = wait.until(EC.element_to_be_clickable((By.ID, 'juicioFormId:j_id109'))).click()
agregarAccionPrep = wait.until(EC.element_to_be_clickable((By.NAME, 'modalPanelFormId:conceptosListId:5:j_id196'))).click()
agregarMonto = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div/div[2]/table/tbody/tr/td/form/span/div/div/div[2]/table/tbody/tr/td/div/table/tbody/tr[1]/td[5]/div/input')))
agregarMonto.send_keys(monto)
time.sleep(1)
grabar = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/div/div[2]/table/tbody/tr/td/form/table/tbody/tr/td[1]/input'))).click()

# Confirmar grabado
grabar2 = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[5]/td/div/div/table/tbody/tr/td[2]/table/tbody/tr[6]/td/table/tbody/tr[2]/td[1]/table/tbody/tr/td/form/table/tbody/tr/td/input'))).click()
time.sleep(1)
alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
alert.accept()
print(Back.WHITE + Fore.BLUE + "⚠️ Formulario aceptado")

# Descargar tasa judicial
time.sleep(1)
imprimir = driver.find_element(By.XPATH, '/html/body/table/tbody/tr[5]/td/div/div/table/tbody/tr/td[2]/table/tbody/tr[6]/td/table/tbody/tr[2]/td[1]/table/tbody/tr/td/form/table/tbody/tr/td[1]/input').click()

# Manejo de archivos descargados
carpeta_descargas = "/Users/cristianamarillacloss/Downloads"
if sistema_operativo == 'Windows':
    carpeta_descargas = r'C:\Users\Usuario\Downloads'

archivos_en_descargas = os.listdir(carpeta_descargas)
numero_mas_alto = 0
for archivo in archivos_en_descargas:
    if archivo.startswith("liquidacionJuicio") and archivo.endswith(".pdf"):
        numero_str = ''.join(filter(str.isdigit, archivo))
        if numero_str:
            numero = int(numero_str)
            numero_mas_alto = max(numero_mas_alto, numero)

nombre_archivo_mas_alto = f"liquidacionJuicio{numero_mas_alto}.pdf"
archivo_a_copiar = os.path.join(carpeta_descargas, nombre_archivo_mas_alto)
path_carpeta_destino = "/Users/cristianamarillacloss/Dropbox/CLIENTES/python"
if sistema_operativo == 'Windows':
    path_carpeta_destino = r'C:\Users\Usuario\Downloads\tasareiniciar'
carpeta_destino = os.path.join(path_carpeta_destino, f"{juicio}-tasa.pdf")
shutil.copy(archivo_a_copiar, carpeta_destino)
os.remove(archivo_a_copiar)

tiempo_fin = time.time()
duracion = round(tiempo_fin - tiempo_inicio)
print(Back.WHITE + Fore.BLUE + f"✅ 🎉 FINALIZADO. En {duracion} segundos !!!")
driver.quit()