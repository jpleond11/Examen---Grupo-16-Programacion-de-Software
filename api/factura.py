from crud.factura_crud import FacturaCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import datetime
from schemas import FacturaCreate, FacturaResponse, FacturaUpdate, RespuestaAPI

router = APIRouter(prefix="/facturas", tags=["facturas"])


@router.get("/", response_model=List[FacturaResponse])
async def obtener_facturas(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtener todas las facturas con paginación."""
    try:
        factura_crud = FacturaCRUD(db)
        facturas = factura_crud.obtener_facturas(skip=skip, limit=limit)
        return facturas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener facturas: {str(e)}",
        )


@router.get("/{factura_id}", response_model=FacturaResponse)
async def obtener_factura(factura_id: UUID, db: Session = Depends(get_db)):
    """Obtener una factura por ID."""
    try:
        factura_crud = FacturaCRUD(db)
        factura = factura_crud.obtener_factura(factura_id)
        if not factura:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada"
            )
        return factura
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener factura: {str(e)}",
        )


@router.post("/", response_model=FacturaResponse, status_code=status.HTTP_201_CREATED)
async def crear_factura(factura_data: FacturaCreate, db: Session = Depends(get_db)):
    """Crear una nueva factura."""
    try:
        factura_crud = FacturaCRUD(db)
        factura = factura_crud.crear_factura(
            monto_factura=factura_data.monto_factura,
            descripcion_factura=factura_data.descripcion_factura,
            cita_id=factura_data.cita_id,
            usuario_id_creacion=factura_data.usuario_id_creacion,
            fecha_emision=factura_data.fecha_emision or datetime.now(),
        )
        return factura
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear factura: {str(e)}",
        )


@router.put("/{factura_id}", response_model=FacturaResponse)
async def actualizar_factura(
    factura_id: UUID, factura_data: FacturaUpdate, db: Session = Depends(get_db)
):
    """Actualizar una factura existente."""
    try:
        factura_crud = FacturaCRUD(db)
        factura_existente = factura_crud.obtener_factura(factura_id)

        if not factura_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada"
            )

        campos_actualizacion = {
            k: v for k, v in factura_data.dict().items() if v is not None
        }

        usuario_id_edicion = campos_actualizacion.pop("usuario_id_edicion", None)

        if not campos_actualizacion:
            return factura_existente

        factura_actualizada = factura_crud.actualizar_factura(
            factura_id,
            usuario_id_edicion=usuario_id_edicion,
            **campos_actualizacion,
        )
        return factura_actualizada
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar factura: {str(e)}",
        )


@router.delete("/{factura_id}", response_model=RespuestaAPI)
async def eliminar_factura(factura_id: UUID, db: Session = Depends(get_db)):
    """Eliminar una factura."""
    try:
        factura_crud = FacturaCRUD(db)
        factura_existente = factura_crud.obtener_factura(factura_id)

        if not factura_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada"
            )

        eliminado = factura_crud.eliminar_factura(factura_id)
        if eliminado:
            return RespuestaAPI(mensaje="Factura eliminada exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar factura",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar factura: {str(e)}",
        )
