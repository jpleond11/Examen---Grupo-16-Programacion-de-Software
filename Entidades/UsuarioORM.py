from database.config import Base
from sqlalchemy import Column, String, Date, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4


class Usuario(Base):
    __tablename__ = "usuarios"

    """
    
    Atributos:
        id_usuario (UUID): Identificador único.
        primer_nombre_usuario (str): Primer nombre.
        segundo_nombre_usuario (str): Segundo nombre (opcional).
        primer_apellido_usuario (str): Primer apellido.
        segundo_apellido_usuario (str): Segundo apellido (opcional).
        rol_usuario (str): Rol asignado al usuario.
        fecha_nacimiento_usuario (date): Fecha de nacimiento.
        nombre_usuario (str): Nombre de usuario para acceso.
        password (str): Contraseña de acceso.

    Relaciones:
        propietarios: Lista de propietarios asociados al usuario.
    """

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
