from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class PropietarioORM(Base):
    __tablename__ = "propietarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=False)
    direccion = Column(String(200), nullable=False)

    animales = relationship("AnimalORM", back_populates="propietario")

# Clase base Animal
class AnimalORM(Base):
    __tablename__ = "animales"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    edad = Column(Integer, nullable=False)
    especie = Column(String(50), default="Desconocida")
    tipo = Column(String(50))  # discriminador de herencia

    propietario_id = Column(Integer, ForeignKey("propietarios.id"), nullable=False)
    propietario = relationship("PropietarioORM", back_populates="animales")
    __mapper_args__ = {
        "polymorphic_on": tipo,
        "polymorphic_identity": "animal"
    }

    vacunas = relationship("VacunaORM", back_populates="animal")
    citas = relationship("CitaORM", back_populates="animal")

    def mostrar_info(self) -> str:
        return f"Nombre: {self.nombre}, Edad: {self.edad}, Especie: {self.especie}, Propietario: {self.propietario.nombre}"

# Subclase Perro
class PerroORM(AnimalORM):
    __tablename__ = "perros"

    id = Column(Integer, ForeignKey("animales.id"), primary_key=True)
    raza = Column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "perro"
    }

    def mostrar_info(self):
        return super().mostrar_info() + f", Raza: {self.raza}"

# Subclase Gato
class GatoORM(AnimalORM):
    __tablename__ = "gatos"

    id = Column(Integer, ForeignKey("animales.id"), primary_key=True)
    color = Column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "gato"
    }

    def mostrar_info(self):
        return super().mostrar_info() + f", Color: {self.color}"

# Subclase Ave
class AveORM(AnimalORM):
    __tablename__ = "aves"

    id = Column(Integer, ForeignKey("animales.id"), primary_key=True)
    tipo_ave = Column(String(50))  # Ejemplo: "Loro", "Canario"

    __mapper_args__ = {
        "polymorphic_identity": "ave"
    }

    def mostrar_info(self):
        return super().mostrar_info() + f", Tipo de ave: {self.tipo_ave}"
    
from pydantic import BaseModel, constr

# ---- Propietario ----
class PropietarioBase(BaseModel):
    nombre: constr(min_length=1, max_length=100)
    telefono: constr(min_length=7, max_length=20)
    direccion: constr(min_length=5, max_length=200)

class PropietarioCreate(PropietarioBase):
    pass

class PropietarioRead(PropietarioBase):
    id: int
    class Config:
        orm_mode = True


# ---- Animal ----
class AnimalBase(BaseModel):
    nombre: constr(min_length=1, max_length=100)
    edad: int

class AnimalCreate(AnimalBase):
    propietario_id: int

class AnimalRead(AnimalBase):
    id: int
    especie: str
    propietario: PropietarioRead
    class Config:
        orm_mode = True


# ---- Perro ----
class PerroCreate(AnimalCreate):
    raza: str

class PerroRead(AnimalRead):
    raza: str


# ---- Gato ----
class GatoCreate(AnimalCreate):
    color: str

class GatoRead(AnimalRead):
    color: str


# ---- Ave ----
class AveCreate(AnimalCreate):
    tipo_ave: str

class AveRead(AnimalRead):
    tipo_ave: str
