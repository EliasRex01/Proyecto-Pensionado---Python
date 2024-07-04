"Ahí comprendí yo, entonces
que la ciencia, no es tan ciencia
cuando no tiene conciencia."
    C. Martinez Paiva. Que me perdone la ciencia

Nombre del software: "Facturación para una Peluquería" apodado FP
Nombre: Andrea Elizabeth Mercado Salinas
CI: 5.662.583



Requerimientos del Sistema:
Los Requerimientos para correr FP se debe de tener instalado Pyhton3


════ ∘◦❁◦∘ ════ ════ ∘◦❁◦∘ ════ ════ ∘◦❁◦∘ ════ ════ ∘◦❁◦∘ ════ ════ ∘◦❁◦∘ ════ 
                        Pasos para la ejecucion del software FP
════ ∘◦❁◦∘ ════ ════ ∘◦❁◦∘ ════ ════ ∘◦❁◦∘ ════ ════ ∘◦❁◦∘ ════ ════ ∘◦❁◦∘ ════ 
1. Verificar si se tiene instalado:
BTrees, persistent, re, transaction, ZODB, zope.interface   
2. Verificar la direccion para la base de datos. En main.py linea 9. conexionBD = conexion("TU_RUTA/datos_persistentes/datos_de_FP.fs")
3. Ejecutar el main.py


════ ∘◦❁◦∘ ════ ════ ∘◦❁◦∘ ════ ════ ∘◦❁◦∘ ════ ════ ∘◦❁◦∘ ════ ════ ∘◦❁◦∘ ════ 
                                CODIGO DE TERCEROS
════ ∘◦❁◦∘ ════ ════ ∘◦❁◦∘ ════ ════ ∘◦❁◦∘ ════ ════ ∘◦❁◦∘ ════ ════ ∘◦❁◦∘ ════ 
___La siguiente sección de código para validar el formato del teléfono fue proporcionada por ChatGPT:
""
telefono = input("Teléfono del cliente (formato: 09xx-xxx-xxx): ")
if re.match(r'^09\d{2}-\d{3}-\d{3}$', telefono):
    break
""
___ChatGPT ayudo a la hora de elaborar la clase ConexionZODB.


════ ∘◦❁◦∘ ════ ════ ∘◦❁◦∘ ════ ════ ∘◦❁◦∘ ════ ════ ∘◦❁◦∘ ════ ════ ∘◦❁◦∘ ════ 
        Ejemplo de inicializacion para el guardado de objeto peluqueria
════ ∘◦❁◦∘ ════ ════ ∘◦❁◦∘ ════ ════ ∘◦❁◦∘ ════ ════ ∘◦❁◦∘ ════ ════ ∘◦❁◦∘ ════ 

Factura para el negocio:
    factura_negocio= Factura("15487930","abril 2024")

Pelquero 1:
    Francisco = Peluquero(cedula="1234567890", nombres="Francisco", apellidos="Mercado", telefono="0987-654-321")

Pelquero 2:
    Federico = Peluquero(cedula="0987654321", nombres="Federico", apellidos="Martínez", telefono="0999-801-742")

Creacion de cortes:
    corte_clasico_1 = CorteClasico("CC1", "Estilo militar", "Este corte clásico se caracteriza por ser un corte corto y uniforme, similar a un estilo militar. Es ideal para un aspecto limpio y ordenado.")
    corte_clasico_2 = CorteClasico("CC2", "Tupé", "El corte clásico de "Tupé" presenta un cabello más largo en la parte superior que puede peinarse hacia atrás o a los lados, creando un aspecto elegante y atemporal.")

    corte_moderno_1 = CorteModerno("CM1", "BuzzCut", "El "BuzzCut" es un corte de cabello extremadamente corto y uniforme. Es un corte moderno y bajo mantenimiento, ideal para quienes prefieren un estilo práctico.")
    corte_moderno_2 = CorteModerno("CM2", "Fade", "El corte "Fade" es un estilo moderno que combina una longitud corta en los lados y la parte posterior con un cabello más largo en la parte superior.")
    corte_moderno_3 = CorteModerno("CM3", "Mullet", "El "Mullet" es un corte moderno que se caracteriza por ser más largo en la parte posterior y los lados, mientras que la parte superior se mantiene corta. ")

    corte_infantil_1 = CorteInfantil("CI1", "Crewcut", " El "Crewcut" es un corte infantil que se caracteriza por ser corto y uniforme en todo el cabello. ")
    corte_infantil_2 = CorteInfantil("CI2", "Spiky Hair", "El "Spiky Hair" es un corte infantil que permite peinar el cabello hacia arriba para lograr un aspecto de puntas levantadas y divertidas. ")

Agregar cortes a peluqueros:
    Francisco.agregar_corte_a_catalogo(corte_clasico_1)
    Francisco.agregar_corte_a_catalogo(corte_moderno_1)
    Francisco.agregar_corte_a_catalogo(corte_moderno_2)
    Francisco.agregar_corte_a_catalogo(corte_moderno_3)
    Federico.agregar_corte_a_catalogo(corte_clasico_1)
    Federico.agregar_corte_a_catalogo(corte_clasico_2)
    Federico.agregar_corte_a_catalogo(corte_moderno_1)
    Federico.agregar_corte_a_catalogo(corte_infantil_1)
    Federico.agregar_corte_a_catalogo(corte_infantil_2)

