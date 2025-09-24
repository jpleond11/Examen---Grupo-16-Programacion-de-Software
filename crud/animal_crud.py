"""
Operaciones CRUD para Animal
"""

from typing import List, Optional
from uuid import UUID
from datetime import date

from sqlalchemy.orm import Session
from Entidades.AnimalORM import Animal


class AnimalCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_animal(
        self,
        nombre_animal: str,
        especie_animal: str,
        fecha_nacimiento_animal: date,
        propietario_id: UUID,
        categoria_id: UUID,
        usuario_id_creacion: UUID,
    ) -> Animal:
        """
        Crea un nuevo registro de Animal en la base de datos.

        Args:
            nombre_animal: Nombre del animal (máx. 50 caracteres).
            especie_animal: Especie del animal (máx. 20 caracteres).
            fecha_nacimiento_animal: Fecha de nacimiento del animal.
            propietario_id: UUID del propietario asociado.
            categoria_id: UUID de la categoría del animal.
            usuario_id_creacion: UUID del usuario que crea el registro.

        Returns:
            El objeto `Animal` creado.

        Raises:
            ValueError: Si se violan validaciones (nombre/especie vacíos o inexistencia de usuario).
        """
        if not nombre_animal or len(nombre_animal.strip()) == 0:
            raise ValueError("El nombre del animal es obligatorio")
        if len(nombre_animal) > 50:
            raise ValueError("El nombre del animal no puede exceder 50 caracteres")

        if not especie_animal or len(especie_animal.strip()) == 0:
            raise ValueError("La especie es obligatoria")
        if len(especie_animal) > 20:
            raise ValueError("La especie no puede exceder 20 caracteres")

        if usuario_id_creacion is not None:
            from Entidades.UsuarioORM import Usuario

            usuario = (
                self.db.query(Usuario)
                .filter(Usuario.id_usuario == usuario_id_creacion)
                .first()
            )
            if not usuario:
                raise ValueError("El usuario especificado no existe")
        else:
                raise ValueError("Debe proporcionar un usuario_id_creacion")

        animal = Animal(
            nombre_animal=nombre_animal.strip(),
            especie_animal=especie_animal.strip(),
            fecha_nacimiento_animal=fecha_nacimiento_animal,
            propietario_id=propietario_id,
            categoria_id=categoria_id,
            usuario_id_creacion=usuario_id_creacion,
        )
        self.db.add(animal)
        self.db.commit()
        self.db.refresh(animal)
        return animal

    def obtener_animal(self, animal_id: UUID) -> Optional[Animal]:
        """
        Obtiene un animal por su UUID.

        Args:
            animal_id: UUID del animal a consultar.
        Returns:    
            Objeto `Animal` si existe, o `None` si no se encuentra.
        """
        return self.db.query(Animal).filter(Animal.id_animal == animal_id).first()

    def obtener_animales(self, skip: int = 0, limit: int = 100) -> List[Animal]:
        """
        Obtiene una lista paginada de animales.

        Args: 
            skip: Número de registros a omitir (por defecto 0).
            limit: Número máximo de registros a devolver (por defecto 100).
        Returns: 
            Lista de objetos `Animal`.
        """
        return self.db.query(Animal).offset(skip).limit(limit).all()

    def obtener_animales_por_propietario(self, propietario_id: UUID) -> List[Animal]:
        """
        Obtiene todos los animales asociados a un propietario específico.

        Args:
            propietario_id: UUID del propietario.
        Returns:
            Lista de objetos `Animal`.
        """
        return (
            self.db.query(Animal).filter(Animal.propietario_id == propietario_id).all()
        )

    def actualizar_animal(
        self, animal_id: UUID, usuario_id_edicion: UUID, **kwargs
    ) -> Optional[Animal]:
        """
        Actualiza los datos de un animal existente.

        Args:
            animal_id: UUID del animal a actualizar.
            usuario_id_edicion: UUID del usuario que edita el registro.
            kwargs: Campos a actualizar (ejemplo: `nombre_animal`, `especie_animal`).
        Raises:    
            ValueError: Si se violan validaciones (nombre/especie vacíos o muy largos).
        Returns:
            Objeto `Animal` actualizado, o `None` si no existe.
        """
        animal = self.obtener_animal(animal_id)
        if not animal:
            return None

        if "nombre_animal" in kwargs:
            nombre = kwargs["nombre_animal"]
            if not nombre or len(nombre.strip()) == 0:
                raise ValueError("El nombre del animal es obligatorio")
            if len(nombre) > 50:
                raise ValueError("El nombre no puede exceder 50 caracteres")
            kwargs["nombre_animal"] = nombre.strip()

        if "especie_animal" in kwargs:
            especie = kwargs["especie_animal"]
            if not especie or len(especie.strip()) == 0:
                raise ValueError("La especie es obligatoria")
            if len(especie) > 20:
                raise ValueError("La especie no puede exceder 20 caracteres")
            kwargs["especie_animal"] = especie.strip()

        kwargs["usuario_id_edicion"] = usuario_id_edicion

        for key, value in kwargs.items():
            if hasattr(animal, key):
                setattr(animal, key, value)

        self.db.commit()
        self.db.refresh(animal)
        return animal

    def eliminar_animal(self, animal_id: UUID) -> bool:
        """
        Elimina un animal de la base de datos.

        Args:
            animal_id: UUID del animal a eliminar.
        Returns:
             `True` si el animal fue eliminado, `False` si no existía.
        """
        animal = self.obtener_animal(animal_id)
        if animal:
            self.db.delete(animal)
            self.db.commit()
            return True
        return False
