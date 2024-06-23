import requests
import pickle
import time
from abc import ABCMeta, abstractmethod
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class GUI:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

    def mostrar_menu(self):
        self.root.title("Sistema de Pensionados")
        self.root.geometry("500x400")

        marco_menu = tk.Frame(self.root)
        marco_menu.pack(pady=20)

        boton_ingresar_ci = tk.Button(marco_menu, text="Ingresar número de cédula", command=self.mostrar_entrada_ci)
        boton_ingresar_ci.pack(pady=10)

        boton_salir = tk.Button(marco_menu, text="Salir", command=self.root.quit)
        boton_salir.pack(pady=10)

    def mostrar_entrada_ci(self):
        self.limpiar_ventana()

        marco_entrada_ci = tk.Frame(self.root)
        marco_entrada_ci.pack(pady=20)

        etiqueta_ci = tk.Label(marco_entrada_ci, text="Ingrese el número de cédula del adulto mayor:")
        etiqueta_ci.pack(pady=5)

        self.entrada_ci = tk.Entry(marco_entrada_ci)
        self.entrada_ci.pack(pady=5)

        boton_enviar = tk.Button(marco_entrada_ci, text="Enviar", command=lambda: self.controller.solicitar_ci(self.entrada_ci))
        boton_enviar.pack(pady=10)

        boton_volver = tk.Button(marco_entrada_ci, text="Volver", command=self.mostrar_menu)
        boton_volver.pack(pady=10)

    def mostrar_error(self, mensaje):
        self.limpiar_ventana()

        marco_error = tk.Frame(self.root)
        marco_error.pack(pady=20)

        etiqueta_error = tk.Label(marco_error, text=mensaje, fg="red")
        etiqueta_error.pack(pady=5)

        boton_volver = tk.Button(marco_error, text="Volver", command=self.mostrar_entrada_ci)
        boton_volver.pack(pady=10)

    def mostrar_datos(self, data, tipo):
        self.limpiar_ventana()
        marco_datos = tk.Frame(self.root)
        marco_datos.pack(pady=20)

        if tipo == 'regular':
            self.mostrar_datos_regular(marco_datos, data)
        elif tipo == 'honorifico':
            self.mostrar_datos_honorifico(marco_datos, data)
        elif tipo == 'faltadoc':
            self.mostrar_datos_faltadoc(marco_datos, data)
        elif tipo == 'candidato':
            self.mostrar_datos_candidato(marco_datos, data)

        boton_volver = tk.Button(marco_datos, text="Volver", command=self.mostrar_menu)
        boton_volver.pack(pady=10)

    def mostrar_datos_regular(self, marco, data):
        tk.Label(marco, text="Datos del pensionado:").pack()
        tk.Label(marco, text=f"CI: {data[2]}").pack()
        tk.Label(marco, text=f"Nombre y Apellido: {data[3]}").pack()
        tk.Label(marco, text=f"Departamento: {data[0]}").pack()
        tk.Label(marco, text=f"Distrito: {data[1]}").pack()
        tk.Label(marco, text=f"Sexo: {data[4]}").pack()
        tk.Label(marco, text=f"Estado: {data[5]}").pack()
        tk.Label(marco, text=f"Fecha de Ingreso: {data[6]}").pack()
        tk.Label(marco, text=f"Comunidad Indígena: {data[7]}").pack()

    def mostrar_datos_honorifico(self, marco, data):
        tk.Label(marco, text="Datos Del Pensionado Honorífico:").pack()
        tk.Label(marco, text=f"CI: {data.ci}").pack()
        tk.Label(marco, text=f"Nombre y Apellido: {data.nombre_apellido}").pack()
        tk.Label(marco, text=f"Departamento: {data.departamento}").pack()
        tk.Label(marco, text=f"Distrito: {data.distrito}").pack()
        tk.Label(marco, text=f"Concepto de Pensión: {data.concepto_pension}").pack()
        tk.Label(marco, text=f"Fecha de Ingreso: {data.fecha_ingreso}").pack()
        tk.Label(marco, text=f"Monto de la Pensión: {data.monto_pension}").pack()

    def mostrar_datos_faltadoc(self, marco, data):
        tk.Label(marco, text="Datos Del Adulto Mayor:").pack()
        tk.Label(marco, text=f"CI: {data[2]}").pack()
        tk.Label(marco, text=f"Nombre y Apellido: {data[3]}").pack()
        tk.Label(marco, text=f"Departamento: {data[0]}").pack()
        tk.Label(marco, text=f"Distrito: {data[1]}").pack()
        tk.Label(marco, text="El Adulto Mayor Necesita Completar Documentos").pack()

    def mostrar_datos_candidato(self, marco, data):
        tk.Label(marco, text="Datos Del Adulto Mayor:").pack()
        tk.Label(marco, text=f"CI: {data[2]}").pack()
        tk.Label(marco, text=f"Nombre y Apellido: {data[3]}").pack()
        tk.Label(marco, text=f"Departamento: {data[0]}").pack()
        tk.Label(marco, text=f"Distrito: {data[1]}").pack()
        tk.Label(marco, text=f"Sexo: {data[4]}").pack()
        tk.Label(marco, text=f"Estado: {data[5]}").pack()
        tk.Label(marco, text=f"Fecha de Ingreso: {data[6]}").pack()
        tk.Label(marco, text=f"Comunidad Indígena: {data[7]}").pack()

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class Persona(metaclass=ABCMeta):
    def __init__(self, ci):
        self.ci = ci

