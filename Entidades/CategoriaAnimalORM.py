from database.config import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from uuid import UUID, uuid4


class CategoriaAnimal(Base):
    __tablename__ = "categoria_animal"

    id_categoria_animal = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False
    )
    nombre_categoria = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(255), nullable=True)

    """ Relaciones """
    animales = relationship(
        "Animal", back_populates="categoria_animal", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<CategoriaAnimal(id={self.id_categoria_animal}, nombre='{self.nombre_categoria}', descripcion='{self.descripcion}')>"
