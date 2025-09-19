"""
Sistema de gestión de citas de una clínica veterinaria con ORM SQLAlchemy y Neon PostgreSQL
Incluye sistema de autenticación con login
"""

import getpass
from typing import Optional

from crud.animal_crud import AnimalCRUD
from crud.cita_crud import CitaCRUD
from crud.factura_crud import FacturaCRUD
from crud.propietario_crud import PropietarioCRUD
from crud.usuario_crud import UsuarioCRUD
from crud.vacuna_crud import VacunaCRUD
from crud.veterinario_crud import VeterinarioCRUD
from database.config import SessionLocal, create_tables
from Entidades.AnimalORM import Animal
from Entidades.CategoriaAnimalORM import CategoriaAnimal
from Entidades.CitaORM import Cita
from Entidades.FacturaORM import Factura
from Entidades.PropietarioORM import Propietario
from Entidades.UsuarioORM import Usuario
from Entidades.VacunaORM import Vacuna
from Entidades.VeterinarioORM import Veterinario


class SistemaGestion:
    """Sistema principal de gestión con interfaz de consola y autenticación"""

    def __init__(self):
        """Inicializar el sistema"""
        self.db = SessionLocal()
        self.animal_crud = AnimalCRUD(self.db)
        self.cita_crud = CitaCRUD(self.db)
        self.factura_crud = FacturaCRUD(self.db)
        self.propietario_crud = PropietarioCRUD(self.db)
        self.usuario_crud = UsuarioCRUD(self.db)
        self.vacuna_crud = VacunaCRUD(self.db)
        self.veterinario_crud = VeterinarioCRUD(self.db)
        self.usuario_actual: Optional[Usuario] = None

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.db.close()

    def mostrar_pantalla_login(self) -> bool:
        """Mostrar pantalla de login y autenticar usuario"""
        print("\n" + "=" * 50)
        print("        SISTEMA DE GESTION DE CLÍNICA VETERINARIA")
        print("=" * 50)
        print("INICIAR SESION")
        print("=" * 50)

        intentos = 0
        max_intentos = 3
