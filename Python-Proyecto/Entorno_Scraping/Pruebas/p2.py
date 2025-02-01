    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.proxy import Proxy, ProxyType
    from bs4 import BeautifulSoup
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

    # FUNCION WAIT TRUE
    def action(driver, path='', value='click'):
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
                break
            except Exception as x:
                time.sleep(1)
                continue

    def main():
        # CARGAR EL NUMERO DE JUICIO
        juicio = input(Back.WHITE + Fore.RED + "Ingresa Nro de juicio: ")
        print(Back.WHITE + Fore.BLUE + "🚀 Iniciar proceso !!")

        url = f'https://unionnegocios.com.py/sistema/juicios/datos/{juicio}'
        try:
            headers = {"Accept": "application/json"}
            response = requests.get(url)
            print(f"HTTP Status Code: {response.status_code}")
            print(f"Response Content: {response.text}")

            if response.status_code == 200:
                data = response.json()
                cedula = data['ci1']
                monto = data['monto']
                print(Back.WHITE + Fore.BLACK + f"--- CI: {data['ci1']} | DEM: {data['dem1']} | MONTO: {data['monto']} ---")
            else:
                print(f"⚠️ Error.... {response.status_code}")
                return
        except Exception as e:
            print(f"Error: {str(e)}")
            return

        print(Back.WHITE + Fore.BLUE + "⌛ procesando....")

        # Configure Chrome options
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')  
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu') 

        # Proxy configuration
        proxy = Proxy()
        proxy.proxy_type = ProxyType.DIRECT
        options.proxy = proxy

        # Initialize WebDriver
        driver = webdriver.Chrome(options=options)

        try:
            # Navigate to login page
            login_url = 'https://ingresosjudiciales.csj.gov.py/LiquidacionesWeb/loginAbogados.seam'
            driver.get(login_url)

            # Wait for driver to load
            wait = WebDriverWait(driver, 10)

            # Authentication and navigation
            action(driver, 'j_id3:username', '1591666')
            action(driver, 'j_id3:password', 'estudioAmarillaCloss2')
            action(driver, 'j_id3:submit', 'click')
            action(driver, 'iconabogadosFormId:j_id17', 'click')
            action(driver, 'iconabogadosFormId:j_id18', 'click')
            action(driver, 'juicioFormId:fechaIdInputDate', fecha_actual)

            # Add Plaintiff
            wait.until(EC.element_to_be_clickable((By.ID, 'juicioFormId:j_id59'))).click()
            tipo_doc_demandante = Select(wait.until(EC.element_to_be_clickable((By.ID, 'juicioFormId:demandantesListId:0:tipoDocumentoContribuyenteId'))))
            tipo_doc_demandante.select_by_value('1')
            time.sleep(1)
            nro_doc_demandante = driver.find_element(By.ID, 'juicioFormId:demandantesListId:0:numeroDocumentoContribuyenteId')
            nro_doc_demandante.send_keys('80111738-0')

            # Add Defendant
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[5]/td/div/div/table/tbody/tr/td[2]/table/tbody/tr[6]/td/table/tbody/tr[2]/td[1]/table/tbody/tr/td/form/span/table[1]/tbody/tr[6]/td/table/tbody/tr/td[2]/a'))).click()
            nro_doc_demandado = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[5]/td/div/div/table/tbody/tr/td[2]/table/tbody/tr[6]/td/table/tbody/tr[2]/td[1]/table/tbody/tr/td/form/span/table[1]/tbody/tr[7]/td/table/tbody/tr[2]/td[2]/input')))
            nro_doc_demandado.send_keys(cedula)

            # Add second defendant if exists
            if data.get('ci2') and data['ci2'].isdigit():
                wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[5]/td/div/div/table/tbody/tr/td[2]/table/tbody/tr[6]/td/table/tbody/tr[2]/td[1]/table/tbody/tr/td/form/span/table[1]/tbody/tr[6]/td/table/tbody/tr/td[2]/a'))).click()
                nro_doc_demandado2 = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[5]/td/div/div/table/tbody/tr[6]/td/table/tbody/tr[2]/td[1]/table/tbody/tr/td/form/span/table[1]/tbody/tr[7]/td/table/tbody/tr[2]/td[2]/input')))
                nro_doc_demandado2.send_keys(data['ci2'])

            # Add concept
            agregarConcepto = wait.until(EC.element_to_be_clickable((By.ID, 'juicioFormId:j_id109'))).click()

            # Remaining steps (concept, amount, confirmation) are kept the same as in your original script

            # Rest of the script remains unchanged...

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            driver.quit()

    if __name__ == "__main__":
        main()