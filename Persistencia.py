import requests
import time
import psycopg2
import tkinter as tk
from tkinter import messagebox
from abc import ABC, ABCMeta, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# Conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    dbname="nombre_db",
    user="usuario",
    password="contraseña",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Crear las tablas si no existen
cursor.execute("""
CREATE TABLE IF NOT EXISTS pensionados_regulares (
    ci VARCHAR PRIMARY KEY,
    nombre_apellido VARCHAR,
    departamento VARCHAR,
    distrito VARCHAR,
    sexo VARCHAR,
    estado VARCHAR,
    fecha_ingreso VARCHAR,
    com_indigena VARCHAR
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS pensionados_honorificos (
    ci VARCHAR PRIMARY KEY,
    nombre_apellido VARCHAR,
    departamento VARCHAR,
    distrito VARCHAR,
    concepto VARCHAR,
    fecha_ingreso VARCHAR,
    monto_pension VARCHAR
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS pensionados_en_proceso (
    ci VARCHAR PRIMARY KEY,
    nombre_apellido VARCHAR,
    departamento VARCHAR,
    distrito VARCHAR
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS pensionados_candidatos (
    ci VARCHAR PRIMARY KEY,
    nombre_apellido VARCHAR,
    departamento VARCHAR,
    distrito VARCHAR,
    situacion VARCHAR,
    ano_censo VARCHAR,
    institucion VARCHAR
);
""")
conn.commit()

# Clase base que abstrae a un pensionado (abstracta)
class Pensionado(ABC):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def buscar(self, ci):
        raise NotImplementedError("Este metodo debe ser implementado por las subclases")

# Clase que abstrae a un pensionado regular
class PensionadoRegular(Pensionado):
    def buscar(self, ci):
        cursor.execute("SELECT * FROM pensionados_regulares WHERE ci = %s", (ci,))
        data = cursor.fetchone()
        if data:
            return data

        url = "https://www.mef.gov.py/portalspir/data_lam.json"
        response = requests.get(url)
        json_data = response.json()

        for row in json_data['rows']:
            if row[2] == ci:
                cursor.execute("""
                    INSERT INTO pensionados_regulares (ci, nombre_apellido, departamento, distrito, sexo, estado, fecha_ingreso, com_indigena)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (ci) DO NOTHING;
                """, (ci, row[3], row[0], row[1], row[4], row[5], row[6], row[7]))
                conn.commit()
                return row
        return None

# Clase que abstrae a un pensionado honorifico
class PensionadoHonorifico(Pensionado):
    def __init__(self):
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)

    def buscar(self, ci):
        cursor.execute("SELECT * FROM pensionados_honorificos WHERE ci = %s", (ci,))
        data = cursor.fetchone()
        if data:
            return data

        url = "https://www.mef.gov.py/portalspir/pensiondpnc.jsp"
        self.driver.get(url)

        try:
            ci_input = self.driver.find_element(By.NAME, "ci")
            ci_input.send_keys(ci)
            ci_input.send_keys(Keys.RETURN)

            time.sleep(8)

            ci = self.driver.find_element(By.CSS_SELECTOR, "td[aria-describedby='list_ci']").text
            nombre_apellido = self.driver.find_element(By.CSS_SELECTOR, "td[aria-describedby='list_nombre']").text
            departamento = self.driver.find_element(By.CSS_SELECTOR, "td[aria-describedby='list_depto']").text
            distrito = self.driver.find_element(By.CSS_SELECTOR, "td[aria-describedby='list_distrito']").text
            concepto_pension = self.driver.find_element(By.CSS_SELECTOR, "td[aria-describedby='list_concepto']").text
            fecha_ingreso = self.driver.find_element(By.CSS_SELECTOR, "td[aria-describedby='list_fechaIngreso']").text
            monto_pension = self.driver.find_element(By.CSS_SELECTOR, "td[aria-describedby='list_monto']").text

            cursor.execute("""
                INSERT INTO pensionados_honorificos (ci, nombre_apellido, departamento, distrito, concepto, fecha_ingreso, monto_pension)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (ci) DO NOTHING;
            """, (ci, nombre_apellido, departamento, distrito, concepto_pension, fecha_ingreso, monto_pension))
            conn.commit()
            return (ci, nombre_apellido, departamento, distrito, concepto_pension, fecha_ingreso, monto_pension)
        except NoSuchElementException:
            return None

