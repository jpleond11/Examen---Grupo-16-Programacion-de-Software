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
        Crea un nuevo registro de Vacuna en la base de datos.

        Args:
            nombre_vacuna: Nombre de la vacuna (obligatorio).
            fecha_aplicacion_vacuna: Fecha en la que se aplicó la vacuna.
            proxima_dosis_vacuna: Fecha de la próxima dosis (opcional).
            usuario_id_creacion: UUID del usuario que crea el registro.

        Returns:
            Objeto `Vacuna` creado.

        Raises:
            ValueError: Si el nombre está vacío o si el usuario de creación no es válido.
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
        Obtiene una vacuna por su UUID.

        Args:
            vacuna_id: UUID de la vacuna a consultar.

        Returns:
            Objeto `Vacuna` si existe, o `None` si no se encuentra.
        """
        return self.db.query(Vacuna).filter(Vacuna.id_vacuna == vacuna_id).first()

    def obtener_vacunas(self, skip: int = 0, limit: int = 100) -> List[Vacuna]:
        """
        Obtiene una lista paginada de vacunas.

        Args:
            skip: Número de registros a omitir (por defecto 0).
            limit: Número máximo de registros a devolver (por defecto 100).

        Returns:
            Lista de objetos `Vacuna`.
        """
        return self.db.query(Vacuna).offset(skip).limit(limit).all()

    def actualizar_vacuna(
        self, vacuna_id: UUID, usuario_id_edicion: UUID, **kwargs
    ) -> Optional[Vacuna]:
        """
        Actualiza los datos de una vacuna existente.

        Args:
            vacuna_id: UUID de la vacuna a actualizar.
            usuario_id_edicion: UUID del usuario que edita el registro.
            kwargs: Campos a actualizar (ejemplo: `nombre_vacuna`, `proxima_dosis_vacuna`).

        Returns:
            Objeto `Vacuna` actualizado, o `None` si no existe.

        Raises:
            ValueError: Si el nombre de la vacuna es inválido.
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
        Elimina una vacuna de la base de datos.

        Args:
            vacuna_id: UUID de la vacuna a eliminar.

        Returns:
            True si la vacuna fue eliminada, False si no existía.
        """
        vacuna = self.obtener_vacuna(vacuna_id)
        if vacuna:
            self.db.delete(vacuna)
            self.db.commit()
            return True
        return False
