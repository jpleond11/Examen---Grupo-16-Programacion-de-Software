"""
Operaciones CRUD para Propietario
"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from Entidades.PropietarioORM import Propietario


class PropietarioCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_propietario(
        self,
        primer_nombre: str,
        primer_apellido: str,
        segundo_nombre: Optional[str],
        segundo_apellido: str,
        telefono: str,
        direccion: str,
        usuario_id_creacion: UUID,
    ) -> Propietario:
        """
        Crear un nuevo propietario
        """
        if not primer_nombre or len(primer_nombre.strip()) == 0:
            raise ValueError("El primer nombre es obligatorio")
        if not primer_apellido or len(primer_apellido.strip()) == 0:
            raise ValueError("El primer apellido es obligatorio")
        if not segundo_apellido or len(segundo_apellido.strip()) == 0:
            raise ValueError("El segundo apellido es obligatorio")
        if not telefono or len(telefono.strip()) == 0:
            raise ValueError("El teléfono es obligatorio")
        if not direccion or len(direccion.strip()) == 0:
            raise ValueError("La dirección es obligatoria")
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

        propietario = Propietario(
            primer_nombre_propietario=primer_nombre.strip(),
            segundo_nombre_propietario=(
                segundo_nombre.strip() if segundo_nombre else None
            ),
            primer_apellido_propietario=primer_apellido.strip(),
            segundo_apellido_propietario=segundo_apellido.strip(),
            telefono=telefono.strip(),
            direccion=direccion.strip(),
            usuario_id_creacion=usuario_id_creacion,
        )

        self.db.add(propietario)
        self.db.commit()
        self.db.refresh(propietario)
        return propietario

    def obtener_propietario(self, propietario_id: UUID) -> Optional[Propietario]:
        """
        Obtener un propietario por ID
        """
        return (
            self.db.query(Propietario)
            .filter(Propietario.id_propietario == propietario_id)
            .first()
        )

    def obtener_propietarios(
        self, skip: int = 0, limit: int = 100
    ) -> List[Propietario]:
        """
        Obtener lista de propietarios con paginación
        """
        return self.db.query(Propietario).offset(skip).limit(limit).all()

    def buscar_por_nombre(self, nombre: str) -> List[Propietario]:
        """
        Buscar propietarios por primer o segundo nombre
        """
        return (
            self.db.query(Propietario)
            .filter(
                (Propietario.primer_nombre_propietario.ilike(f"%{nombre}%"))
                | (Propietario.segundo_nombre_propietario.ilike(f"%{nombre}%"))
            )
            .all()
        )

    def buscar_por_apellido(self, apellido: str) -> List[Propietario]:
        """
        Buscar propietarios por apellido (primer o segundo)
        """
        return (
            self.db.query(Propietario)
            .filter(
                (Propietario.primer_apellido_propietario.ilike(f"%{apellido}%"))
                | (Propietario.segundo_apellido_propietario.ilike(f"%{apellido}%"))
            )
            .all()
        )

    def actualizar_propietario(
        self, propietario_id: UUID, usuario_id_edicion: UUID, **kwargs
    ) -> Optional[Propietario]:
        """
        Actualizar un propietario
        """
        propietario = self.obtener_propietario(propietario_id)
        if not propietario:
            return None

        if "primer_nombre_propietario" in kwargs:
            if not kwargs["primer_nombre_propietario"].strip():
                raise ValueError("El primer nombre no puede estar vacío")
            kwargs["primer_nombre_propietario"] = kwargs[
                "primer_nombre_propietario"
            ].strip()

        if "primer_apellido_propietario" in kwargs:
            if not kwargs["primer_apellido_propietario"].strip():
                raise ValueError("El primer apellido no puede estar vacío")
            kwargs["primer_apellido_propietario"] = kwargs[
                "primer_apellido_propietario"
            ].strip()

        if "segundo_apellido_propietario" in kwargs:
            if not kwargs["segundo_apellido_propietario"].strip():
                raise ValueError("El segundo apellido no puede estar vacío")
            kwargs["segundo_apellido_propietario"] = kwargs[
                "segundo_apellido_propietario"
            ].strip()

        if "telefono" in kwargs:
            if not kwargs["telefono"].strip():
                raise ValueError("El teléfono no puede estar vacío")
            kwargs["telefono"] = kwargs["telefono"].strip()

        if "direccion" in kwargs:
            if not kwargs["direccion"].strip():
                raise ValueError("La dirección no puede estar vacía")
            kwargs["direccion"] = kwargs["direccion"].strip()

        kwargs["usuario_id_edicion"] = usuario_id_edicion

        for key, value in kwargs.items():
            if hasattr(propietario, key):
                setattr(propietario, key, value)

        self.db.commit()
        self.db.refresh(propietario)
        return propietario

    def eliminar_propietario(self, propietario_id: UUID) -> bool:
        """
        Eliminar un propietario
        """
        propietario = self.obtener_propietario(propietario_id)
        if propietario:
            self.db.delete(propietario)
            self.db.commit()
            return True
        return False
