from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class CitaORM(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, nullable=False, default=datetime.utcnow)
    motivo = Column(String(200), nullable=False)

    # Relación con Animal
    animal_id = Column(Integer, ForeignKey("animales.id"), nullable=False)
    animal = relationship("AnimalORM", back_populates="citas")

    factura = relationship("FacturaORM", back_populates="cita", uselist=False)

    def agendar_cita(self) -> str:
        return f"Cita para {self.animal.nombre} el {self.fecha.strftime('%d/%m/%Y %H:%M')} - Motivo: {self.motivo}"

from pydantic import BaseModel, constr
from datetime import datetime

class CitaBase(BaseModel):
    fecha: datetime
    motivo: constr(min_length=3, max_length=200)

class CitaCreate(CitaBase):
    animal_id: int  # El cliente debe indicar a qué animal pertenece

class CitaRead(CitaBase):
    id: int

    class Config:
        orm_mode = True
