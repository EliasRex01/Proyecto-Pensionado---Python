# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('scrape/', views.scrape_view, name='scrape_view'),
]

# views.py
from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

def scrape_view(request):
    # Configurar el navegador
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Para ejecutar Chrome en modo sin cabeza (headless)
    driver = webdriver.Chrome(options=chrome_options)  # O webdriver.Firefox() si estás usando Firefox
    driver.get("https://www.mef.gov.py/portalspir/lamdpnc.jsp")

    # Obtener el CI de la solicitud POST
    ci = request.POST.get('ci')

    # Encontrar el campo CI e ingresar el número
    ci_input = driver.find_element_by_id("id_del_campo_ci")
    ci_input.send_keys(ci)

    # Simular clic en el botón de búsqueda
    search_button = driver.find_element_by_id("id_del_boton_de_busqueda")
    search_button.click()

    # Esperar a que la página cargue los resultados
    time.sleep(5)  # Puedes ajustar este tiempo según la velocidad de carga de la página

    # Capturar el contenido de los campos
    campo1 = driver.find_element_by_id("id_del_campo_1").text
    campo2 = driver.find_element_by_id("id_del_campo_2").text
    # Añadir más campos según sea necesario

    # Crear el archivo PDF
    file_path = os.path.join("ruta_de_la_carpeta_local", "resultado.pdf")
    with open(file_path, "w") as f:
        f.write(f"Campo 1: {campo1}\n")
        f.write(f"Campo 2: {campo2}\n")
        # Escribir más campos según sea necesario

    # Cerrar el navegador
    driver.quit()

    # Devolver una respuesta adecuada, por ejemplo, un mensaje de éxito
    return HttpResponse("Web scraping completado con éxito. Archivo PDF guardado en la carpeta local.")
