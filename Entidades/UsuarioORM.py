from database.config import Base
from sqlalchemy import Column, String, Date, Text
from sqlalchemy.orm import relationship
from uuid import UUID, uuid4


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False
    )
    primer_nombre_usuario = Column(String(50), nullable=False, index=True)
    segundo_nombre_usuario = Column(String(50), nullable=True, index=True)
    primer_apellido_usuario = Column(String(50), nullable=False, index=True)
    segundo_apellido_usuario = Column(String(50), nullable=True, index=True)
    rol_usuario = Column(Text, nullable=False)
    fecha_nacimiento_usuario = Column(Date, nullable=False)
    nombre_usuario = Column(String(50), nullable=False, index=True)
    password = Column(String(50), nullable=False, index=True)

    """ Relaciones """
    propietarios = relationship(
        "Propietario", back_populates="usuario", cascade="all, delete-orphan"
    )
