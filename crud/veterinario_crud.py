"""
Operaciones CRUD para Veterinario
"""

import re
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from Entidades.VeterinarioORM import Veterinario


class VeterinarioCRUD:
    def __init__(self, db: Session):
        self.db = db

    def _validar_email(self, email: str) -> bool:
        """
        Valida que el email tenga un formato correcto.

        Args:
            email: Dirección de correo a validar.

        Returns:
            True si el email tiene un formato válido, False en caso contrario.
        """
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def _validar_telefono(self, telefono: str) -> bool:
        """
        Valida que el teléfono tenga un formato correcto.

        Args:
            telefono: Número de teléfono a validar.

        Returns:
            True si el teléfono cumple el formato, False en caso contrario.
        """
        pattern = r"^\+?[\d\s\-\(\)]{7,15}$"
        return re.match(pattern, telefono) is not None

    def crear_veterinario(
        self,
        primer_nombre: str,
        primer_apellido: str,
        telefono: str,
        email: str,
        especialidad: str,
        segundo_nombre: str = None,
        segundo_apellido: str = None,
        usuario_id_creacion: UUID = None,
    ) -> Veterinario:
        """
        Crea un nuevo registro de Veterinario en la base de datos.

        Args:
            primer_nombre: Primer nombre del veterinario (obligatorio).
            primer_apellido: Primer apellido del veterinario (obligatorio).
            telefono: Teléfono del veterinario en formato válido.
            email: Dirección de correo electrónico única y válida.
            especialidad: Especialidad del veterinario.
            segundo_nombre: Segundo nombre del veterinario (opcional).
            segundo_apellido: Segundo apellido del veterinario (opcional).
            usuario_id_creacion: UUID del usuario que crea el registro.

        Returns:
            Objeto `Veterinario` creado.

        Raises:
            ValueError: Si algún campo obligatorio es inválido,
                        si el email ya existe o
                        si el usuario de creación no es válido.
        """
        if not primer_nombre or len(primer_nombre.strip()) == 0:
            raise ValueError("El primer nombre es obligatorio")

        if not primer_apellido or len(primer_apellido.strip()) == 0:
            raise ValueError("El primer apellido es obligatorio")

        if not self._validar_telefono(telefono):
            raise ValueError("El teléfono no tiene un formato válido")

        if not self._validar_email(email):
            raise ValueError("El email no tiene un formato válido")

        if (
            self.db.query(Veterinario)
            .filter(Veterinario.email == email.lower().strip())
            .first()
        ):
            raise ValueError("El email ya está registrado")

        if not especialidad or len(especialidad.strip()) == 0:
            raise ValueError("La especialidad es obligatoria")

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

        veterinario = Veterinario(
            primer_nombre_veterinario=primer_nombre.strip(),
            segundo_nombre_veterinario=(
                segundo_nombre.strip() if segundo_nombre else None
            ),
            primer_apellido_veterinario=primer_apellido.strip(),
            segundo_apellido_veterinario=(
                segundo_apellido.strip() if segundo_apellido else None
            ),
            telefono=telefono.strip(),
            email=email.lower().strip(),
            especialidad=especialidad.strip(),
            usuario_id_creacion=usuario_id_creacion,
        )
        self.db.add(veterinario)
        self.db.commit()
        self.db.refresh(veterinario)
        return veterinario

    def obtener_veterinario(self, veterinario_id: UUID) -> Optional[Veterinario]:
        """
        Obtiene un veterinario por su UUID.

        Args:
            veterinario_id: UUID del veterinario a consultar.

        Returns:
            Objeto `Veterinario` si existe, o `None` si no se encuentra.
        """
        return (
            self.db.query(Veterinario)
            .filter(Veterinario.id_veterinario == veterinario_id)
            .first()
        )

    def obtener_veterinarios(
        self, skip: int = 0, limit: int = 100
    ) -> List[Veterinario]:
        """
        Obtiene una lista paginada de veterinarios.

        Args:
            skip: Número de registros a omitir (por defecto 0).
            limit: Número máximo de registros a devolver (por defecto 100).

        Returns:
            Lista de objetos `Veterinario`.
        """
        return self.db.query(Veterinario).offset(skip).limit(limit).all()

    def actualizar_veterinario(
        self, veterinario_id: UUID, usuario_id_edicion: UUID, **kwargs
    ) -> Optional[Veterinario]:
        """
        Actualiza los datos de un veterinario existente.

        Args:
            veterinario_id: UUID del veterinario a actualizar.
            usuario_id_edicion: UUID del usuario que edita el registro.
            kwargs: Campos a actualizar (ejemplo: `telefono`, `email`, `especialidad`).

        Returns:
            Objeto `Veterinario` actualizado, o `None` si no existe.

        Raises:
            ValueError: Si el teléfono o email son inválidos,
                        o si el email ya está registrado.
        """
        veterinario = self.obtener_veterinario(veterinario_id)
        if not veterinario:
            return None

        if "telefono" in kwargs and kwargs["telefono"]:
            if not self._validar_telefono(kwargs["telefono"]):
                raise ValueError("Formato de teléfono inválido")
            kwargs["telefono"] = kwargs["telefono"].strip()

        if "email" in kwargs and kwargs["email"]:
            if not self._validar_email(kwargs["email"]):
                raise ValueError("Email inválido")
            if (
                self.db.query(Veterinario)
                .filter(Veterinario.email == kwargs["email"].lower().strip())
                .first()
            ):
                raise ValueError("El email ya está registrado")
            kwargs["email"] = kwargs["email"].lower().strip()

        for key, value in kwargs.items():
            if hasattr(veterinario, key):
                setattr(veterinario, key, value)

        veterinario.usuario_id_edicion = usuario_id_edicion
        self.db.commit()
        self.db.refresh(veterinario)
        return veterinario

    def eliminar_veterinario(self, veterinario_id: UUID) -> bool:
        """
        Elimina un veterinario de la base de datos.

        Args:
            veterinario_id: UUID del veterinario a eliminar.

        Returns:
            True si el veterinario fue eliminado, False si no existía.
        """
        veterinario = self.obtener_veterinario(veterinario_id)
        if veterinario:
            self.db.delete(veterinario)
            self.db.commit()
            return True
        return False
