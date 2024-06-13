import pickle
from model import Pensionado
from category import Regular, EnProceso, Candidato, Honorifico

class PostScraping:
    def __init__(self):
        self.ps_regular = Regular()
        self.ps_faltadoc = EnProceso()
        self.ps_candidato = Candidato()
        self.ps_honorifico = Honorifico()
        self.datos_honorificos = []

    def procesar(self, ci):
        self.procesar_regular(ci)
        self.procesar_faltadoc(ci)
        self.procesar_candidato(ci)
        self.procesar_honorifico(ci)
        self.guardar_datos(ci)

    def procesar_regular(self, ci):
        pensionado = Pensionado(ci, self.ps_regular)
        dato = pensionado.buscar_categoria()
        if dato:
            self.mostrar_datos_regular(dato)

    def procesar_faltadoc(self, ci):
        p = Pensionado(ci, self.ps_faltadoc)
        dato_faltadoc = p.buscar_categoria()
        if dato_faltadoc:
            if self.ps_regular.buscar(ci) or self.ps_candidato.buscar(ci):
                return
            self.mostrar_datos_faltadoc(dato_faltadoc)

    def procesar_candidato(self, ci):
        p = Pensionado(ci, self.ps_candidato)
        dato = p.buscar_categoria()
        if dato:
            self.mostrar_datos_candidato(dato)

    def procesar_honorifico(self, ci):
        p = Pensionado(ci, self.ps_honorifico)
        dato = p.buscar_categoria()
        if dato:
            self.datos_honorificos.append(dato)
            self.mostrar_datos_honorifico(dato)

    def mostrar_datos_regular(self, data):
        print("")
        print("Datos Del Pensionado:")
        print(f"CI: {data[2]}")
        print(f"Nombre y Apellido: {data[3]}")
        print(f"Departamento: {data[0]}")
        print(f"Distrito: {data[1]}")
        print(f"Sexo: {data[4]}")
        print(f"Estado: {data[5]}")
        print(f"Fecha de Ingreso: {data[6]}")
        print(f"Comunidad Indígena: {data[7]}")
        print("")

    def mostrar_datos_faltadoc(self, data):
        print("")
        print("Datos Del Adulto Mayor:")
        print(f"CI: {data[2]}")
        print(f"Nombre y Apellido: {data[3]}")
        print(f"Departamento: {data[0]}")
        print(f"Distrito: {data[1]}")
        print("El Adulto Mayor Necesita Completar Su Documentación")
        print("")

    def mostrar_datos_candidato(self, data):
        print("")
        print("Datos Del Adulto Mayor:")
        print(f"CI: {data[2]}")
        print(f"Nombre y Apellido: {data[3]}")
        print(f"Departamento: {data[0]}")
        print(f"Distrito: {data[1]}")
        print(f"Año Del Censo: {data[5]}")
        print(f"Institución: {data[6]}")
        print(f"Situación: {data[4]}")
        print("")

    def mostrar_datos_honorifico(self, data):
        print("")
        print("Datos Del Pensionado Honorífico:")
        print(f"CI: {data.ci}")
        print(f"Nombre: {data.nombre_apellido}")
        print(f"Departamento: {data.departamento}")
        print(f"Distrito: {data.distrito}")
        print(f"Concepto: {data.concepto_pension}")
        print(f"Fecha de Ingreso: {data.fecha_ingreso}")
        print(f"Monto de Pensión: {data.monto_pension}")
        print("")

    def guardar_datos(self, ci):
        # Aquí sólo guardamos los datos honoríficos y omitimos el objeto webdriver
        filename = f"datos_{ci}.pickle"
        data_to_save = {
            'datos_honorificos': self.datos_honorificos
        }
        with open(filename, 'wb') as file:
            pickle.dump(data_to_save, file)

    @staticmethod
    def carga_datos(filename):
        with open(filename, 'rb') as file:
            data = pickle.load(file)
        ps = PostScraping()
        ps.datos_honorificos = data['datos_honorificos']
        return ps
