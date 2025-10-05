"""
Modelos Pydantic para las respuestas de la API
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


# Modelos base para Usuario
class UsuarioBase(BaseModel):
    nombre: str
    nombre_usuario: str
    email: EmailStr
    telefono: Optional[str] = None
    es_admin: bool = False


class UsuarioCreate(UsuarioBase):
    contraseña: str


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    nombre_usuario: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    es_admin: Optional[bool] = None
    activo: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    id: UUID
    activo: bool
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True


class UsuarioLogin(BaseModel):
    nombre_usuario: str
    contraseña: str


class CambioContraseña(BaseModel):
    contraseña_actual: str
    nueva_contraseña: str

# Modelo para cita
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

# Modelo para factura
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

# Modelos base para Animal
class AnimalBase(BaseModel):
    nombre_animal: str
    especie: str
    raza: Optional[str] = None
    edad: Optional[int] = None
    peso: Optional[float] = None
    propietario_id: UUID
    usuario_id_creacion: UUID
    usuario_id_edicion: Optional[UUID] = None

class AnimalCreate(AnimalBase):
    pass

class AnimalUpdate(BaseModel):
    nombre_animal: Optional[str] = None
    especie: Optional[str] = None
    raza: Optional[str] = None
    edad: Optional[int] = None
    peso: Optional[float] = None
    propietario_id: Optional[UUID] = None
    usuario_id_edicion: Optional[UUID] = None

class AnimalResponse(AnimalBase):
    id_animal: UUID
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True

# Modelos base para Propietario
class PropietarioBase(BaseModel):
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    usuario_id_creacion: UUID
    usuario_id_edicion: Optional[UUID] = None

class PropietarioCreate(PropietarioBase):
    pass

class PropietarioUpdate(BaseModel):
    primer_nombre: Optional[str] = None
    segundo_nombre: Optional[str] = None
    primer_apellido: Optional[str] = None
    segundo_apellido: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    usuario_id_edicion: Optional[UUID] = None

class PropietarioResponse(PropietarioBase):
    id_propietario: UUID
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True

# Modelos base para Veterinario
class VeterinarioBase(BaseModel):
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    especialidad: Optional[str] = None
    telefono: Optional[str] = None
    email: EmailStr
    usuario_id_creacion: UUID
    usuario_id_edicion: Optional[UUID] = None   

class VeterinarioCreate(VeterinarioBase):
    pass

class VeterinarioUpdate(BaseModel):
    primer_nombre: Optional[str] = None
    segundo_nombre: Optional[str] = None
    primer_apellido: Optional[str] = None
    segundo_apellido: Optional[str] = None
    especialidad: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    usuario_id_edicion: Optional[UUID] = None

class VeterinarioResponse(VeterinarioBase):
    id_veterinario: UUID
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True

# Modelos base para Vacuna
class VacunaBase(BaseModel):
    nombre_vacuna: str
    descripcion_vacuna: Optional[str] = None
    fecha_administracion: Optional[datetime] = None
    proxima_dosis: Optional[datetime] = None
    animal_id: UUID
    usuario_id_creacion: UUID
    usuario_id_edicion: Optional[UUID] = None

class VacunaCreate(VacunaBase):
    pass

class VacunaUpdate(BaseModel):
    nombre_vacuna: Optional[str] = None
    descripcion_vacuna: Optional[str] = None
    fecha_administracion: Optional[datetime] = None
    proxima_dosis: Optional[datetime] = None
    animal_id: Optional[UUID] = None
    usuario_id_edicion: Optional[UUID] = None

class VacunaResponse(VacunaBase):
    id_vacuna: UUID
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True

# Modelos base para Rol
class RolBase(BaseModel):
    nombre_rol: str
    descripcion_rol: Optional[str] = None
    usuario_id_creacion: UUID
    usuario_id_edicion: Optional[UUID] = None

class RolCreate(RolBase):
    pass

class RolUpdate(BaseModel):
    nombre_rol: Optional[str] = None
    descripcion_rol: Optional[str] = None
    usuario_id_edicion: Optional[UUID] = None
    
class RolResponse(RolBase):
    id_rol: UUID
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
