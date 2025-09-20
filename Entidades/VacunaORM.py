from database.config import Base
from sqlalchemy import Column, String, Date, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime


class Vacuna(Base):
    __tablename__ = "vacunas"

    id_vacuna = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False
    )
    nombre_vacuna = Column(String(100), nullable=False)
    fecha_aplicacion_vacuna = Column(Date, nullable=False)
    proxima_dosis_vacuna = Column(Date, nullable=True)

    usuario_id_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )
    usuario_id_edicion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True
    )
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    """ Relaciones """
    citas = relationship("Cita", back_populates="vacuna", cascade="all, delete-orphan")

    def mostrar_info(self):
        return (
            f"Vacuna: {self.nombre_vacuna}, "
            f"Fecha de aplicación: {self.fecha_aplicacion_vacuna}, "
            f"Próxima dosis: {self.proxima_dosis_vacuna}"
        )
