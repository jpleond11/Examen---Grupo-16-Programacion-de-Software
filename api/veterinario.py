from crud.veterinario_crud import VeterinarioCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from schemas import (
    VeterinarioCreate,
    VeterinarioResponse,
    VeterinarioUpdate,
    RespuestaAPI,
)

"""
Módulo de rutas para la gestión de veterinarios.

Contiene los endpoints para realizar operaciones CRUD sobre los veterinarios.
Permite listar, obtener, crear, actualizar y eliminar registros de veterinarios.

Endpoints:
- GET /veterinarios/ : Lista todos los veterinarios con paginación.
- GET /veterinarios/{veterinario_id} : Obtiene un veterinario por su ID.
- POST /veterinarios/ : Crea un nuevo veterinario.
- PUT /veterinarios/{veterinario_id} : Actualiza un veterinario existente.
- DELETE /veterinarios/{veterinario_id} : Elimina un veterinario.
"""

router = APIRouter(prefix="/veterinarios", tags=["veterinarios"])


@router.get("/", response_model=List[VeterinarioResponse])
async def obtener_veterinarios(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtener todos los veterinarios con paginación."""
    try:
        veterinario_crud = VeterinarioCRUD(db)
        veterinarios = veterinario_crud.obtener_veterinarios(skip=skip, limit=limit)
        return veterinarios
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener veterinarios: {str(e)}",
        )


@router.get("/{veterinario_id}", response_model=VeterinarioResponse)
async def obtener_veterinario(veterinario_id: UUID, db: Session = Depends(get_db)):
    """Obtener un veterinario por ID."""
    try:
        veterinario_crud = VeterinarioCRUD(db)
        veterinario = veterinario_crud.obtener_veterinario(veterinario_id)
        if not veterinario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Veterinario no encontrado",
            )
        return veterinario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener veterinario: {str(e)}",
        )


@router.post(
    "/", response_model=VeterinarioResponse, status_code=status.HTTP_201_CREATED
)
async def crear_veterinario(
    veterinario_data: VeterinarioCreate, db: Session = Depends(get_db)
):
    """Crear un nuevo veterinario."""
    try:
        veterinario_crud = VeterinarioCRUD(db)
        veterinario = veterinario_crud.crear_veterinario(
            primer_nombre=veterinario_data.primer_nombre_veterinario,
            segundo_nombre=veterinario_data.segundo_nombre_veterinario,
            primer_apellido=veterinario_data.primer_apellido_veterinario,
            segundo_apellido=veterinario_data.segundo_apellido_veterinario,
            telefono=veterinario_data.telefono,
            email=veterinario_data.email,
            especialidad=veterinario_data.especialidad,
            usuario_id_creacion=veterinario_data.usuario_id_creacion,
        )
        return veterinario
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear veterinario: {str(e)}",
        )


@router.put("/{veterinario_id}", response_model=VeterinarioResponse)
async def actualizar_veterinario(
    veterinario_id: UUID,
    veterinario_data: VeterinarioUpdate,
    db: Session = Depends(get_db),
):
    """Actualizar un veterinario existente."""
    try:
        veterinario_crud = VeterinarioCRUD(db)

        veterinario_existente = veterinario_crud.obtener_veterinario(veterinario_id)
        if not veterinario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Veterinario no encontrado",
            )

        campos_actualizacion = {
            k: v for k, v in veterinario_data.dict().items() if v is not None
        }

        usuario_id_edicion = campos_actualizacion.pop("usuario_id_edicion", None)

        if not campos_actualizacion:
            return veterinario_existente

        veterinario_actualizado = veterinario_crud.actualizar_veterinario(
            veterinario_id,
            usuario_id_edicion=usuario_id_edicion,
            **campos_actualizacion,
        )
        return veterinario_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar veterinario: {str(e)}",
        )


@router.delete("/{veterinario_id}", response_model=RespuestaAPI)
async def eliminar_veterinario(veterinario_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un veterinario."""
    try:
        veterinario_crud = VeterinarioCRUD(db)

        veterinario_existente = veterinario_crud.obtener_veterinario(veterinario_id)
        if not veterinario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Veterinario no encontrado",
            )

        eliminado = veterinario_crud.eliminar_veterinario(veterinario_id)
        if eliminado:
            return RespuestaAPI(
                mensaje="Veterinario eliminado exitosamente", exito=True
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar veterinario",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar veterinario: {str(e)}",
        )
