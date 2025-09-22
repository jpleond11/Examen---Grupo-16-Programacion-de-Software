"""
Configuración de la base de datos PostgreSQL con Neon
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos Neon PostgreSQL
# Obtener la URL completa de conexión desde las variables de entorno
DATABASE_URL = (
    os.getenv("DATABASE_URL")
    or "postgresql://neondb_owner:npg_31HWAoYpQMJe@ep-curly-shape-adaq5kuo-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)

# Crear el motor de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Mostrar las consultas SQL en consola
    pool_pre_ping=True,  # Verificar conexión antes de usar
    pool_recycle=300,  # Reciclar conexiones cada 5 minutos
)

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


def get_db():
    """
    Generador de sesiones de base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Crear todas las tablas definidas en los modelos
    """
    # Importar todos los modelos para que se registren en Base.metadata
    from Entidades.AnimalORM import Animal
    from Entidades.CategoriaAnimalORM import CategoriaAnimal
    from Entidades.CitaORM import Cita
    from Entidades.FacturaORM import Factura
    from Entidades.PropietarioORM import Propietario
    from Entidades.UsuarioORM import Usuario
    from Entidades.VacunaORM import Vacuna
    from Entidades.VeterinarioORM import Veterinario

    Base.metadata.create_all(bind=engine)
