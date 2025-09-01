#Se crea la clase factura
from datetime import datetime
from .cita import Cita

class Factura:
    def __init__(self, cita: Cita, monto: float, fecha_emision: datetime) -> None:
        self.cita = cita
        self.monto = monto
        self.fecha_emision = fecha_emision

    def __str__(self):
        return (f"Factura - Fecha: {self.fecha_emision.strftime('%d/%m/%Y')}\n"
                f"Mascota: {self.cita.animal.nombre}\n"
                f"Dueño: {self.cita.animal.propietario.nombre}\n"
                f"Motivo: {self.cita.motivo}\n"
                f"Monto: ${self.monto:.2f}"
        )