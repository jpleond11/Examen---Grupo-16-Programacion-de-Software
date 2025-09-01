#Se crea la clase de citas
from datetime import datetime
from animal import Animal

class Cita(Animal):
    def __init__(self, nombre, edad, propietario, fecha:datetime, motivo) -> None:
        super().__init__(nombre, edad, propietario)
        self._fecha = fecha
        self._motivo = motivo

    def agendar_cita(self) -> None:
        return f"Cita para {self.animal.nombre} el {self.fecha} - Motivo: {self.motivo}"