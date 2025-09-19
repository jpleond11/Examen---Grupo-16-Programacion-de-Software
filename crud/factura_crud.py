"""
Operaciones CRUD para Factura
"""

from typing import List, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
from Entidades.FacturaORM import Factura


class FacturaCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_factura(
        self,
        monto_factura: float,
        descripcion_factura: str,
        cita_id: UUID,
        usuario_id_creacion: UUID,
        fecha_emision: Optional[datetime] = None,
    ) -> Factura:
        """
        Crear una nueva factura
        """
        if monto_factura <= 0:
            raise ValueError("El monto de la factura debe ser mayor a 0")

        if not descripcion_factura or len(descripcion_factura.strip()) == 0:
            raise ValueError("La descripción de la factura es obligatoria")

        if len(descripcion_factura) > 200:
            raise ValueError("La descripción no puede exceder 200 caracteres")

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

        factura = Factura(
            monto_factura=monto_factura,
            descripcion_factura=descripcion_factura.strip(),
            cita_id=cita_id,
            usuario_id_creacion=usuario_id_creacion,
            fecha_emision=fecha_emision or datetime.now(),
        )
        self.db.add(factura)
        self.db.commit()
        self.db.refresh(factura)
        return factura

    def obtener_factura(self, factura_id: UUID) -> Optional[Factura]:
        """
        Obtener una factura por ID
        """
        return self.db.query(Factura).filter(Factura.id_factura == factura_id).first()

    def obtener_facturas(self, skip: int = 0, limit: int = 100) -> List[Factura]:
        """
        Obtener lista de facturas con paginación
        """
        return self.db.query(Factura).offset(skip).limit(limit).all()

    def obtener_facturas_por_cita(self, cita_id: UUID) -> List[Factura]:
        """
        Obtener todas las facturas asociadas a una cita
        """
        return self.db.query(Factura).filter(Factura.cita_id == cita_id).all()

    def obtener_facturas_por_fecha(
        self, fecha_inicio: datetime, fecha_fin: datetime
    ) -> List[Factura]:
        """
        Obtener facturas emitidas en un rango de fechas
        """
        return (
            self.db.query(Factura)
            .filter(
                Factura.fecha_emision >= fecha_inicio,
                Factura.fecha_emision <= fecha_fin,
            )
            .all()
        )

    def actualizar_factura(
        self, factura_id: UUID, usuario_id_edicion: UUID, **kwargs
    ) -> Optional[Factura]:
        """
        Actualizar una factura
        """
        factura = self.obtener_factura(factura_id)
        if not factura:
            return None

        if "monto_factura" in kwargs:
            if kwargs["monto_factura"] <= 0:
                raise ValueError("El monto de la factura debe ser mayor a 0")

        if "descripcion_factura" in kwargs:
            descripcion = kwargs["descripcion_factura"]
            if not descripcion or len(descripcion.strip()) == 0:
                raise ValueError("La descripción de la factura es obligatoria")
            if len(descripcion) > 200:
                raise ValueError("La descripción no puede exceder 200 caracteres")
            kwargs["descripcion_factura"] = descripcion.strip()

        kwargs["usuario_id_edicion"] = usuario_id_edicion

        for key, value in kwargs.items():
            if hasattr(factura, key):
                setattr(factura, key, value)

        self.db.commit()
        self.db.refresh(factura)
        return factura

    def eliminar_factura(self, factura_id: UUID) -> bool:
        """
        Eliminar una factura
        """
        factura = self.obtener_factura(factura_id)
        if factura:
            self.db.delete(factura)
            self.db.commit()
            return True
        return False
