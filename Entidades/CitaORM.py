from database.config import Base
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime


class Cita(Base):
    __tablename__ = "citas"

    """
    Atributos:
        id_cita (UUID): Identificador único.
        fecha_inicio_cita (datetime): Fecha y hora de inicio.
        fecha_final_cita (datetime): Fecha y hora de finalización.
        motivo_cita (str): Motivo de la cita.
        animal_id (UUID): Referencia al animal.
        vacuna_id (UUID): Referencia a la vacuna.
        veterinario_id (UUID): Referencia al veterinario.
        usuario_id_creacion (UUID): Usuario que creó el registro.
        usuario_id_edicion (UUID): Usuario que editó el registro.
        fecha_creacion (datetime): Fecha de creación.
        fecha_actualizacion (datetime): Última actualización.

    Relaciones:
        animal, vacuna, facturas, veterinario.

    Métodos:
        agendar_cita(): Retorna una cadena con la cita agendada.
    """

    id_cita = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False
    )
    fecha_inicio_cita = Column(DateTime, nullable=False)
    fecha_final_cita = Column(DateTime, nullable=True)
    motivo_cita = Column(String(200), nullable=False)

    animal_id = Column(
        UUID(as_uuid=True), ForeignKey("animales.id_animal"), nullable=False
    )
    vacuna_id = Column(
        UUID(as_uuid=True), ForeignKey("vacunas.id_vacuna"), nullable=True
    )
    veterinario_id = Column(
        UUID(as_uuid=True), ForeignKey("veterinarios.id_veterinario"), nullable=False
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
    animal = relationship("Animal", back_populates="citas")
    vacuna = relationship("Vacuna", back_populates="citas")
    facturas = relationship(
        "Factura", back_populates="cita", cascade="all, delete-orphan"
    )
    veterinario = relationship("Veterinario", back_populates="citas")

    def agendar_cita(self) -> str:
        return (
            f"Cita para {self.animal.nombre_animal} "
            f"el {self.fecha_inicio_cita.strftime('%d/%m/%Y %H:%M')} "
            f"- Motivo: {self.motivo_cita}"
        )
