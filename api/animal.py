from crud.animal_crud import AnimalCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from schemas import AnimalCreate, AnimalResponse, AnimalUpdate, RespuestaAPI

"""
Módulo de rutas para la gestión de animales.

Este archivo define los endpoints relacionados con las operaciones CRUD de animales.
Incluye funciones para obtener, crear, actualizar y eliminar registros en la base de datos.

Endpoints:
- GET /animales/ : Lista todos los animales con paginación.
- GET /animales/{animal_id} : Obtiene un animal por su ID.
- POST /animales/ : Crea un nuevo animal.
- PUT /animales/{animal_id} : Actualiza un animal existente.
- DELETE /animales/{animal_id} : Elimina un animal.
"""

router = APIRouter(prefix="/animales", tags=["animales"])


@router.get("/", response_model=List[AnimalResponse])
async def obtener_animales(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtener todos los animales con paginación."""
    try:
        animal_crud = AnimalCRUD(db)
        animales = animal_crud.obtener_animales(skip=skip, limit=limit)
        return animales
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener animales: {str(e)}",
        )


@router.get("/{animal_id}", response_model=AnimalResponse)
async def obtener_animal(animal_id: UUID, db: Session = Depends(get_db)):
    """Obtener un animal por ID."""
    try:
        animal_crud = AnimalCRUD(db)
        animal = animal_crud.obtener_animal(animal_id)
        if not animal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Animal no encontrado"
            )
        return animal
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener animal: {str(e)}",
        )


@router.post("/", response_model=AnimalResponse, status_code=status.HTTP_201_CREATED)
async def crear_animal(animal_data: AnimalCreate, db: Session = Depends(get_db)):
    """Crear un nuevo animal."""
    try:
        animal_crud = AnimalCRUD(db)
        animal = animal_crud.crear_animal(
            nombre_animal=animal_data.nombre_animal,
            especie_animal=animal_data.especie_animal,
            fecha_nacimiento_animal=animal_data.fecha_nacimiento_animal,
            propietario_id=animal_data.propietario_id,
            categoria_id=animal_data.categoria_id,
            usuario_id_creacion=animal_data.usuario_id_creacion,
        )
        return animal
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear animal: {str(e)}",
        )


@router.put("/{animal_id}", response_model=AnimalResponse)
async def actualizar_animal(
    animal_id: UUID, animal_data: AnimalUpdate, db: Session = Depends(get_db)
):
    """Actualizar un animal existente."""
    try:
        animal_crud = AnimalCRUD(db)

        # Verificar que el animal existe
        animal_existente = animal_crud.obtener_animal(animal_id)
        if not animal_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Animal no encontrado"
            )

        # Filtrar campos None para actualización
        campos_actualizacion = {
            k: v for k, v in animal_data.dict().items() if v is not None
        }

        usuario_id_edicion = campos_actualizacion.pop("usuario_id_edicion", None)

        if not campos_actualizacion:
            return animal_existente

        animal_actualizado = animal_crud.actualizar_animal(
            animal_id,
            usuario_id_edicion=usuario_id_edicion,
            **campos_actualizacion,
        )
        return animal_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar animal: {str(e)}",
        )


@router.delete("/{animal_id}", response_model=RespuestaAPI)
async def eliminar_animal(animal_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un animal."""
    try:
        animal_crud = AnimalCRUD(db)

        # Verificar que el animal existe
        animal_existente = animal_crud.obtener_animal(animal_id)
        if not animal_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Animal no encontrado"
            )

        eliminado = animal_crud.eliminar_animal(animal_id)
        if eliminado:
            return RespuestaAPI(mensaje="Animal eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar animal",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar animal: {str(e)}",
        )
