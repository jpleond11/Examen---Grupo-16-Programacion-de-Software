from database.config import Base
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime


class Factura(Base):
    __tablename__ = "facturas"

    """
    Atributos:
        id_factura (UUID): Identificador único.
        monto_factura (float): Valor total de la factura.
        fecha_emision (datetime): Fecha de emisión.
        descripcion_factura (str): Descripción de la factura.
        cita_id (UUID): Referencia a la cita asociada.
        usuario_id_creacion (UUID): Usuario que creó el registro.
        usuario_id_edicion (UUID): Usuario que editó el registro.
        fecha_creacion (datetime): Fecha de creación.
        fecha_actualizacion (datetime): Última actualización.

    Relaciones:
        cita: Relación con la cita correspondiente.

    Métodos:
        __str__(): Devuelve una representación en texto con la información de la factura.
    """

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
