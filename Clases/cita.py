#Se crea la clase de citas
from datetime import datetime
from .animal import Animal

class Cita:
    def __init__(self, animal:Animal, fecha:datetime, motivo: str) -> None:
        self._animal = animal
        self._fecha = fecha
        self._motivo = motivo
        
    @property
    def animal(self):
        return self._animal
    @property
    def fecha(self):
        return self._fecha
    @property
    def motivo (self):
        return self._motivo        

    def agendar_cita(self) -> str:
        return f"Cita para {self.animal.nombre} el {self.fecha.strftime('%d/%m/%Y %H:%M')} - Motivo: {self.motivo}"