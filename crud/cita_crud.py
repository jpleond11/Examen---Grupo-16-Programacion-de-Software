"""
Operaciones CRUD para Cita
"""

from typing import List, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
from Entidades.CitaORM import Cita


class CitaCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_cita(
        self,
        fecha_inicio_cita: datetime,
        motivo_cita: str,
        animal_id: UUID,
        vacuna_id: UUID,
        veterinario_id: UUID,
        usuario_id_creacion: UUID,
        fecha_final_cita: Optional[datetime] = None,
    ) -> Cita:
        """
        Crear una nueva cita
        """
        if not motivo_cita or len(motivo_cita.strip()) == 0:
            raise ValueError("El motivo de la cita es obligatorio")
        if len(motivo_cita) > 200:
            raise ValueError("El motivo no puede exceder 200 caracteres")

        if fecha_final_cita and fecha_final_cita < fecha_inicio_cita:
            raise ValueError(
                "La fecha final no puede ser anterior a la fecha de inicio"
            )

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

        cita = Cita(
            fecha_inicio_cita=fecha_inicio_cita,
            fecha_final_cita=fecha_final_cita,
            motivo_cita=motivo_cita.strip(),
            animal_id=animal_id,
            vacuna_id=vacuna_id,
            veterinario_id=veterinario_id,
            usuario_id_creacion=usuario_id_creacion,
        )
        self.db.add(cita)
        self.db.commit()
        self.db.refresh(cita)
        return cita

    def obtener_cita(self, cita_id: UUID) -> Optional[Cita]:
        """
        Obtener una cita por ID
        """
        return self.db.query(Cita).filter(Cita.id_cita == cita_id).first()

    def obtener_citas(self, skip: int = 0, limit: int = 100) -> List[Cita]:
        """
        Obtener lista de citas con paginación
        """
        return self.db.query(Cita).offset(skip).limit(limit).all()

    def obtener_citas_por_animal(self, animal_id: UUID) -> List[Cita]:
        """
        Obtener todas las citas de un animal
        """
        return self.db.query(Cita).filter(Cita.animal_id == animal_id).all()

    def obtener_citas_por_veterinario(self, veterinario_id: UUID) -> List[Cita]:
        """
        Obtener todas las citas de un veterinario
        """
        return self.db.query(Cita).filter(Cita.veterinario_id == veterinario_id).all()

    def actualizar_cita(
        self, cita_id: UUID, usuario_id_edicion: UUID, **kwargs
    ) -> Optional[Cita]:
        """
        Actualizar una cita
        """
        cita = self.obtener_cita(cita_id)
        if not cita:
            return None

        if "motivo_cita" in kwargs:
            motivo = kwargs["motivo_cita"]
            if not motivo or len(motivo.strip()) == 0:
                raise ValueError("El motivo de la cita es obligatorio")
            if len(motivo) > 200:
                raise ValueError("El motivo no puede exceder 200 caracteres")
            kwargs["motivo_cita"] = motivo.strip()

        if "fecha_final_cita" in kwargs and kwargs["fecha_final_cita"]:
            if kwargs["fecha_final_cita"] < cita.fecha_inicio_cita:
                raise ValueError(
                    "La fecha final no puede ser anterior a la fecha de inicio"
                )

        kwargs["usuario_id_edicion"] = usuario_id_edicion

        for key, value in kwargs.items():
            if hasattr(cita, key):
                setattr(cita, key, value)

        self.db.commit()
        self.db.refresh(cita)
        return cita

    def eliminar_cita(self, cita_id: UUID) -> bool:
        """
        Eliminar una cita
        """
        cita = self.obtener_cita(cita_id)
        if cita:
            self.db.delete(cita)
