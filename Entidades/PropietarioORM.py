from database.config import Base
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from uuid import UUID, uuid4
from datetime import datetime


class Propietario(Base):
    __tablename__ = "propietarios"

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
    usuario = relationship("Usuario", back_populates="propietarios")
    animales = relationship(
        "Animal", back_populates="propietario", cascade="all, delete-orphan"
    )

    def mostrar_info(self) -> str:
        return (
            f"Nombre: {self.primer_nombre_propietario} {self.segundo_nombre_propietario or ''}"
            f"{self.primer_apellido_propietario} {self.segundo_apellido_propietario},"
            f"Telefono: {self.telefono}, Dirección: {self.direccion}"
        )
