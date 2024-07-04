
from ZODB import FileStorage, DB
import transaction
from tkinter import *
from tkinter import font, messagebox
from Controlador.quimeracontrolador import Factura, Recibo
from Modelo.tienda import Tienda
from Modelo.configuracion import Producto,Cliente
from tkinter import Radiobutton, StringVar


class QuimeraBoutiqueApp(Frame):
    def __init__(self, master=None, tienda=None,root=None,base_de_datos=None):
        Frame.__init__(self, master)
        self.master = master
        master.title("Quimera Boutique")
        master.geometry('985x770')
        master.resizable(0, 0)
        master.configure(bg='lightgray')

        self.tienda = tienda if tienda else Tienda(db=base_de_datos)  # Pasa la conexión de la base de datos a la tienda
        self.base_de_datos = base_de_datos  # Almacena la conexión a la base de datos

        self.base_de_datos = base_de_datos
        ##self.root = root()
        self.init_widgets()



    def init_widgets(self):
        self.titulo = Label(self.master, text='Quimera Boutique', font=('Arial', 40, "bold"))
        self.titulo.config(background='#E3CDCB', fg='#806D79')
        self.titulo.place(x=270, y=150)

        custom_font = font.Font(family="Helvetica", size=24)


        self.agregar_button = Button(self.master, text="Agregar\n Producto", font=custom_font, command=self.agregar_producto)
        self.agregar_button.place(x=250, y=300)

        self.venta_button = Button(self.master, text="Realizar\n Venta", command=self.realizar_venta, font=custom_font)
        self.venta_button.place(x=250, y=500)

        self.devolucion_button = Button(self.master, text="Realizar\n Devolución", command=self.realizar_devolucion,
                                      font=custom_font)
        self.devolucion_button.place(x=500, y=300)

        self.inventario_button = Button(self.master, text="Imprimir\n Inventario", command=self.imprimir_inventario,
                                        font=custom_font)
        self.inventario_button.place(x=500, y=500)

        self.salir_button = Button(self.master, text="Salir", font=("Arial", 20, "bold"), command=self.salir_aplicacion)
        self.salir_button.place(x=750, y=650)

        self.logo = PhotoImage(file='logo.png')
        self.logo = self.logo.subsample(2)
        self.logoHub = Label(image=self.logo)
        self.logoHub.config(bg="#E3CDCB")
        self.logoHub.place(x=20, y=50)

    def agregar_producto(self):
        ventana_agregar = VentanaSecundaria()
        ventana_agregar.title('Agregar un nuevo producto')
        self.ventana_agregar = ventana_agregar

        titulo = Label(ventana_agregar, text='Ingrese los datos del producto', font=('Arial', 40, "bold"))
        titulo.place(x=200, y=20)

        producto_label = Label(ventana_agregar, text="Nombre del producto:", font=('Arial', 25))
        producto_label.place(x=10, y=100)
        self.producto_entry = TextBox(ventana_agregar)
        self.producto_entry.place(x=10, y=150)

        precio_label = Label(ventana_agregar, text="Precio del producto:", font=('Arial', 25))
        precio_label.place(x=10, y=250)
        self.precio_entry = TextBox(ventana_agregar)
        self.precio_entry.place(x=10, y=300)

        stock_label = Label(ventana_agregar, text="Cantidad en stock:", font=('Arial', 25))
        stock_label.place(x=10, y=400)
        self.stock_entry = TextBox(ventana_agregar)
        self.stock_entry.place(x=10, y=450)

        aceptarBT = Boton(ventana_agregar, text='Siguiente', command=self.agregar_a_tienda)
        aceptarBT.place(x=400, y=500)


    def agregar_a_tienda(self):
        try:
            self.tienda.db.abrir_conexion()

            nombre = self.producto_entry.get()
            precio = float(self.precio_entry.get())
            stock = int(self.stock_entry.get())

            # Obtener el último ID de producto directamente desde el inventario
            ultimo_id_producto = max(self.tienda.inventario.keys(), default=0)
            nuevo_codigo = ultimo_id_producto + 1

            # Agregar el producto a la tienda
            self.tienda.agregar_producto(Producto(nombre, precio, stock))
            #self.tienda.agregar_producto

            # Actualizar el inventario después de agregar un producto
            self.tienda.db.actualizar_inventario()

            transaction.commit()
        except Exception as e:
            print(f"Error al agregar producto a la tienda: {e}")
        finally:
            # Cerrar la conexión
            self.tienda.db.cerrar_conexion()

        # Destruir la ventana actual
        if self.ventana_agregar:
            self.ventana_agregar.destroy()
            self.ventana_agregar = None  # Limpiar la referencia después de destruir la ventana

            # Mostrar la ventana de éxito
            self.mostrar_exito()

    def mostrar_exito(self):
        ventana_exito = Toplevel(self.master)
        ventana_exito.title("Éxito")
        mensaje_exito = Label(ventana_exito, text="Producto agregado correctamente e inventario actualizado.")
        mensaje_exito.pack()

        self.realizar_venta_button = Button(self.master, text="Realizar Venta", command=self.realizar_venta)
        self.realizar_venta_button.pack()

    def realizar_venta(self):
        # Crear una nueva ventana para la venta
        ventana_venta = VentanaSecundaria2()
        ventana_venta.title("Realizar Venta")
        self. ventana_venta=  ventana_venta

        titulo = Label(ventana_venta, text='Elija el tipo de transaccion', font=('Arial', 20, "bold"))
        titulo.place(x=20, y=20)

        # Crear una variable para almacenar la opción seleccionada (factura o ticket)
        self.opcion_factura_ticket = StringVar()

        # Agregar radiobuttons para seleccionar entre factura y ticket
        font_size = 16
        custom_font = font.Font(family="Helvetica", size=font_size)
        factura_radio = Radiobutton(ventana_venta, text="Factura", variable=self.opcion_factura_ticket, value="Factura",font=custom_font)
        factura_radio.pack()
        factura_radio.place(x=175, y=100)

        ticket_radio = Radiobutton(ventana_venta, text="Ticket", variable=self.opcion_factura_ticket, value="Ticket",font=custom_font)
        ticket_radio.pack()
        ticket_radio.place(x=175, y=200)

        # Agregar un botón para abrir la ventana siguiente
        siguiente_button = Button(ventana_venta, text="Siguiente", command=self.abrir_ventana_siguiente)
        siguiente_button.pack()
        siguiente_button.place(x=200, y=300)

    def abrir_ventana_siguiente(self):
        opcion_seleccionada = self.opcion_factura_ticket.get()

        if opcion_seleccionada == "Factura":
            self.abrir_ventana_factura()
        elif opcion_seleccionada == "Ticket":
            self.abrir_ventana_recibo()

    def abrir_ventana_factura(self):
        # Crear una nueva ventana para la factura
        ventana_factura = VentanaSecundaria()
        ventana_factura.title('Factura')
        self.ventana_factura = ventana_factura

        titulo = Label(ventana_factura, text='Ingrese los datos para la factura', font=('Arial', 20, "bold"))
        titulo.place(x=300, y=20)

        # Agregar cuadros de entrada de texto para datos del cliente y productos
        cliente_label = Label(ventana_factura, text="Nombre del Cliente:", font=('Arial', 16))
        cliente_label.place(x=370, y=100)

        self.cliente_entry = Entry(ventana_factura)
        self.cliente_entry.place(x=370, y=140)
        self.cliente_entry.focus_set()

        direccion_label = Label(ventana_factura, text="Direccion del Cliente:", font=('Arial', 16))
        direccion_label.place(x=370, y=180)

        self.direccion_entry = Entry(ventana_factura)
        self.direccion_entry.place(x=370, y=220)
        self.direccion_entry.focus_set()

        telefono_label = Label(ventana_factura, text="Telefono del Cliente:", font=('Arial', 16))
        telefono_label.place(x=370, y=260)

        self.telefono_entry = Entry(ventana_factura)
        self.telefono_entry.place(x=370, y=300)
        self.telefono_entry.focus_set()

        ruc_label = Label(ventana_factura, text="RUC del Cliente:", font=('Arial', 16))
        ruc_label.place(x=370, y=340)

        self.ruc_entry = Entry(ventana_factura)
        self.ruc_entry.place(x=370, y=380)
        self.ruc_entry.focus_set()

        codigo_producto_label = Label(ventana_factura, text="Código del Producto:", font=('Arial', 16))
        codigo_producto_label.place(x=370, y=420)

        self.codigo_producto_entry = Entry(ventana_factura)
        self.codigo_producto_entry.place(x=370, y=460)
        self.codigo_producto_entry.focus_set()

        cantidad_label = Label(ventana_factura, text="Cantidad del Producto:", font=('Arial', 16))
        cantidad_label.place(x=370, y=500)

        self.cantidad_entry = Entry(ventana_factura)
        self.cantidad_entry.place(x=370, y=540)
        self.cantidad_entry.focus_set()

        # Agregar un botón para confirmar la factura
        confirmar_factura_button = Button(ventana_factura, text="Confirmar Factura", command=self.confirmar_factura)
        confirmar_factura_button.place (x=370, y=650)


    def confirmar_factura(self):
        nombre_cliente = self.cliente_entry.get()
        direccion_cliente = self.direccion_entry.get()
        telefono_cliente = self.telefono_entry.get()
        ruc_cliente = self.ruc_entry.get()

        # Obtener el código del producto y la cantidad (deberías obtener esto de tu interfaz gráfica)
        codigo_producto = self.codigo_producto_entry.get()
        cantidad = int(self.cantidad_entry.get())

        # Crear un objeto Cliente
        cliente = Cliente(nombre_cliente, direccion_cliente, telefono_cliente, ruc_cliente)

        # Obtener los productos vendidos
        productos_vendidos = {codigo_producto: cantidad}

        # Crear un objeto Factura
        factura = Factura(cliente, self.tienda, productos_vendidos, cliente.ruc)
        informacion_comprobante = factura.generar_comprobante()

        # Mostrar el comprobante de la transacción
        self.mostrar_comprobante_transaccion(informacion_comprobante)

        # Cerrar la ventana actual
        if self.ventana_factura:
            self.ventana_factura.destroy()
            self.ventana_factura = None

    def abrir_ventana_recibo(self):
        ventana_recibo = VentanaSecundaria()
        ventana_recibo.title('Recibo')
        self.ventana_recibo= ventana_recibo

        titulo = Label(ventana_recibo, text='Ingrese los datos para el recibo', font=('Arial', 20, "bold"))
        titulo.place(x=300, y=10)

        # Agregar cuadros de entrada de texto para datos del cliente y productos
        cliente_label_recibo = Label(ventana_recibo, text="Nombre del Cliente:", font=('Arial', 20))
        cliente_label_recibo.place(x=370, y=100)

        self.cliente_entry_recibo= Entry(ventana_recibo)
        self.cliente_entry_recibo.place(x=370, y=150)
        self.cliente_entry_recibo.focus_set()

        direccion_label = Label(ventana_recibo, text="Direccion del Cliente:", font=('Arial', 20))
        direccion_label.place(x=370, y=200)

        self.direccion_entry_recibo= Entry(ventana_recibo)
        self.direccion_entry_recibo.place(x=370, y=250)
        self.direccion_entry_recibo.focus_set()

        telefono_label = Label(ventana_recibo, text="Telefono del Cliente:", font=('Arial', 20))
        telefono_label.place(x=370, y=300)

        self.telefono_entry_recibo= Entry(ventana_recibo)
        self.telefono_entry_recibo.place(x=370, y=350)
        self.telefono_entry_recibo.focus_set()

        codigo_producto_label = Label(ventana_recibo, text="Código del Producto:", font=('Arial', 20))
        codigo_producto_label.place(x=370, y=400)

        self.codigo_producto_entry = Entry(ventana_recibo)
        self.codigo_producto_entry.place(x=370, y=450)
        self.codigo_producto_entry.focus_set()

        cantidad_label = Label(ventana_recibo, text="Cantidad del Producto:", font=('Arial', 20))
        cantidad_label.place(x=370, y=500)

        self.cantidad_entry = Entry(ventana_recibo)
        self.cantidad_entry.place(x=370, y=550)
        self.cantidad_entry.focus_set()

        # Agregar un botón para confirmar el recibo
        confirmar_recibo_button = Button(ventana_recibo, text="Confirmar Recibo", command=self.confirmar_recibo)
        confirmar_recibo_button.place(x=370, y=650)

    def confirmar_recibo(self):
        nombre_cliente = self.cliente_entry_recibo.get()
        direccion_cliente = self.direccion_entry_recibo.get()
        telefono_cliente = self.telefono_entry_recibo.get()

        codigo_producto = self.codigo_producto_entry.get()
        cantidad = int(self.cantidad_entry.get())

        # Crear un objeto Cliente
        cliente = Cliente(nombre_cliente, direccion_cliente, telefono_cliente)

        # Obtener los productos vendidos
        productos_vendidos = {codigo_producto: cantidad}

        # Crear un objeto Recibo
        recibo = Recibo(cliente, self.tienda, productos_vendidos)
        informacion_comprobante = recibo.generar_comprobante()

        # Agrega un mensaje de depuración
        print("Información del comprobante:", informacion_comprobante)

        # Mostrar el comprobante en la ventana
        self.mostrar_comprobante_transaccion(informacion_comprobante)

        # Cerrar la ventana actual
        if self.ventana_recibo:
            self.ventana_recibo.destroy()
            self.ventana_recibo = None

    def mostrar_comprobante_transaccion(self, informacion_comprobante):
        ventana_comprobante = Toplevel()
        ventana_comprobante.title('Comprobante de Transacción')

        texto_comprobante = Text(ventana_comprobante, wrap=WORD, height=20, width=50)
        texto_comprobante.insert("1.0", informacion_comprobante)
        texto_comprobante.pack()

        # Agregar un botón para cerrar la ventana del comprobante
        cerrar_button = Button(ventana_comprobante, text="Cerrar", command=ventana_comprobante.destroy)
        cerrar_button.pack()

        # Puedes también descomentar la siguiente línea si quieres que la ventana sea modal
        # ventana_comprobante.grab_set()
        ventana_comprobante.focus_set()
        ventana_comprobante.wait_window()

    def realizar_devolucion(self):
        ventana_devolucion = VentanaSecundaria2()
        ventana_devolucion.title("Realizar Devolución")
        self.ventana_devolucion = ventana_devolucion

        titulo = Label(ventana_devolucion, text='Ingrese los datos del producto', font=('Arial', 20, "bold"))
        titulo.place(x=20, y=20)

        codigo_label = Label(ventana_devolucion, text="Código del Producto:")
        codigo_label.place(x=175, y=100)
        self.codigo_devolucion_entry = Entry(ventana_devolucion)
        self.codigo_devolucion_entry.place(x=175, y=130)

        cantidad_label = Label(ventana_devolucion, text="Cantidad a Devolver:")
        cantidad_label.place(x=175, y=200)
        self.cantidad_devolucion_entry = Entry(ventana_devolucion)
        self.cantidad_devolucion_entry.place(x=175, y=230)

        confirmar_devolucion_bt = Button(ventana_devolucion, text="Confirmar Devolución",
                                        command=self.confirmar_devolucion)
        confirmar_devolucion_bt.pack()
        confirmar_devolucion_bt.place(x=175, y=300)


    def confirmar_devolucion(self):
        # Obtener el código del producto y la cantidad desde la interfaz
        codigo_producto = self.codigo_devolucion_entry.get()
        cantidad = int(self.cantidad_devolucion_entry.get())

        self.devolver_producto_interfaz(codigo_producto, cantidad)

        # Cerrar la ventana de devolución después de confirmar
        if self.ventana_devolucion:
            self.ventana_devolucion.destroy()
            self.ventana_devolucion = None

    def devolver_producto_interfaz(self, producto_codigo, cantidad):
        # Convertir el código del producto a cadena
        producto_codigo_str = str(producto_codigo)

        # Llama a la función de la tienda para devolver el producto
        exito = self.tienda.devolver_producto(producto_codigo_str, cantidad)

        if exito:
            # Actualiza la interfaz con el mensaje de éxito
            mensaje = f"Se han devuelto {cantidad} unidades del producto con código {producto_codigo_str}."
            self.mostrar_mensaje_exitoso(mensaje)
        else:
            # Actualiza la interfaz con el mensaje de error
            mensaje = f"No se pudo realizar la devolución del producto con código {producto_codigo_str}."
            self.mostrar_mensaje_error(mensaje)

    def mostrar_mensaje_exitoso(self, mensaje):
        ventana_exito = Toplevel(self.master)
        ventana_exito.title("Éxito")
        mensaje_exito = Label(ventana_exito, text=mensaje)
        mensaje_exito.pack()

    def imprimir_inventario(self):
        inventario = self.tienda.obtener_inventario()

        ventana_inventario = Toplevel(self.master)
        ventana_inventario.title("Inventario")

        text_inventario = Text(ventana_inventario)
        text_inventario.pack()

        for codigo, producto in inventario.items():
            nombre = producto.nombre
            precio = producto.precio
            stock = producto.stock
            info_producto = f"Código: {codigo}, Nombre: {nombre}, Precio: {precio}, Stock: {stock}\n"
            text_inventario.insert(INSERT, info_producto)

    def salir_aplicacion(self):
        # Mostrar un mensaje de confirmación antes de salir
        resultado = messagebox.askquestion("Salir", "¿Está seguro que desea salir?", icon='warning')

        if resultado == 'yes':
            # Cerrar la conexión de la base de datos
            self.tienda.db.cerrar_conexion()

            # Destruir la ventana principal
            self.master.destroy()


