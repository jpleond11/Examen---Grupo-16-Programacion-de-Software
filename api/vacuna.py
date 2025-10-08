from crud.vacuna_crud import VacunaCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from schemas import VacunaCreate, VacunaUpdate, VacunaResponse, RespuestaAPI

router = APIRouter(prefix="/vacunas", tags=["vacunas"])


@router.get("/", response_model=List[VacunaResponse])
async def obtener_vacunas(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtener todas las vacunas con paginación."""
    try:
        vacuna_crud = VacunaCRUD(db)
        vacunas = vacuna_crud.obtener_vacunas(skip=skip, limit=limit)
        return vacunas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener vacunas: {str(e)}",
        )


@router.get("/{vacuna_id}", response_model=VacunaResponse)
async def obtener_vacuna(vacuna_id: UUID, db: Session = Depends(get_db)):
    """Obtener una vacuna por ID."""
    try:
        vacuna_crud = VacunaCRUD(db)
        vacuna = vacuna_crud.obtener_vacuna(vacuna_id)
        if not vacuna:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vacuna no encontrada"
            )
        return vacuna
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener vacuna: {str(e)}",
        )


@router.post("/", response_model=VacunaResponse, status_code=status.HTTP_201_CREATED)
async def crear_vacuna(vacuna_data: VacunaCreate, db: Session = Depends(get_db)):
    """Crear una nueva vacuna."""
    try:
        vacuna_crud = VacunaCRUD(db)
        vacuna = vacuna_crud.crear_vacuna(
            nombre_vacuna=vacuna_data.nombre_vacuna,
            fecha_aplicacion_vacuna=vacuna_data.fecha_aplicacion_vacuna,
            proxima_dosis_vacuna=vacuna_data.proxima_dosis_vacuna,
            usuario_id_creacion=vacuna_data.usuario_id_creacion,
        )
        return vacuna
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear vacuna: {str(e)}",
        )


@router.put("/{vacuna_id}", response_model=VacunaResponse)
async def actualizar_vacuna(
    vacuna_id: UUID, vacuna_data: VacunaUpdate, db: Session = Depends(get_db)
):
    """Actualizar una vacuna existente."""
    try:
        vacuna_crud = VacunaCRUD(db)

        vacuna_existente = vacuna_crud.obtener_vacuna(vacuna_id)
        if not vacuna_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vacuna no encontrada"
            )

        campos_actualizacion = {
            k: v for k, v in vacuna_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return vacuna_existente

        usuario_id_edicion = campos_actualizacion.pop("usuario_id_edicion", None)

        vacuna_actualizada = vacuna_crud.actualizar_vacuna(
            vacuna_id, usuario_id_edicion=usuario_id_edicion, **campos_actualizacion
        )
        return vacuna_actualizada
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar vacuna: {str(e)}",
        )


@router.delete("/{vacuna_id}", response_model=RespuestaAPI)
async def eliminar_vacuna(vacuna_id: UUID, db: Session = Depends(get_db)):
    """Eliminar una vacuna."""
    try:
        vacuna_crud = VacunaCRUD(db)

        vacuna_existente = vacuna_crud.obtener_vacuna(vacuna_id)
        if not vacuna_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vacuna no encontrada"
            )

        eliminada = vacuna_crud.eliminar_vacuna(vacuna_id)
        if eliminada:
            return RespuestaAPI(mensaje="Vacuna eliminada exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar vacuna",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar vacuna: {str(e)}",
        )
