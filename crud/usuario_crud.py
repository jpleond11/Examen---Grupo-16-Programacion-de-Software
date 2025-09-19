"""
Operaciones CRUD para Usuario
"""

from typing import List, Optional
from uuid import UUID
from datetime import date

from sqlalchemy.orm import Session
from Entidades.UsuarioORM import Usuario


class UsuarioCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_usuario(
        self,
        primer_nombre: str,
        primer_apellido: str,
        rol: str,
        fecha_nacimiento: date,
        nombre_usuario: str,
        password: str,
        segundo_nombre: Optional[str] = None,
        segundo_apellido: Optional[str] = None,
    ) -> Usuario:
        """
        Crear un nuevo usuario con validaciones mínimas
        """
        if not primer_nombre or len(primer_nombre.strip()) == 0:
            raise ValueError("El primer nombre es obligatorio")

        if not primer_apellido or len(primer_apellido.strip()) == 0:
            raise ValueError("El primer apellido es obligatorio")

        if not rol:
            raise ValueError("El rol del usuario es obligatorio")

        if not fecha_nacimiento:
            raise ValueError("La fecha de nacimiento es obligatoria")

        if not nombre_usuario:
            raise ValueError("El nombre de usuario es obligatorio")

        if self.obtener_usuario_por_nombre_usuario(nombre_usuario):
            raise ValueError("El nombre de usuario ya está registrado")

        if not password:
            raise ValueError("La contraseña es obligatoria")

        usuario = Usuario(
            primer_nombre_usuario=primer_nombre.strip(),
            segundo_nombre_usuario=segundo_nombre.strip() if segundo_nombre else None,
            primer_apellido_usuario=primer_apellido.strip(),
            segundo_apellido_usuario=(
                segundo_apellido.strip() if segundo_apellido else None
            ),
            rol_usuario=rol.strip(),
            fecha_nacimiento_usuario=fecha_nacimiento,
            nombre_usuario=nombre_usuario.strip().lower(),
            password=password.strip(),
        )

        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def obtener_usuario(self, usuario_id: UUID) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()

    def obtener_usuario_por_nombre_usuario(
        self, nombre_usuario: str
    ) -> Optional[Usuario]:
        return (
            self.db.query(Usuario)
            .filter(Usuario.nombre_usuario == nombre_usuario.lower().strip())
            .first()
        )

    def obtener_usuarios(self, skip: int = 0, limit: int = 100) -> List[Usuario]:
        return self.db.query(Usuario).offset(skip).limit(limit).all()

    def actualizar_usuario(self, usuario_id: UUID, **kwargs) -> Optional[Usuario]:
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            return None

        if "nombre_usuario" in kwargs:
            nuevo_nombre_usuario = kwargs["nombre_usuario"].lower().strip()
            existente = self.obtener_usuario_por_nombre_usuario(nuevo_nombre_usuario)
            if existente and existente.id_usuario != usuario_id:
                raise ValueError("El nombre de usuario ya está registrado")
            kwargs["nombre_usuario"] = nuevo_nombre_usuario

        if "password" in kwargs:
            nueva_password = kwargs["password"].strip()
            if len(nueva_password) < 6:
                raise ValueError("La contraseña debe tener al menos 6 caracteres")
            kwargs["password"] = nueva_password

        if "rol_usuario" in kwargs:
            nuevo_rol = kwargs["rol_usuario"].strip()
            if not nuevo_rol:
                raise ValueError("El rol no puede estar vacío")
            kwargs["rol_usuario"] = nuevo_rol

        for key, value in kwargs.items():
            if hasattr(usuario, key):
                setattr(usuario, key, value)

        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def eliminar_usuario(self, usuario_id: UUID) -> bool:
        usuario = self.obtener_usuario(usuario_id)
        if usuario:
            self.db.delete(usuario)
            self.db.commit()
            return True
        return False

    def autenticar_usuario(
        self, nombre_usuario: str, password: str
    ) -> Optional[Usuario]:
        usuario = self.obtener_usuario_por_nombre_usuario(nombre_usuario)
        if not usuario:
            return None

        if usuario.password != password:
            return None

        return usuario
