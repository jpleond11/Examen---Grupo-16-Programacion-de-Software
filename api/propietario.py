from crud.propietario_crud import PropietarioCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from schemas import (
    PropietarioCreate,
    PropietarioResponse,
    PropietarioUpdate,
    RespuestaAPI,
)

"""
Módulo de rutas para la gestión de propietarios.

Incluye los endpoints para realizar operaciones CRUD sobre los propietarios.
Permite listar, crear, actualizar y eliminar propietarios en la base de datos.

Endpoints:
- GET /propietarios/ : Lista todos los propietarios con paginación.
- GET /propietarios/{propietario_id} : Obtiene un propietario por su ID.
- POST /propietarios/ : Crea un nuevo propietario.
- PUT /propietarios/{propietario_id} : Actualiza un propietario existente.
- DELETE /propietarios/{propietario_id} : Elimina un propietario.
"""

router = APIRouter(prefix="/propietarios", tags=["propietarios"])


@router.get("/", response_model=List[PropietarioResponse])
async def obtener_propietarios(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtener todos los propietarios con paginación."""
    try:
        propietario_crud = PropietarioCRUD(db)
        propietarios = propietario_crud.obtener_propietarios(skip=skip, limit=limit)
        return propietarios
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener propietarios: {str(e)}",
        )


@router.get("/{propietario_id}", response_model=PropietarioResponse)
async def obtener_propietario(propietario_id: UUID, db: Session = Depends(get_db)):
    """Obtener un propietario por ID."""
    try:
        propietario_crud = PropietarioCRUD(db)
        propietario = propietario_crud.obtener_propietario(propietario_id)
        if not propietario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Propietario no encontrado",
            )
        return propietario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener propietario: {str(e)}",
        )


@router.post(
    "/", response_model=PropietarioResponse, status_code=status.HTTP_201_CREATED
)
async def crear_propietario(
    propietario_data: PropietarioCreate, db: Session = Depends(get_db)
):
    """Crear un nuevo propietario."""
    try:
        propietario_crud = PropietarioCRUD(db)
        propietario = propietario_crud.crear_propietario(
            primer_nombre=propietario_data.primer_nombre_propietario,
            segundo_nombre=propietario_data.segundo_nombre_propietario,
            primer_apellido=propietario_data.primer_apellido_propietario,
            segundo_apellido=propietario_data.segundo_apellido_propietario,
            telefono=propietario_data.telefono,
            direccion=propietario_data.direccion,
            usuario_id_creacion=propietario_data.usuario_id_creacion,
        )
        return propietario
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear propietario: {str(e)}",
        )


@router.put("/{propietario_id}", response_model=PropietarioResponse)
async def actualizar_propietario(
    propietario_id: UUID,
    propietario_data: PropietarioUpdate,
    db: Session = Depends(get_db),
):
    """Actualizar un propietario existente."""
    try:
        propietario_crud = PropietarioCRUD(db)
        propietario_existente = propietario_crud.obtener_propietario(propietario_id)

        if not propietario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Propietario no encontrado",
            )

        campos_actualizacion = {
            k: v for k, v in propietario_data.dict().items() if v is not None
        }

        usuario_id_edicion = campos_actualizacion.pop("usuario_id_edicion", None)

        if not campos_actualizacion:
            return propietario_existente

        propietario_actualizado = propietario_crud.actualizar_propietario(
            propietario_id,
            usuario_id_edicion=usuario_id_edicion,
            **campos_actualizacion,
        )
        return propietario_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar propietario: {str(e)}",
        )


@router.delete("/{propietario_id}", response_model=RespuestaAPI)
async def eliminar_propietario(propietario_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un propietario."""
    try:
        propietario_crud = PropietarioCRUD(db)
        propietario_existente = propietario_crud.obtener_propietario(propietario_id)

        if not propietario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Propietario no encontrado",
            )

        eliminado = propietario_crud.eliminar_propietario(propietario_id)
        if eliminado:
            return RespuestaAPI(
                mensaje="Propietario eliminado exitosamente", exito=True
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar propietario",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar propietario: {str(e)}",
        )
