"Inventario y Facturación de la boutique Quimera"
Nombre: Fátima Ferreira
C.I.:5.228.140

Requerimientos
Es necesaria la instalación de python3.
Así también verificar que estén instalados los paquetes: transaction, ZODB,OOBTree, persistent.
Una vez verificado, se procede a ejecutar el programa desde main.py

Diseño MVC
Modelo 
Las clases relacionadas con la representación de datos y la lógica de negocio están principalmente en el archivo  tienda.py.
Lo relacionado con la gestión de productos, clientes, y los datos de la empresa, se encuentra en configuracion.py. 
Controlador 
El controlador llamado quimeracontrolador.py se encarga del tipo de transacción que se realiza al realizar una venta en la tienda. Así también como generar su respectivo comprobante.
Vista	
En interfaz.py se encuentra InterfazUsuario la cual se encarga de la interacción con el usuario mediante la terminal. Además está ConexionZODB que es la que se encarga de la persistencia de los datos del inventario.
