# Sistema de Gestión de Veterinaria

API REST desarrollada con **FastAPI**, **SQLAlchemy** y **PostgreSQL (Neon)** para la gestión integral de una clínica veterinaria.  
Permite administrar **usuarios, animales, propietarios, citas, facturas, vacunas y veterinarios** con validaciones y control de relaciones entre entidades.

---

## Características principales

- Gestión completa de entidades con operaciones **CRUD**.
- Validaciones avanzadas de campos y relaciones (fechas, montos, existencia de usuarios, etc.).
- Control de usuarios creadores y editores.
- Integración con **Neon PostgreSQL** mediante SQLAlchemy.
- Documentación automática en Swagger (`/docs`) y Redoc (`/redoc`).
- Soporte de **CORS** para integraciones externas.
- Schemas unificados en un solo archivo: `schemas.py`.

---

## Estructura del proyecto
Clínica Veterinaria
├── api/
│ ├── animal.py
│ ├── cita.py
│ ├── factura.py
│ ├── propietario.py
│ ├── usuario.py
│ ├── vacuna.py
│ └── veterinario.py
│
├── crud/
│ ├── AnimalCRUD.py
│ ├── CitaCRUD.py
│ ├── FacturaCRUD.py
│ ├── PropietarioCRUD.py
│ ├── UsuarioCRUD.py
│ ├── VacunaCRUD.py
│ └── VeterinarioCRUD.py
│
├── Entidades/
│ ├── Animal.py
│ ├── Cita.py
│ ├── Factura.py
│ ├── Propietario.py
│ ├── Usuario.py
│ ├── Vacuna.py
│ └── Veterinario.py
│
├── database/
│ └── config.py
│
├── schemas.py
├── main.py
├── requirements.txt
└── README.md

---

## Instalación y configuración

### 1. Clonar el repositorio

'''bash
git clone https://github.com/jpleond11/Examen-1---Grupo-16-Programacion-de-Software
cd Examen-1---Grupo-16-Programacion-de-Software

### 2. Crear entorno virtual

python3 -m venv venv
source venv/bin/activate      # Mac/Linux
# o en Windows:
# venv\Scripts\activate

### 3. Instalar dependencias

pip install -r requirements.txt

### 4. Configurar las variables de entorno

Crea un archivo .env dentro del directorio database/ con tu cadena de conexión:

DATABASE_URL=postgresql+psycopg2://usuario:contraseña@host/neon_db

## Ejecución del proyecto
Para correr el servidor, ejecuta el siguiente comando desde la raíz del proyecto:
-- python main.py
El servidor se iniciará en:
-- http://localhost:8000

## Documentación de la API
Una vez en ejecución, puedes acceder a:
Swagger UI: http://localhost:8000/docs
Redoc: http://localhost:8000/redoc

## Endpoints principales
| Módulo       | Endpoint base   | Descripción                                 |
| ------------ | --------------- | ------------------------------------------- |
| Usuarios     | `/usuarios`     | CRUD de usuarios y autenticación            |
| Animales     | `/animales`     | CRUD de animales y control de propietarios  |
| Propietarios | `/propietarios` | CRUD de propietarios                        |
| Veterinarios | `/veterinarios` | CRUD de veterinarios                        |
| Vacunas      | `/vacunas`      | CRUD de vacunas                             |
| Citas        | `/citas`        | CRUD de citas con validación de fechas      |
| Facturas     | `/facturas`     | CRUD de facturas y filtros por cita o fecha |

## Ejemplo de uso (usuarios)

POST /usuarios/crear:
{
  "primer_nombre_usuario": "Juan",
  "rol_usuario": "admin",
  "fecha_nacimiento_usuario": "1995-04-10",
  "nombre_usuario": "juanp",
  "password": "123456",
  "email_usuario": "juanp@example.com"
}

Respuesta:
{
  "mensaje": "Usuario creado correctamente",
  "usuario_id": 1
}

## Licencia

Este proyecto fue desarrollado con fines educativos y puede ser adaptado libremente.
Autores: Juan Pablo León Duque, Andrés David Villa Marín.