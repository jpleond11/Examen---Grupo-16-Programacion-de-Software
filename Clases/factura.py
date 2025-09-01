#Se crea la clase factura
from .cita import Cita

class Factura(Cita):
    def __init__(self, monto: float, fecha_emision, nombre, propietario, motivo) -> None:
        super().__init__(nombre, propietario, motivo)
        self._monto = monto
        self.fecha_emision = fecha_emision

    def __str__(self):
        return super().__str__(f"Factura - Fecha: {self.fecha_emision}\n"
                               f"Mascota: {self.cita.animal.nombre}\n"
                               f"Dueño: {self.cita.animal.propietario}\n"
                               f"Motivo: {self.cita.motivo}\n"
                               f"Monto: ${self._monto}")    