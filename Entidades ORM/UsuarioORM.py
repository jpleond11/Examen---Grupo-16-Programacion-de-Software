from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import date
from uuid import UUID

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(UUID(as_uuid=True), primary_key=True, default=UUID.uuid4, unique=True, nullable=False)
    primer_nombre_usuario = Column(String(50), nullable=False, index=True)
    segundo_nombre_usuario = Column(String(50), nullable=True, index=True)
    primer_apellido_usuario = Column(String(50), nullable=False, index=True)
    segundo_apellido_usuario = Column(String(50), nullable=True, index=True)
    rol_usuario = Column(Text, nullable=False)
    fecha_nacimiento_usuario = Column(date, nullable=False)

    """ Relaciones """
    propietarios = relationship("Propietario", back_populates="usuario", cascade="all, delete-orphan")

""" Esquemas de Pydantic para validación y serialización """
from pydantic import BaseModel, constr, Field
from datetime import date
from uuid import UUID

class UsuarioSchema(BaseModel):
    id_usuario: UUID | None = Field(default=None)

    primer_nombre_usuario: constr(strip_whitespace=True, min_length=1, max_length=50) #type: ignore
    segundo_nombre_usuario: constr(strip_whitespace=True, min_length=1, max_length=50) | None = None #type: ignore

    primer_apellido_usuario: constr(strip_whitespace=True, min_length=1, max_length=50) #type: ignore
    segundo_apellido_usuario: constr(strip_whitespace=True, min_length=1, max_length=50) | None = None #type: ignore

    rol_usuario: constr(strip_whitespace=True, min_length=1) #type: ignore

    fecha_nacimiento_usuario: date 

    class Config:
        from_attributes = True 

