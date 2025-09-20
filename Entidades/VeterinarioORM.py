from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.config import Base


class Veterinario(Base):
    __tablename__ = "veterinarios"

    id_veterinario = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False
    )
    primer_nombre_veterinario = Column(String(50), nullable=False)
    segundo_nombre_veterinario = Column(String(50), nullable=True)
    primer_apellido_veterinario = Column(String(50), nullable=False)
    segundo_apellido_veterinario = Column(String(50), nullable=True)
    telefono = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    especialidad = Column(String(100), nullable=False)

    usuario_id_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )
    usuario_id_edicion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True
    )
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    """ Relaciones """
    citas = relationship(
        "Cita", back_populates="veterinario", cascade="all, delete-orphan"
    )

    def __str__(self):
        return (
            f"Veterinario: {self.primer_nombre_veterinario} {self.primer_apellido_veterinario} "
            f"- Especialidad: {self.especialidad} - Tel: {self.telefono}"
        )
