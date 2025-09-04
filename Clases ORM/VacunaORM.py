from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class VacunaORM(Base):
    __tablename__ = "vacunas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    fecha_aplicacion = Column(Date, nullable=False)
    proxima_dosis = Column(Date, nullable=True)

    # Relación con Animal
    animal_id = Column(Integer, ForeignKey("animales.id"), nullable=False)
    animal = relationship("AnimalORM", back_populates="vacunas")

    def mostrar_info(self):
        return (
            f"Vacuna: {self.nombre}, "
            f"Fecha de aplicación: {self.fecha_aplicacion}, "
            f"Próxima dosis: {self.proxima_dosis}"
        )

from pydantic import BaseModel, constr
from datetime import date

class VacunaBase(BaseModel):
    nombre: constr(min_length=1, max_length=100)
    fecha_aplicacion: date
    proxima_dosis: date | None = None

class VacunaCreate(VacunaBase):
    animal_id: int  # el cliente debe indicar a qué animal pertenece

class VacunaRead(VacunaBase):
    id: int

    class Config:
        orm_mode = True
