"""
Operaciones CRUD para Vacuna
"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from Entidades.VacunaORM import Vacuna


class VacunaCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_vacuna(
        self,
        nombre_vacuna: str,
        fecha_aplicacion_vacuna,
        proxima_dosis_vacuna=None,
        usuario_id_creacion: UUID = None,
    ) -> Vacuna:
        """
        Crear una nueva vacuna
        """
        if not nombre_vacuna or len(nombre_vacuna.strip()) == 0:
            raise ValueError("El nombre de la vacuna es obligatorio")

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

        vacuna = Vacuna(
            nombre_vacuna=nombre_vacuna.strip(),
            fecha_aplicacion_vacuna=fecha_aplicacion_vacuna,
            proxima_dosis_vacuna=proxima_dosis_vacuna,
            usuario_id_creacion=usuario_id_creacion,
        )
        self.db.add(vacuna)
        self.db.commit()
        self.db.refresh(vacuna)
        return vacuna

    def obtener_vacuna(self, vacuna_id: UUID) -> Optional[Vacuna]:
        """
        Obtener una vacuna por su ID
        """
        return self.db.query(Vacuna).filter(Vacuna.id_vacuna == vacuna_id).first()

    def obtener_vacunas(self, skip: int = 0, limit: int = 100) -> List[Vacuna]:
        """
        Obtener una lista de vacunas con paginación
        """
        return self.db.query(Vacuna).offset(skip).limit(limit).all()

    def actualizar_vacuna(
        self, vacuna_id: UUID, usuario_id_edicion: UUID, **kwargs
    ) -> Optional[Vacuna]:
        """
        Actualizar una vacuna
        """
        vacuna = self.obtener_vacuna(vacuna_id)
        if not vacuna:
            return None

        if "nombre_vacuna" in kwargs:
            nombre = kwargs["nombre_vacuna"]
            if not nombre or len(nombre.strip()) == 0:
                raise ValueError("El nombre de la vacuna es obligatorio")
            kwargs["nombre_vacuna"] = nombre.strip()

        for key, value in kwargs.items():
            if hasattr(vacuna, key):
                setattr(vacuna, key, value)

        vacuna.usuario_id_edicion = usuario_id_edicion
        self.db.commit()
        self.db.refresh(vacuna)
        return vacuna

    def eliminar_vacuna(self, vacuna_id: UUID) -> bool:
        """
        Eliminar una vacuna por ID
        """
        vacuna = self.obtener_vacuna(vacuna_id)
        if vacuna:
            self.db.delete(vacuna)
            self.db.commit()
            return True
        return False
