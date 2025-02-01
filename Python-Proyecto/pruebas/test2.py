# version usando url



from django.http import JsonResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time
import os
import platform
import shutil

def crear_tasa(request):
    nro_juicio = request.GET.get('nro')

    if not nro_juicio:
        return JsonResponse({'error': 'No se proporcionó un número de juicio'}, status=400)

    # Aquí puedes colocar todo el código que compartiste, adaptado a una función de Django.

    # Inicializar Selenium y realizar la automatización web
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=options)
    url = 'https://ingresosjudiciales.csj.gov.py/LiquidacionesWeb/loginAbogados.seam'
    driver.get(url)

    # Aquí agregarías el resto de tu código que realiza la automatización.
    # Por ejemplo:
    action('j_id3:username', '1591666')
    action('j_id3:password', 'estudioAmarillaCloss2')
    action('j_id3:submit', 'click')
    action('iconabogadosFormId:j_id17', 'click')
    action('iconabogadosFormId:j_id18', 'click')
    action('juicioFormId:fechaIdInputDate', datetime.now().strftime('%d/%m/%Y'))

    # Agregar Demandante
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'juicioFormId:j_id59'))).click()
    # ... (y así sucesivamente, el resto de tu código)

    driver.quit()

    return JsonResponse({'status': 'success', 'nro_juicio': nro_juicio})
