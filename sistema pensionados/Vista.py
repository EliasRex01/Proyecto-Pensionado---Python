#!/usr/bin/env python3
'''
Clase vista que contiene la clase GUI que maneja la interfaz
de usuario del sistema.
'''

import tkinter as tk
from tkinter import messagebox

#------------------------------------------------------------------------------------

class GUI:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
    
    def mostrar_menu(self):
        """
        Operacion que define el contenido del menu del sistema
        """
        self.root.title("Sistema de Pensionados")
        self.root.geometry("500x400")

        marco_menu = tk.Frame(self.root)
        marco_menu.pack(pady=20)

        boton_ingresar_ci = tk.Button(marco_menu, text="Ingresar numero de cedula",
                                      command=self.mostrar_entrada_ci)
        boton_ingresar_ci.pack(pady=10)
        
        boton_salir = tk.Button(marco_menu, text="Salir", command=self.root.quit)
        boton_salir.pack(pady=10)

    def mostrar_entrada_ci(self):
        self.limpiar_ventana()

        marco_entrada_ci = tk.Frame(self.root)
        marco_entrada_ci.pack(pady=20)

        etiqueta_ci = tk.Label(marco_entrada_ci,
                               text="Ingrese el numero de cedula del adulto mayor:")
        etiqueta_ci.pack(pady=5)

        entrada_ci = tk.Entry(marco_entrada_ci)
        entrada_ci.pack(pady=5)

        boton_enviar = tk.Button(marco_entrada_ci, text="Enviar", command=lambda:
                                 self.controller.solicitar_ci(entrada_ci))
        boton_enviar.pack(pady=10)

        boton_volver = tk.Button(marco_entrada_ci, text="Volver", command=
                                 self.mostrar_menu)
        boton_volver.pack(pady=10)

    def mostrar_datos(self, data, tipo):
        self.limpiar_ventana()
        marco_datos = tk.Frame(self.root)
        marco_datos.pack(pady=20)

        if tipo == 'regular':
            self.mostrar_datos_regular(marco_datos, data)
        elif tipo == 'faltadoc':
            self.mostrar_datos_faltadoc(marco_datos, data)
        elif tipo == 'candidato':
            self.mostrar_datos_candidato(marco_datos, data)
        elif tipo == 'honorifico':
            self.mostrar_datos_honorifico(marco_datos, data)

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
        tk.Label(marco, text=f"Comunidad Indigena: {data[7]}").pack()
    
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
        tk.Label(marco, text=f"Comunidad Indigena: {data[7]}").pack()

    def mostrar_datos_honorifico(self, marco, data):
        tk.Label(marco, text="Datos Del Pensionado Honorifico:").pack()
        tk.Label(marco, text=f"CI: {data.ci}").pack()
        tk.Label(marco, text=f"Nombre y Apellido: {data.nombre_apellido}").pack()
        tk.Label(marco, text=f"Departamento: {data.departamento}").pack()
        tk.Label(marco, text=f"Distrito: {data.distrito}").pack()
        tk.Label(marco, text=f"Concepto de Pension: {data.concepto_pension}").pack()
        tk.Label(marco, text=f"Fecha de Ingreso: {data.fecha_ingreso}").pack()
        tk.Label(marco, text=f"Monto de la Pension: {data.monto_pension}").pack()

    def mostrar_error(self, mensaje):
        messagebox.showerror("Error", mensaje)

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()