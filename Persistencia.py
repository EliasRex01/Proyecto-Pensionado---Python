# logica adaptada a la persistencia de datos

        print(f"CI: {data[2]}")
        print(f"Nombre y Apellido: {data[3]}")
        print(f"Departamento: {data[0]}")
        print(f"Distrito: {data[1]}")
        print(f"Sexo: {data[4]}")
        print(f"Estado: {data[5]}")
        print(f"Fecha de Ingreso: {data[6]}")
        print(f"Com. Indigena: {data[7]}")
        print("")

    # operacion que muestra en pantalla los datos del pensionado con
    # documentos faltantes
    def mostrar_datos_faltadoc(self, data):
        print("")
        print("Datos Del Adulto Mayor:")
        print(f"CI: {data[2]}")
        print(f"Nombre y Apellido: {data[3]}")
        print(f"Departamento: {data[0]}")
        print(f"Distrito: {data[1]}")
        print("El Adulto Mayor Necesita Completar Su Documentacion")
        print("")

    # operacion que muestra en pantalla los datos del candidato a pensionado
    def mostrar_datos_candidato(self, data):
        print("")
        print("Datos Del Adulto Mayor:")
        print(f"CI: {data[2]}")
        print(f"Nombre y Apellido: {data[3]}")
        print(f"Departamento: {data[0]}")
        print(f"Distrito: {data[1]}")
        print(f"Año Del Censo: {data[5]}")
        print(f"Institucion: {data[6]}")
        print(f"Situacion: {data[4]}")
        print("")


# llamada a la consulta
c = Consulta()
ci = input("Ingrese el numero de cedula del adulto mayor: ")

# Validar si la entrada es un número de cedula valido
while not ci.isdigit():
    print("Por favor, ingrese solo números para el número de cédula.")
    ci = input("Ingrese el numero de cedula del adulto mayor: ")

c.consultar_regular(ci)
c.consultar_honorifico(ci)
c.consultar_faltadoc(ci)
c.consultar_candidato(ci)
