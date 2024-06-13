from abc import ABCMeta, abstractmethod

class Persona(metaclass=ABCMeta):
    """
    Clase abstracta que abstrae a una persona
    """
    def __init__(self, ci):
        self.ci = ci

class Pensionado(Persona):
    """
    Clase que abstrae a un pensionado
    """
    def __init__(self, ci, categoria):
        super().__init__(ci)
        self.categoria = categoria

    def buscar_categoria(self):
        return self.categoria.buscar(self.ci)

class Categoria(metaclass=ABCMeta):
    """
    Clase abstracta que abstrae una categoría de pensionado
    """
    @abstractmethod
    def buscar(self, ci):
        raise NotImplementedError("La operación debe ser implementada")

class HonorificoData:
    """
    Clase auxiliar para los datos de los pensionados honoríficos
    """
    def __init__(self, ci, nombre_apellido, departamento, distrito, concepto_pension, fecha_ingreso, monto_pension):
        self.ci = ci
        self.nombre_apellido = nombre_apellido
        self.departamento = departamento
        self.distrito = distrito
        self.concepto_pension = concepto_pension
        self.fecha_ingreso = fecha_ingreso
        self.monto_pension = monto_pension