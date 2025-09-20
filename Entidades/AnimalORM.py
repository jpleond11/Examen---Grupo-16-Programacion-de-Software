from database.config import Base
from sqlalchemy import Column, String, ForeignKey, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime


class Animal(Base):
    __tablename__ = "animales"

    """
    Atributos:
        id_animal (UUID): Identificador único.
        nombre_animal (str): Nombre del animal.
        especie_animal (str): Especie del animal.
        fecha_nacimiento_animal (date): Fecha de nacimiento.
        propietario_id (UUID): Referencia al propietario.
        categoria_id (UUID): Referencia a la categoría.
        usuario_id_creacion (UUID): Usuario que creó el registro.
        usuario_id_edicion (UUID): Usuario que editó el registro.
        fecha_creacion (datetime): Fecha de creación.
        fecha_actualizacion (datetime): Última actualización.

    Relaciones:
        propietario, categoria_animal, citas.

    Métodos:
        mostrar_info(): Devuelve una cadena con información básica del animal.
    """

    id_animal = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False
    )
    nombre_animal = Column(String(50), nullable=False)
    especie_animal = Column(String(20), nullable=False)
    fecha_nacimiento_animal = Column(Date, nullable=False)

    propietario_id = Column(
        UUID(as_uuid=True), ForeignKey("propietarios.id_propietario"), nullable=False
    )
    categoria_id = Column(
        UUID(as_uuid=True),
        ForeignKey("categoria_animal.id_categoria_animal"),
        nullable=False,
    )

    usuario_id_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )
    usuario_id_edicion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True
    )
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    """ Relaciones """
    propietario = relationship("Propietario", back_populates="animales")
    categoria_animal = relationship("CategoriaAnimal", back_populates="animales")
    citas = relationship("Cita", back_populates="animal", cascade="all, delete-orphan")

    def mostrar_info(self) -> str:
        return (
            f"Nombre: {self.nombre_animal}, "
            f"Especie: {self.especie_animal}, "
            f"Fecha de Nacimiento: {self.fecha_nacimiento_animal}"
        )