class Pensionado(Persona):
    def __init__(self, ci, categoria):
        super().__init__(ci)
        self.categoria = categoria

    def buscar_categoria(self):
        return self.categoria.buscar(self.ci)

class Categoria(metaclass=ABCMeta):
    @abstractmethod
    def buscar(self, ci):
        raise NotImplementedError("La operación debe ser implementada")

class Regular(Categoria):
    def buscar(self, ci):
        url = "https://www.mef.gov.py/portalspir/data_lam.json"
        response = requests.get(url)
        if response.status_code != 200:
            raise CedulaNoExisteException("Error al consultar la base de datos de Regular")
        try:
            json_data = response.json()
        except ValueError:
            raise CedulaNoExisteException("Error al decodificar la respuesta de Regular")
        print(f"Buscando en Regular: {ci}")

        for row in json_data['rows']:
            if row[2] == ci:
                print(f"Encontrado en Regular: {row}")
                return row

        raise CedulaNoExisteException("El número de cédula no existe")

class Honorifico(Categoria):
    def __init__(self):
        self.driver = None

    def setup_driver(self):
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
        print(f"Buscando en Honorifico: {ci}")

        try:
            ci_input = self.driver.find_element(By.NAME, "ci")
            ci_input.send_keys(ci)
            ci_input.send_keys(Keys.RETURN)
            time.sleep(8)

            ci = self.driver.find_element(By.CSS_SELECTOR, "td[aria-describedby='tabla_cedula']")

            if ci is not None:
                honorifico_data = HonorificoData(
                    ci.text,
                    self.driver.find_element(By.CSS_SELECTOR, "td[aria-describedby='tabla_nombreapellido']").text,
                    self.driver.find_element(By.CSS_SELECTOR, "td[aria-describedby='tabla_dpto']").text,
                    self.driver.find_element(By.CSS_SELECTOR, "td[aria-describedby='tabla_distrito']").text,
                    self.driver.find_element(By.CSS_SELECTOR, "td[aria-describedby='tabla_concepto_pension']").text,
                    self.driver.find_element(By.CSS_SELECTOR, "td[aria-describedby='tabla_fechaingreso']").text,
                    self.driver.find_element(By.CSS_SELECTOR, "td[aria-describedby='tabla_monto_pension']").text,
                )
                print(f"Encontrado en Honorifico: {honorifico_data}")
                return honorifico_data

        except NoSuchElementException:
            print("No encontrado en Honorifico")

        raise CedulaNoExisteException("El número de cédula no existe en honoríficos")

class HonorificoData:
    def __init__(self, ci, nombre_apellido, departamento, distrito, concepto_pension, fecha_ingreso, monto_pension):
        self.ci = ci
        self.nombre_apellido = nombre_apellido
        self.departamento = departamento
        self.distrito = distrito
        self.concepto_pension = concepto_pension
        self.fecha_ingreso = fecha_ingreso
        self.monto_pension = monto_pension

    def __repr__(self):
        return f"HonorificoData(ci={self.ci}, nombre_apellido={self.nombre_apellido}, departamento={self.departamento}, distrito={self.distrito}, concepto_pension={self.concepto_pension}, fecha_ingreso={self.fecha_ingreso}, monto_pension={self.monto_pension})"

class EnProceso(Categoria):
    def buscar(self, ci):
        url = "https://www.mef.gov.py/portalspir/data_proc.json"
        response = requests.get(url)
        if response.status_code != 200:
            raise CedulaNoExisteException("Error al consultar la base de datos de En Proceso")
        try:
            json_data = response.json()
        except ValueError:
            raise CedulaNoExisteException("Error al decodificar la respuesta de En Proceso")
        print(f"Buscando en EnProceso: {ci}")

        for row in json_data['rows']:
            if row[2] == ci:
                print(f"Encontrado en EnProceso: {row}")
                return row

        raise CedulaNoExisteException("El número de cédula no existe en En Proceso")

