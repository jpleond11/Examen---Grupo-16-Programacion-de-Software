"""
Modelos Pydantic para las respuestas de la API
"""

from datetime import datetime, date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UsuarioBase(BaseModel):
    primer_nombre_usuario: str
    segundo_nombre_usuario: Optional[str] = None
    primer_apellido_usuario: str
    segundo_apellido_usuario: Optional[str] = None
    rol_usuario: str
    fecha_nacimiento_usuario: date
    nombre_usuario: str
    password: str


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioUpdate(BaseModel):
    primer_nombre_usuario: Optional[str] = None
    segundo_nombre_usuario: Optional[str] = None
    primer_apellido_usuario: Optional[str] = None
    segundo_apellido_usuario: Optional[str] = None
    rol_usuario: Optional[str] = None
    fecha_nacimiento_usuario: Optional[date] = None
    nombre_usuario: Optional[str] = None
    password: Optional[str] = None


class UsuarioResponse(UsuarioBase):
    id_usuario: UUID
    primer_nombre_usuario: str
    segundo_nombre_usuario: Optional[str]
    primer_apellido_usuario: str
    segundo_apellido_usuario: Optional[str]
    rol_usuario: str
    fecha_nacimiento_usuario: date
    nombre_usuario: str

    class Config:
        from_attributes = True


class CitaBase(BaseModel):
    fecha_inicio_cita: datetime
    fecha_final_cita: Optional[datetime] = None
    motivo_cita: str
    animal_id: UUID
    vacuna_id: Optional[UUID] = None
    veterinario_id: UUID
    usuario_id_creacion: UUID
    usuario_id_edicion: Optional[UUID] = None


class CitaCreate(CitaBase):
    pass


class CitaUpdate(BaseModel):
    fecha_inicio_cita: Optional[datetime] = None
    fecha_final_cita: Optional[datetime] = None
    motivo_cita: Optional[str] = None
    animal_id: Optional[UUID] = None
    vacuna_id: Optional[UUID] = None
    veterinario_id: Optional[UUID] = None
    usuario_id_edicion: Optional[UUID] = None


class CitaResponse(CitaBase):
    id_cita: UUID
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True


class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool
    detalle: Optional[str] = None
    data: Optional[dict] = None

    class Config:
        schema_extra = {
            "example": {
                "mensaje": "Operación exitosa",
                "exito": True,
                "detalle": "El usuario ha sido creado correctamente.",
                "data": {"id": "123e4567-e89b-12d3-a456-426614174000"},
            }
        }


class FacturaBase(BaseModel):
    monto_factura: float
    fecha_emision: Optional[datetime] = None
    descripcion_factura: str
    cita_id: UUID
    usuario_id_creacion: UUID
    usuario_id_edicion: Optional[UUID] = None


class FacturaCreate(FacturaBase):
    pass


class FacturaUpdate(BaseModel):
    monto_factura: Optional[float] = None
    fecha_emision: Optional[datetime] = None
    descripcion_factura: Optional[str] = None
    cita_id: Optional[UUID] = None
    usuario_id_edicion: Optional[UUID] = None


class FacturaResponse(FacturaBase):
    id_factura: UUID
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True


class AnimalBase(BaseModel):
    nombre_animal: str
    especie_animal: str
    fecha_nacimiento_animal: date
    propietario_id: UUID
    categoria_id: UUID
    usuario_id_creacion: UUID
    usuario_id_edicion: Optional[UUID] = None


class AnimalCreate(AnimalBase):
    pass


class AnimalUpdate(BaseModel):
    nombre_animal: Optional[str] = None
    especie_animal: Optional[str] = None
    fecha_nacimiento_animal: Optional[date] = None
    propietario_id: Optional[UUID] = None
    categoria_id: Optional[UUID] = None
    usuario_id_edicion: Optional[UUID] = None


class AnimalResponse(AnimalBase):
    id_animal: UUID
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True


class PropietarioBase(BaseModel):
    primer_nombre_propietario: str = Field(
        ..., max_length=50, description="Primer nombre del propietario"
    )
    segundo_nombre_propietario: Optional[str] = Field(
        None, max_length=50, description="Segundo nombre del propietario"
    )
    primer_apellido_propietario: str = Field(
        ..., max_length=50, description="Primer apellido del propietario"
    )
    segundo_apellido_propietario: str = Field(
        ..., max_length=50, description="Segundo apellido del propietario"
    )
    telefono: str = Field(
        ..., max_length=20, description="Número de teléfono del propietario"
    )
    direccion: str = Field(..., max_length=200, description="Dirección del propietario")
    usuario_id_creacion: UUID
    usuario_id_edicion: Optional[UUID] = None


class PropietarioCreate(PropietarioBase):
    pass


class PropietarioUpdate(BaseModel):
    primer_nombre_propietario: Optional[str] = Field(None, max_length=50)
    segundo_nombre_propietario: Optional[str] = Field(None, max_length=50)
    primer_apellido_propietario: Optional[str] = Field(None, max_length=50)
    segundo_apellido_propietario: Optional[str] = Field(None, max_length=50)
    telefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = Field(None, max_length=200)
    usuario_id_edicion: Optional[UUID] = None


class PropietarioResponse(PropietarioBase):
    id_propietario: UUID
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True


class VeterinarioBase(BaseModel):
    primer_nombre_veterinario: str
    segundo_nombre_veterinario: Optional[str] = None
    primer_apellido_veterinario: str
    segundo_apellido_veterinario: Optional[str] = None
    telefono: str
    email: EmailStr
    especialidad: str
    usuario_id_creacion: UUID
    usuario_id_edicion: Optional[UUID] = None


class VeterinarioCreate(VeterinarioBase):
    pass


class VeterinarioUpdate(BaseModel):
    primer_nombre_veterinario: Optional[str] = None
    segundo_nombre_veterinario: Optional[str] = None
    primer_apellido_veterinario: Optional[str] = None
    segundo_apellido_veterinario: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    especialidad: Optional[str] = None
    usuario_id_edicion: Optional[UUID] = None


class VeterinarioResponse(VeterinarioBase):
    id_veterinario: UUID
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True


class VacunaBase(BaseModel):
    nombre_vacuna: str
    fecha_aplicacion_vacuna: date
    proxima_dosis_vacuna: Optional[date] = None
    usuario_id_creacion: UUID
    usuario_id_edicion: Optional[UUID] = None


class VacunaCreate(VacunaBase):
    pass


class VacunaUpdate(BaseModel):
    nombre_vacuna: Optional[str] = None
    fecha_aplicacion_vacuna: Optional[date] = None
    proxima_dosis_vacuna: Optional[date] = None
    usuario_id_edicion: Optional[UUID] = None


class VacunaResponse(VacunaBase):
    id_vacuna: UUID
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
