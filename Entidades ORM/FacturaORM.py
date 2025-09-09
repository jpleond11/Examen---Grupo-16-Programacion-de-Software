from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class FacturaORM(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, index=True)
    monto = Column(Float, nullable=False)
    fecha_emision = Column(DateTime, default=datetime.utcnow)

    # Relación con Cita
    cita_id = Column(Integer, ForeignKey("citas.id"), unique=True, nullable=False)
    cita = relationship("CitaORM", back_populates="factura")

    def __str__(self):
        return (
            f"Factura - Fecha: {self.fecha_emision.strftime('%d/%m/%Y')}\n"
            f"Mascota: {self.cita.animal.nombre}\n"
            f"Dueño: {self.cita.animal.propietario.nombre}\n"
            f"Motivo: {self.cita.motivo}\n"
            f"Monto: ${self.monto:.2f}"
        )

from pydantic import BaseModel, condecimal
from datetime import datetime

class FacturaBase(BaseModel):
    monto: condecimal(gt=0, decimal_places=2)
    fecha_emision: datetime

class FacturaCreate(FacturaBase):
    cita_id: int  # El cliente debe indicar a qué cita pertenece

class FacturaRead(FacturaBase):
    id: int

    class Config:
        orm_mode = True
