from pydantic import BaseModel, constr
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class PropietarioORM(Base):
    __tablename__ = "propietarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=False)
    direccion = Column(String(200), nullable=False)

    def mostrar_info(self) -> str:
        return f"Nombre: {self.nombre}, Telefono: {self.telefono}, Dirección: {self.direccion}"
    
    from pydantic import BaseModel, constr

class PropietarioBase(BaseModel):
    nombre: constr(min_length=1, max_length=100)
    telefono: constr(min_length=7, max_length=20)
    direccion: constr(min_length=5, max_length=200)

class PropietarioCreate(PropietarioBase):
    """Datos necesarios para crear un propietario"""
    pass

class PropietarioRead(PropietarioBase):
    """Datos que se devuelven al cliente (incluye ID)"""
    id: int

    class Config:
        orm_mode = True