Nombre del software: Inventario y facturacion de Quimera Boutique
Nombre: Fatima Ferreira
CI: 5.228.140

Requerimientos del Sistema con interfaz gráfica:
Instalacion de Python3
BTrees, persistent, re, transaction, ZODB
Ejecutar main_grafica.py

El menu cuenta con las opciones de agregar producto, devolver producto, realizar venta e imprimir inventario

Ejemplos
Agregar productos
bd.agregar_producto(nombre, precio, stock)
bd.agregar_producto('Camisa', 50000, 20)
bd.agregar_producto('Pantalon', 80000, 25)
bd.agregar_producto('Vestido', 120000, 25)


Realizar venta
Para factura
cliente = Cliente(nombre_cliente, direccion_cliente, telefono_cliente, ruc_cliente)
cliente = Cliente(Juan Ortiz, Santa Ana, 0981456982, 0123456789)
productos_vendidos = {codigo_producto: cantidad}

Para recibo
cliente = Cliente(nombre_cliente, direccion_cliente, telefono_cliente)
cliente = Cliente(Fatima, Avenida Ortiz Guerrero, 0981487215)
productos_vendidos = {codigo_producto: cantidad}
productos_vendidos = {1: 2}


Devolver producto
devolver_producto_interfaz(codigo_producto, cantidad)
devolver_producto_interfaz(3, 1)
