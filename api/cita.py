from crud.cita_crud import CitaCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from schemas import CitaBase, CitaCreate, CitaResponse, CitaUpdate, RespuestaAPI

router = APIRouter(prefix="/citas", tags=["citas"])


@router.get("/", response_model=List[CitaResponse])
async def obtener_citas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener todas las citas con paginación."""
    try:
        cita_crud = CitaCRUD(db)
        citas = cita_crud.obtener_citas(skip=skip, limit=limit)
        return citas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener citas: {str(e)}",
        )


@router.get("/{cita_id}", response_model=CitaResponse)
async def obtener_cita(cita_id: UUID, db: Session = Depends(get_db)):
    """Obtener una cita por ID."""
    try:
        cita_crud = CitaCRUD(db)
        cita = cita_crud.obtener_cita(cita_id)
        if not cita:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada"
            )
        return cita
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener cita: {str(e)}",
        )


@router.post("/", response_model=CitaResponse, status_code=status.HTTP_201_CREATED)
async def crear_cita(cita_data: CitaCreate, db: Session = Depends(get_db)):
    """Crear una nueva cita."""
    try:
        cita_crud = CitaCRUD(db)
        cita = cita_crud.crear_cita(
            fecha_inicio_cita=cita_data.fecha_inicio_cita,
            fecha_final_cita=cita_data.fecha_final_cita,
            motivo_cita=cita_data.motivo_cita,
            animal_id=cita_data.animal_id,
            vacuna_id=cita_data.vacuna_id,
            veterinario_id=cita_data.veterinario_id,
            usuario_id_creacion=cita_data.usuario_id_creacion,
        )
        return cita
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear cita: {str(e)}",
        )


@router.put("/{cita_id}", response_model=CitaResponse)
async def actualizar_cita(
    cita_id: UUID, cita_data: CitaUpdate, db: Session = Depends(get_db)
):
    """Actualizar una cita existente."""
    try:
        cita_crud = CitaCRUD(db)

        # Verificar que la cita existe
        cita_existente = cita_crud.obtener_cita(cita_id)
        if not cita_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada"
            )

        # Filtrar solo campos no nulos
        campos_actualizacion = {
            k: v for k, v in cita_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return cita_existente

        cita_actualizada = cita_crud.actualizar_cita(
            cita_id, usuario_id_edicion=cita_data.usuario_id_edicion, **campos_actualizacion
        )
        return cita_actualizada
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar cita: {str(e)}",
        )


@router.delete("/{cita_id}", response_model=RespuestaAPI)
async def eliminar_cita(cita_id: UUID, db: Session = Depends(get_db)):
    """Eliminar una cita."""
    try:
        cita_crud = CitaCRUD(db)

        cita_existente = cita_crud.obtener_cita(cita_id)
        if not cita_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada"
            )

        eliminado = cita_crud.eliminar_cita(cita_id)
        if eliminado:
            return RespuestaAPI(mensaje="Cita eliminada exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar cita",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar cita: {str(e)}",
        )
