from database.config import Base
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from uuid import UUID, uuid4
from datetime import datetime


class Factura(Base):
    __tablename__ = "facturas"

    id_factura = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False
    )
    monto_factura = Column(Float, nullable=False)
    fecha_emision = Column(DateTime, default=datetime.now, nullable=False)
    descripcion_factura = Column(String(200), nullable=False)

    cita_id = Column(UUID(as_uuid=True), ForeignKey("citas.id_cita"), nullable=False)

    usuario_id_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )
    usuario_id_edicion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True
    )
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    """ Relaciones """
    cita = relationship("Cita", back_populates="facturas")

    def __str__(self):
        return (
            f"Factura - Fecha: {self.fecha_emision.strftime('%d/%m/%Y')}\n"
            f"Mascota: {self.cita.animal.nombre_animal}\n"
            f"Dueño: {self.cita.animal.propietario.primer_nombre_propietario} {self.cita.animal.propietario.segundo_nombre_propietario}\n"
            f"Motivo: {self.cita.motivo_cita}\n"
            f"Monto: ${self.monto_factura:.2f}"
        )
