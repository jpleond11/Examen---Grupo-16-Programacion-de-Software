from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from uuid import UUID
from datetime import date, datetime

class Animal(Base):
    __tablename__ = "animales"

    id_animal = Column(UUID(as_uuid=True), primary_key=True, default=UUID.uuid4, unique=True, nullable=False)
    nombre_animal = Column(String(50), nullable=False)
    especie_animal = Column(String(20), nullable=False)
    fecha_nacimiento_animal = Column(date, nullable=False)

    usuario_id_creacion = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    usuario_id_edicion = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    fecha_creacion = Column(datetime, default=datetime.now, nullable=False)
    fecha_actualizacion = Column(datetime, default=datetime.now, onupdate=datetime.now)

    """ Relaciones """
    propietario = relationship("Propietario", back_populates="animales")
    categoria_animal = relationship("Propietario", back_populates="categorias_animales")

    def mostrar_info(self) -> str:
        return f"Nombre: {self.nombre_animal}, Fecha de Nacimiento: {self.fecha_nacimiento_animal}, Especie: {self.especie_animal}"

""" Se procede a realizar las validaciones por Pydantic """
from pydantic import BaseModel, constr, Field
from datetime import date, datetime

class AnimalSchema(BaseModel):
    id_animal: UUID | None = Field(default=None)

    nombre_animal: constr(strip_whitespace=True, min_length=1, max_length=50) #type: ignore
    especie_animal: constr(strip_whitespace=True, min_length=1, max_length=20) #type: ignore
    fecha_nacimiento_animal: date

    usuario_id_creacion: UUID  
    usuario_id_edicion: UUID  

    fecha_creacion: datetime | None = None
    fecha_actualizacion: datetime | None = None

    class Config:
        from_attributes = True 

