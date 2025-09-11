from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class CategoriaAnimal(Base):
    __tablename__ = "categoria_animal"

    id_categoria_animal = Column(Integer, primary_key=True, autoincrement=True)
    nombre_categoria = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<CategoriaAnimal(id={self.id_categoria_animal}, nombre='{self.nombre_categoria}')>"

""" Se procede a realizar las validaciones por Pydantic """
from pydantic import BaseModel, Field
from typing import Optional

class CategoriaAnimalBase(BaseModel):
    nombre_categoria: str = Field(..., min_length=2, max_length=100, description="Nombre de la categoría, ejemplo: Perro, Gato, Ave")
    descripcion: Optional[str] = Field(None, max_length=255, description="Descripción opcional de la categoría")


""" Para crear una categoría"""
class CategoriaAnimalCreate(CategoriaAnimalBase):
    pass


""" Para actualizar una categoría (todo opcional)"""
class CategoriaAnimalUpdate(BaseModel):
    nombre_categoria: Optional[str] = Field(None, min_length=2, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=255)


"""Esquema de respuesta"""
class CategoriaAnimalResponse(CategoriaAnimalBase):
    id_categoria_animal: int

    class Config:
        orm_mode = True