# Clase que abstrae a un pensionado en proceso
class PensionadoEnProceso(Pensionado):
    def buscar(self, ci):
        cursor.execute("SELECT * FROM pensionados_en_proceso WHERE ci = %s", (ci,))
        data = cursor.fetchone()
        if data:
            return data

        url = "https://www.mef.gov.py/portalspir/faltadoclam.json"
        response = requests.get(url)
        json_data = response.json()

        for row in json_data['rows']:
            if row[2] == ci:
                cursor.execute("""
                    INSERT INTO pensionados_en_proceso (ci, nombre_apellido, departamento, distrito)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (ci) DO NOTHING;
                """, (ci, row[3], row[0], row[1]))
                conn.commit()
                return row
        return None

# Clase que abstrae a un candidato a pensionado
class PensionadoCandidato(Pensionado):
    def buscar(self, ci):
        cursor.execute("SELECT * FROM pensionados_candidatos WHERE ci = %s", (ci,))
        data = cursor.fetchone()
        if data:
            return data

        url = "https://www.mef.gov.py/portalspir/censolam.json"
        response = requests.get(url)
        json_data = response.json()

        for row in json_data['rows']:
            if row[2] == ci:
                cursor.execute("""
                    INSERT INTO pensionados_candidatos (ci, nombre_apellido, departamento, distrito, situacion, ano_censo, institucion)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (ci) DO NOTHING;
                """, (ci, row[3], row[0], row[1], row[4], row[5], row[6]))
                conn.commit()
                return row
        return None

# Clase que abstrae la consulta del pensionado y hace uso de la operacion buscar
class Consulta:
    def __init__(self):
        self.pensionado_regular = PensionadoRegular()
        self.pensionado_honorifico = PensionadoHonorifico()
        self.pensionado_faltadoc = PensionadoEnProceso()
        self.pensionado_candidato = PensionadoCandidato()

    def consultar_regular(self, ci):
        return self.pensionado_regular.buscar(ci)

    def consultar_honorifico(self, ci):
        return self.pensionado_honorifico.buscar(ci)

    def consultar_faltadoc(self, ci):
        return self.pensionado_faltadoc.buscar(ci)

    def consultar_candidato(self, ci):
        return self.pensionado_candidato.buscar(ci)

# Interfaz gráfica con tkinter
def buscar_ci():
    ci = ci_entry.get()
    if not ci.isdigit():
        messagebox.showerror("Error", "Por favor, ingrese solo números para el número de cédula.")
        return

    consulta = Consulta()
    resultado = {
        "regular": consulta.consultar_regular(ci),
        "honorifico": consulta.consultar_honorifico(ci),
        "faltadoc": consulta.consultar_faltadoc(ci),
        "candidato": consulta.consultar_candidato(ci),
    }

    resultados_text.delete(1.0, tk.END)
    for tipo, data in resultado.items():
        if data:
            resultados_text.insert(tk.END, f"\n{tipo.upper()}:\n")
            resultados_text.insert(tk.END, f"CI: {data[0]}\n", "bold")
            resultados_text.insert(tk.END, f"Nombre y Apellido: {data[1]}\n")
            resultados_text.insert(tk.END, f"Departamento: {data[2]}\n")
            resultados_text.insert(tk.END, f"Distrito: {data[3]}\n")
            if tipo == "regular":
                resultados_text.insert(tk.END, f"Sexo: {data[4]}\n")
                resultados_text.insert(tk.END, f"Estado: {data[5]}\n")
                resultados_text.insert(tk.END, f"Fecha de Ingreso: {data[6]}\n")
                resultados_text.insert(tk.END, f"Com. Indigena: {data[7]}\n")
            elif tipo == "honorifico":
                resultados_text.insert(tk.END, f"Concepto: {data[4]}\n")
                resultados_text.insert(tk.END, f"Fecha de Ingreso: {data[5]}\n")
                resultados_text.insert(tk.END, f"Monto de Pensión: {data[6]}\n")
            elif tipo == "faltadoc":
                resultados_text.insert(tk.END, "El Adulto Mayor Necesita Completar Su Documentación\n")
            elif tipo == "candidato":
                resultados_text.insert(tk.END, f"Situación: {data[4]}\n")
                resultados_text.insert(tk.END, f"Año del Censo: {data[5]}\n")
                resultados_text.insert(tk.END, f"Institución: {data[6]}\n")

def crear_interfaz():
    global ci_entry, resultados_text
    ventana = tk.Tk()
    ventana.title("Consulta de Pensionados")

    tk.Label(ventana, text="Ingrese el número de cédula del adulto mayor:").pack()
    ci_entry = tk.Entry(ventana)
    ci_entry.pack()

    tk.Button(ventana, text="Buscar", command=buscar_ci).pack()

    resultados_text = tk.Text(ventana, wrap="word")
    resultados_text.pack()

    resultados_text.tag_configure("bold", font=("Helvetica", 10, "bold"))

    ventana.mainloop()

crear_interfaz()

# Cerrar la conexión a la base de datos al terminar el uso
cursor.close()
conn.close()