Creacion de usuarios para peluqueros:
    peluqueroAdmin=Administrador(Francisco,"admin","1234")
    peluqueroNormal=Cajero(Federico,"fede01","1234")
    axel_gomez = Cliente(cedula="4887143", nombres="Axel", apellidos="Gómez", telefono="0999-111-111", ruc="1234567890")
    carlos_barrios = Cliente(cedula="2115897", nombres="Carlos", apellidos="Barrios", telefono="0999-222-222", ruc="9876543210")
    alexander_barreto = Cliente(cedula="4987423", nombres="Alexander", apellidos="Barreto", telefono="0999-333-333", ruc="1111111111")
    peluqueriaFM1= Peluqueria("FM", "5112395-4", "San salvador y chile", factura_negocio)
    peluqueriaFM1.agregar_cliente(axel_gomez)
    peluqueriaFM1.agregar_cliente(carlos_barrios)
    peluqueriaFM1.agregar_cliente(alexander_barreto)
    peluqueriaFM1.agregar_usuarios(peluqueroAdmin)
    peluqueriaFM1.agregar_usuarios(peluqueroNormal)
    conexionBD.guardar_peluqueria(peluqueriaFM1)




Copie y pegue rapido ->

    factura_negocio= Factura("15487930","abril 2024")
    Francisco = Peluquero(cedula="1234567890", nombres="Francisco", apellidos="Mercado", telefono="0987-654-321")
    Federico = Peluquero(cedula="0987654321", nombres="Federico", apellidos="Martínez", telefono="0999-801-742")
    corte_clasico_1 = CorteClasico("CC1", "Estilo militar", "Este corte clásico se caracteriza por ser un corte corto y uniforme, similar a un estilo militar. Es ideal para un aspecto limpio y ordenado.")
    corte_clasico_2 = CorteClasico("CC2", "Tupé", "El corte clásico de Tupé presenta un cabello más largo en la parte superior que puede peinarse hacia atrás o a los lados, creando un aspecto elegante y atemporal.")
    corte_moderno_1 = CorteModerno("CM1", "BuzzCut", "El BuzzCut es un corte de cabello extremadamente corto y uniforme. Es un corte moderno y bajo mantenimiento, ideal para quienes prefieren un estilo práctico.")
    corte_moderno_2 = CorteModerno("CM2", "Fade", "El corte Fade es un estilo moderno que combina una longitud corta en los lados y la parte posterior con un cabello más largo en la parte superior.")
    corte_moderno_3 = CorteModerno("CM3", "Mullet", "El Mullet es un corte moderno que se caracteriza por ser más largo en la parte posterior y los lados, mientras que la parte superior se mantiene corta. ")
    corte_infantil_1 = CorteInfantil("CI1", "Crewcut", " El Crewcut es un corte infantil que se caracteriza por ser corto y uniforme en todo el cabello. ")
    corte_infantil_2 = CorteInfantil("CI2", "Spiky Hair", "El Spiky Hair es un corte infantil que permite peinar el cabello hacia arriba para lograr un aspecto de puntas levantadas y divertidas. ")
    Francisco.agregar_corte_a_catalogo(corte_clasico_1)
    Francisco.agregar_corte_a_catalogo(corte_moderno_1)
    Francisco.agregar_corte_a_catalogo(corte_moderno_2)
    Francisco.agregar_corte_a_catalogo(corte_moderno_3)
    Federico.agregar_corte_a_catalogo(corte_clasico_1)
    Federico.agregar_corte_a_catalogo(corte_clasico_2)
    Federico.agregar_corte_a_catalogo(corte_moderno_1)
    Federico.agregar_corte_a_catalogo(corte_infantil_1)
    Federico.agregar_corte_a_catalogo(corte_infantil_2)
    peluqueroAdmin=Administrador(Francisco,"admin","1234")
    peluqueroNormal=Cajero(Federico,"fede01","1234")
    axel_gomez = Cliente(cedula="4887143", nombres="Axel", apellidos="Gómez", telefono="0999-111-111", ruc="1234567890")
    carlos_barrios = Cliente(cedula="2115897", nombres="Carlos", apellidos="Barrios", telefono="0999-222-222", ruc="9876543210")
    alexander_barreto = Cliente(cedula="4987423", nombres="Alexander", apellidos="Barreto", telefono="0999-333-333", ruc="1111111111")
    peluqueriaFM1= Peluqueria("FM", "5112395-4", "San salvador y chile", factura_negocio)
    peluqueriaFM1.agregar_cliente(axel_gomez)
    peluqueriaFM1.agregar_cliente(carlos_barrios)
    peluqueriaFM1.agregar_cliente(alexander_barreto)
    peluqueriaFM1.agregar_usuarios(peluqueroAdmin)
    peluqueriaFM1.agregar_usuarios(peluqueroNormal)
    conexionBD.guardar_peluqueria(peluqueriaFM1)