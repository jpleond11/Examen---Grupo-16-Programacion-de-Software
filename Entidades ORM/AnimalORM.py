# animal.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from .categoria_animal import CategoriaAnimal

Base = declarative_base()

class Animal(Base):
    __tablename__ = "animal"

    id_animal = Column(Integer, primary_key=True, autoincrement=True)

    id_propietario = Column(Integer, ForeignKey("propietario.id_propietario"), nullable=False)
    id_categoria_animal = Column(Integer, ForeignKey("categoria_animal.id_categoria_animal"), nullable=False)

    nombre_animal = Column(String(100), nullable=False)
    especie_animal = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=True)
    
    categoria_animal = Column(String(100), nullable=True)

    usuario_id_creacion = Column(Integer, nullable=False)
    usuario_id_edicion = Column(Integer, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    categoria = relationship("CategoriaAnimal", back_populates="animales")

    def __repr__(self):
        return f"<Animal(id={self.id_animal}, nombre='{self.nombre_animal}', especie='{self.especie_animal}')>"

CategoriaAnimal.animales = relationship("Animal", back_populates="categoria", cascade="all, delete-orphan")


""" Se procede a realizar las validaciones por Pydantic """
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional

class AnimalBase(BaseModel):
    nombre_animal: str = Field(..., min_length=2, max_length=100, description="Nombre del animal")
    especie_animal: str = Field(..., min_length=2, max_length=100, description="Especie del animal")
    fecha_nacimiento: Optional[date] = Field(None, description="Fecha de nacimiento del animal")
    id_categoria_animal: int = Field(..., gt=0, description="ID de la categoría del animal")
    id_propietario: int = Field(..., gt=0, description="ID del propietario")

    usuario_id_creacion: int = Field(..., gt=0, description="Usuario que crea el registro")
    usuario_id_edicion: Optional[int] = Field(None, gt=0, description="Usuario que edita el registro")


"""Para crear un nuevo animal"""
class AnimalCreate(AnimalBase):
    pass


"""Para actualizar un animal (se permite opcionalidad en campos)"""
class AnimalUpdate(BaseModel):
    nombre_animal: Optional[str] = Field(None, min_length=2, max_length=100)
    especie_animal: Optional[str] = Field(None, min_length=2, max_length=100)
    fecha_nacimiento: Optional[date] = None
    id_categoria_animal: Optional[int] = Field(None, gt=0)
    id_propietario: Optional[int] = Field(None, gt=0)
    usuario_id_edicion: Optional[int] = Field(None, gt=0)


"""Esquema de respuesta"""
class AnimalResponse(AnimalBase):
    id_animal: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        orm_mode = True