class Candidato(Categoria):
    def buscar(self, ci):
        url = "https://www.mef.gov.py/portalspir/data_proc_cand.json"
        response = requests.get(url)
        if response.status_code != 200:
            raise CedulaNoExisteException("Error al consultar la base de datos de Candidato")
        try:
            json_data = response.json()
        except ValueError:
            raise CedulaNoExisteException("Error al decodificar la respuesta de Candidato")
        print(f"Buscando en Candidato: {ci}")

        for row in json_data['rows']:
            if row[2] == ci:
                print(f"Encontrado en Candidato: {row}")
                return row

        raise CedulaNoExisteException("El número de cédula no existe en Candidato")

class CedulaNoExisteException(Exception):
    def __init__(self, message):
        self.message = message

class CedulaNoValidaException(Exception):
    def __init__(self, message):
        self.message = message

class Menu:
    def __init__(self, root, ps):
        self.root = root
        self.ps = ps

    def mostrar_menu(self):
        self.ps.gui.mostrar_menu()

    def solicitar_ci(self, entrada_ci):
        ci = entrada_ci.get().strip()
        try:
            self.ps.procesar(ci)
        except (CedulaNoExisteException, CedulaNoValidaException) as e:
            messagebox.showerror("Error", e.message)
            self.ps.gui.mostrar_error(e.message)

class PostScraping:
    def __init__(self, gui):
        self.ps_regular = Regular()
        self.ps_faltadoc = EnProceso()
        self.ps_candidato = Candidato()
        self.ps_honorifico = Honorifico()
        self.datos_honorificos = []
        self.gui = gui  # Guardar el objeto GUI

    def procesar(self, ci):
        encontrado = False
        datos = None
        tipo = None
        try:
            print(f"Procesando cédula: {ci}")
            if not ci.isdigit():
                raise CedulaNoValidaException("La cédula debe ser numérica")
            datos, tipo = self.procesar_regular(ci)
            if not datos:
                datos, tipo = self.procesar_faltadoc(ci)
            if not datos:
                datos, tipo = self.procesar_candidato(ci)
            if not datos:
                datos, tipo = self.procesar_honorifico(ci)

            if datos:
                self.guardar_datos(ci, datos, tipo)
            else:
                raise CedulaNoExisteException("El número de cédula no existe")
        except (CedulaNoExisteException, CedulaNoValidaException) as e:
            raise e

    def procesar_regular(self, ci):
        try:
            dato = self.ps_regular.buscar(ci)
            if dato:
                self.gui.mostrar_datos(dato, 'regular')
                return dato, 'regular'
        except CedulaNoExisteException:
            pass
        return None, None

    def procesar_honorifico(self, ci):
        try:
            dato = self.ps_honorifico.buscar(ci)
            if dato:
                self.datos_honorificos.append(dato)
                self.gui.mostrar_datos(dato, 'honorifico')
                return dato, 'honorifico'
        except CedulaNoExisteException:
            pass
        return None, None

    def procesar_faltadoc(self, ci):
        try:
            dato = self.ps_faltadoc.buscar(ci)
            if dato and not (self.ps_regular.buscar(ci) or self.ps_candidato.buscar(ci)):
                self.gui.mostrar_datos(dato, 'faltadoc')
                return dato, 'faltadoc'
        except CedulaNoExisteException:
            pass
        return None, None

    def procesar_candidato(self, ci):
        try:
            dato = self.ps_candidato.buscar(ci)
            if dato:
                self.gui.mostrar_datos(dato, 'candidato')
                return dato, 'candidato'
        except CedulaNoExisteException:
            pass
        return None, None

    def guardar_datos(self, ci, datos, tipo):
        filename = f"datos_{tipo}_{ci}.pickle"
        with open(filename, 'wb') as file:
            pickle.dump(datos, file)

    @classmethod
    def carga_datos(cls, filename):
        with open(filename, 'rb') as file:
            data = pickle.load(file)
        ps = cls()
        ps.datos_honorificos = data['datos_honorificos']
        return ps

def main():
    """
    Operación main principal que invoca el sistema
    """
    root = tk.Tk()
    gui = GUI(root, None)
    ps = PostScraping(gui)
    objeto_menu = Menu(root, ps)
    gui.controller = objeto_menu
    objeto_menu.mostrar_menu()
    root.mainloop()

if __name__ == '__main__':
    main()
