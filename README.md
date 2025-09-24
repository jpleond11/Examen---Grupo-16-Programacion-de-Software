# Sistema de Gestión de Clínica Veterinaria

Este proyecto es un sistema de gestión para una clínica veterinaria, desarrollado en **Python** utilizando **SQLAlchemy** como ORM y **PostgreSQL (Neon Database)** como motor de base de datos.  

El sistema permite administrar usuarios, propietarios, animales, veterinarios, citas, vacunas y facturas. Incluye autenticación de usuarios mediante un sistema de inicio de sesión.

---

## Características

- **Login y autenticación** con creación automática de usuario administrador si no existen usuarios registrados.  
- **CRUD completo** para las siguientes entidades:
  - Usuarios
  - Propietarios
  - Animales
  - Veterinarios
  - Citas
  - Vacunas
  - Facturas  
- **PostgreSQL + SQLAlchemy ORM** con soporte para UUID.  

---

## Requisitos

- Python 3.10 o superior  
- PostgreSQL (Neon u otra instancia)  
- Instalar dependencias:  

''bash
- Ejecutar el comando: "pip install sqlalchemy psycopg2-binary"

## Configuración
DATABASE_URL = "postgresql+psycopg2://usuario:password@host:puerto/nombre_bd"

## Ejecución
python main.py

- Si no existen usuarios en la base de datos, se creará automáticamente:
- Usuario: admin
- Contraseña: admin123
- Rol: Administrador

## Ejemplo de uso
1. Ejecua el programa:
- python main.py

2. Ingresa las credenciales:
--- INICIO DE SESIÓN ---
Nombre de usuario: admin
Contraseña: admin123
Bienvenido Admin Root

3. Selecciona una opción del menú principal:
--- CLÍNICA VETERINARIA ---
1. Menú Usuarios
2. Menú Propietarios
3. Menú Mascotas
4. Menú Veterinarios
5. Menú Citas
6. Menú Vacunas
7. Menú Facturas
8. Salir
Selecciona una opción: 2

4. Usa el submenú CRUD correspondiente:
--- PROPIETARIOS ---
1. Crear
2. Ver todos
3. Ver por ID
4. Actualizar
5. Eliminar
6. Volver al menú principal
Seleccione: 1

## Ejemplo de creación de propietario:
--- Crear Propietario ---
Primer nombre: Juan
Segundo nombre (opcional, enter para omitir): Carlos
Primer apellido: Pérez
Segundo apellido: Gómez
Teléfono: 3001234567
Dirección: Calle 45 # 12 - 34
Propietario creado: Juan Pérez

## Estructura del proyecto
.
├── crud/
│   ├── animal_crud.py
│   ├── cita_crud.py
│   ├── factura_crud.py
│   ├── propietario_crud.py
│   ├── usuario_crud.py
│   ├── vacuna_crud.py
│   └── veterinario_crud.py
├── database/
│   └── config.py
├── Entidades/
│   ├── (modelos ORM de las entidades)
├── main.py   # Menú principal

## Futuras mejoras
- Validación avanzada de datos.
- Migrar a API REST con FastAPI o Flask.
- Reportes automáticos en PDF.
- Interfaz gráfica o cliente web.