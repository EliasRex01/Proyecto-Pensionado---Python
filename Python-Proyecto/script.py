class Cliente:
  def __init__(self, nombre):
      self.nombre = nombre
      self.compras = 0

  def calcular_descuento(self):
      descuento = 0
      if self.compras > 5:
          descuento += 0.05
      return descuento

  def incrementar_compras(self):
      self.compras += 1


class ClienteRegular(Cliente):
  def __init__(self, nombre):
      super().__init__(nombre)
      self.tipo = "Regular"

  def calcular_descuento(self):
      return super().calcular_descuento() + 0.05


class ClienteVIP(Cliente):
  def __init__(self, nombre):
      super().__init__(nombre)
      self.tipo = "VIP"

  def calcular_descuento(self):
      return super().calcular_descuento() + 0.1


class Libro:
  def __init__(self, titulo, precio):
      self.titulo = titulo
      self.precio = precio

  def __str__(self):
      return f"Libro: {self.titulo} - Precio: {self.precio}"


class Libreria:
  def __init__(self):
      self.libros = []

  def agregar_libro(self, libro):
      self.libros.append(libro)

  def calcular_precio_total(self, cliente):
      subtotal = sum(libro.precio for libro in self.libros)
      descuento = cliente.calcular_descuento()
      total = subtotal * (1 - descuento)
      return total

  def registrar_venta(self, cliente):
      cliente.incrementar_compras()



# Ejemplo de uso:
if __name__ == "__main__":
    # Crear algunos libros
    libro1 = Libro("El principito", 10)
    libro2 = Libro("Cien años de soledad", 15)
    libro3 = Libro("Python for Dummies", 20)

    # Crear una librería
    libreria = Libreria()

    # Agregar libros a la librería
    libreria.agregar_libro(libro1)
    libreria.agregar_libro(libro2)
    libreria.agregar_libro(libro3)

    # Crear clientes
    cliente_regular = ClienteRegular("Elias Soto")
    cliente_vip = ClienteVIP("Juan Pérez")

    # Imprimir información de los clientes
    print(f"01 {cliente_regular} Cliente: {cliente_regular.tipo} Libros: {len(libreria.libros)} Precio: {sum(libro.precio for libro in libreria.libros)} Total: ${libreria.calcular_precio_total(cliente_regular)}")
    print(f"02 {cliente_vip} Cliente: {cliente_vip.tipo} Libros: {len(libreria.libros)} Precio: {sum(libro.precio for libro in libreria.libros)} Total: ${libreria.calcular_precio_total(cliente_vip)}")
