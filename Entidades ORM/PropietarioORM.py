from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

class Propietario(Base):
    __tablename__ = "propietarios"

    id_propietario = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False, unique=True)
    primer_nombre_propietario = Column(String(50), nullable=False)
    segundo_nombre_propietario = Column(String(50), nullable=True)
    primer_apellido_propietario = Column(String(50), nullable=False)
    segundo_apellido_propietario = Column(String(50), nullable=False)
    telefono = Column(String(20), nullable=False)
    direccion = Column(String(200), nullable=False)

    usuario_id_creacion = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    usuario_id_edicion = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    fecha_creacion = Column(datetime, default=datetime.now, nullable=False)
    fecha_actualizacion = Column(datetime, default=datetime.now, onupdate=datetime.now)

    """ Relaciones """
    usuario = relationship("Usuario", back_populates="propietarios")

    def mostrar_info(self) -> str:
        return f"Nombre: {self.nombre}, Telefono: {self.telefono}, Dirección: {self.direccion}"
    
""" Se procede a realizar las validaciones por Pydantic """
    
from pydantic import BaseModel, constr, Field
from typing import Optional
from datetime import datetime

class PropietarioBase(BaseModel):
    primer_nombre_propietario: constr(strip_whitespace=True, min_length=2, max_length=50) #type: ignore
    segundo_nombre_propietario: Optional[constr(strip_whitespace=True, max_length=50)] = None #type:ignore
    primer_apellido_propietario: constr(strip_whitespace=True, min_length=2, max_length=50) #type:ignore
    segundo_apellido_propietario: constr(strip_whitespace=True, min_length=2, max_length=50) #type:ignore
    telefono: constr(strip_whitespace=True, min_length=7, max_length=20) #type:ignore
    direccion: constr(strip_whitespace=True, min_length=5, max_length=200) #type:ignore

    usuario_id_creacion: int = Field(..., gt=0)
    """ obligatorio, debe ser > 0 """
    usuario_id_edicion: int = Field(..., gt=0)
    """ # obligatorio, debe ser > 0 """

class PropietarioCreate(PropietarioBase):
    """ Esquema para crear un propietario (el ID lo genera la BD)."""
    pass

class PropietarioUpdate(BaseModel):
    """ Esquema para actualizar un propietario (campos opcionales)."""
    primer_nombre_propietario: Optional[constr(strip_whitespace=True, min_length=2, max_length=50)] #type:ignore
    segundo_nombre_propietario: Optional[constr(strip_whitespace=True, max_length=50)] #type:ignore
    primer_apellido_propietario: Optional[constr(strip_whitespace=True, min_length=2, max_length=50)] #type:ignore
    segundo_apellido_propietario: Optional[constr(strip_whitespace=True, min_length=2, max_length=50)] #type:ignore
    telefono: Optional[constr(strip_whitespace=True, min_length=7, max_length=20)] #type:ignore
    direccion: Optional[constr(strip_whitespace=True, min_length=5, max_length=200)] #type:ignore
    usuario_id_edicion: Optional[int] = Field(None, gt=0)

class PropietarioResponse(PropietarioBase):
    """ Respuesta que incluye metadata como IDs y fechas."""
    id_propietario: str
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]

    class Config:
        orm_mode = True 