class VentanaSecundaria(Toplevel):
    def __init__(self):
        super().__init__()
        super().geometry('985x770')
        super().config(bg='#ECE9D2')
        super().grab_set()

class VentanaSecundaria2(Toplevel):
    def __init__(self):
        super().__init__()
        super().geometry('500x400')
        super().config(bg='#ECE9D2')
        super().grab_set()

class TextBox(Entry):
    # Clase para abstraer las cajas de texto
    def __init__(self, parent=None, **config):
        Entry.__init__(self, parent, **config)

class Boton(Button):
    # Clase para abstraer botones, heredando de Button pero estos botones son utilizados para selecciones
    def __init__(self, parent=None, **config):
        Button.__init__(self, parent, **config)
        self.config(
            fg='black',
            bg='#D9D9D9',
            relief='raised',
            font=("Verdana", 20, "bold"),
            activeforeground="#F1F1F1",
            activebackground="#D5A3C0",
            height=2,
            width=12
                )


class BaseDeDatosZODB:
    def __init__(self, archivo_bd):
        self.archivo_bd = archivo_bd
        self.connection = None
        self.root = None
        self.tienda= None

    def abrir_conexion(self):
        storage = FileStorage.FileStorage(self.archivo_bd)
        db = DB(storage)
        self.connection = db.open()
        self.root = self.connection.root

        # Crear una instancia de la Tienda si no existe en la base de datos
        if not hasattr(self.root, 'tienda'):
            self.root.tienda = Tienda()

    def cerrar_conexion(self):
        try:
            if self.connection:
                transaction.commit()
        except Exception as e:
            print(f"Error al realizar commit antes de cerrar la conexión: {e}")
        finally:
            try:
                if self.connection:
                    self.connection.close()
            except Exception as e:
                print(f"Error al cerrar la conexión: {e}")


