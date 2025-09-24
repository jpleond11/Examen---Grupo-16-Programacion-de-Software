from database.config import Base
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime


class Propietario(Base):
    __tablename__ = "propietarios"

    """
    Atributos:
        id_propietario (UUID): Identificador único.
        primer_nombre_propietario (str): Primer nombre.
        segundo_nombre_propietario (str): Segundo nombre (opcional).
        primer_apellido_propietario (str): Primer apellido.
        segundo_apellido_propietario (str): Segundo apellido.
        telefono (str): Número de contacto.
        direccion (str): Dirección de residencia.
        usuario_id_creacion (UUID): Usuario que creó el registro.
        usuario_id_edicion (UUID): Usuario que editó el registro.
        fecha_creacion (datetime): Fecha de creación.
        fecha_actualizacion (datetime): Última actualización.

    Relaciones:
        usuario: Usuario asociado.
        animales: Lista de animales del propietario.

    Métodos:
        mostrar_info(): Retorna información básica del propietario.
    """

    id_propietario = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False
    )
    primer_nombre_propietario = Column(String(50), nullable=False)
    segundo_nombre_propietario = Column(String(50), nullable=True)
    primer_apellido_propietario = Column(String(50), nullable=False)
    segundo_apellido_propietario = Column(String(50), nullable=False)
    telefono = Column(String(20), nullable=False)
    direccion = Column(String(200), nullable=False)

    usuario_id_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )
    usuario_id_edicion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True
    )
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    """ Relaciones """
    usuario_creador = relationship("Usuario", foreign_keys=[usuario_id_creacion], back_populates="propietarios_creados")
    usuario_editor = relationship("Usuario", foreign_keys=[usuario_id_edicion], back_populates="propietarios_editados")

    animales = relationship(
        "Animal", back_populates="propietario", cascade="all, delete-orphan"
    )

    def mostrar_info(self) -> str:
        return (
            f"Nombre: {self.primer_nombre_propietario} {self.segundo_nombre_propietario or ''}"
            f"{self.primer_apellido_propietario} {self.segundo_apellido_propietario},"
            f"Telefono: {self.telefono}, Dirección: {self.direccion}"
        )
