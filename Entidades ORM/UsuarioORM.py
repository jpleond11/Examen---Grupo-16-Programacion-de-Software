from sqlalchemy import Column, String, DateTime, Text
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List
from uuid import UUID

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(UUID(as_uuid=True), primary_key=True, default=UUID.uuid4, unique=True, nullable=False)
    primer_nombre_usuario = Column(String(50), nullable=False, index=True)
    segundo_nombre_usuario = Column(String(50), nullable=True, index=True)
    primer_apellido_usuario = Column(String(50), nullable=False, index=True)
    segundo_apellido_usuario = Column(String(50), nullable=True, index=True)
    rol_usuario = Column(Text, nullable=False)
    fecha_nacimiento_usuario = Column(datetime, nullable=False)