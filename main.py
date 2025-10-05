import uvicorn
from api import usuario, animal, cita  # Importar otros routers aquí
from database.config import create_tables
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Crear la aplicación FastAPI
app = FastAPI(
    title="Sistema de Gestión de Veterinaria",
    description="API REST para gestión de una veterinaria",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas del router de usuarios
app.include_router(usuario.router)
app.include_router(animal.router)
app.include_router(cita.router)
# TODO: Incluir otros routers aquí



# Menú principal
@app.on_event("startup")
async def startup_event():
    """Evento de inicio de la aplicación"""
    print("Iniciando Sistema de Gestión de Veterinaria...")
    print("Configurando base de datos...")
    create_tables()
    print("Sistema listo para usar.")
    print("Documentación disponible en: http://localhost:8000/docs")

@app.get("/", tags=["raíz"])
async def root():
    """Endpoint raíz que devuelve información básica de la API."""
    return {
        "mensaje": "Bienvenido al Sistema de Gestión de Veterinaria",
        "version": "1.0.0",
        "documentacion": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "usuarios": "/usuarios"},
    }

def main():
    """Función principal para ejecutar el servidor"""
    print("Iniciando servidor FastAPI...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Recargar automáticamente en desarrollo
        log_level="info",
    )

if __name__ == "__main__":
    main()

"""
Sistema de gestión de citas de una clínica veterinaria con ORM SQLAlchemy y Neon PostgreSQL
Incluye sistema de autenticación con login
"""

from typing import Optional
from datetime import datetime
from uuid import UUID

from crud.animal_crud import AnimalCRUD
from crud.cita_crud import CitaCRUD
from crud.factura_crud import FacturaCRUD
from crud.propietario_crud import PropietarioCRUD
from crud.usuario_crud import UsuarioCRUD
from crud.vacuna_crud import VacunaCRUD
from crud.veterinario_crud import VeterinarioCRUD
from database.config import SessionLocal, create_tables

class SistemaVeterinaria:
    def __init__(self):
        """ Inicialización del sistema """
        self.db = SessionLocal()
        self.animal_crud = AnimalCRUD(self.db)
        self.cita_crud = CitaCRUD(self.db)
        self.factura_crud = FacturaCRUD(self.db)
        self.propietario_crud = PropietarioCRUD(self.db)
        self.usuario_crud = UsuarioCRUD(self.db)
        self.vacuna_crud = VacunaCRUD(self.db)
        self.veterinario_crud = VeterinarioCRUD(self.db)

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.db.close()

def login(usuario_crud: UsuarioCRUD) -> UUID:
    print("\n--- BIENVENIDO AL PROGRAMA DE GESTIÓN DE LA CLÍNICA VETERINARIA ---")
    print("\n--- INICIO DE SESIÓN ---")
    while True:
        nombre_usuario = input("Nombre de usuario: ").strip().lower()
        password = input("Contraseña: ").strip()

        usuario = usuario_crud.autenticar_usuario(nombre_usuario, password)
        if usuario:
            print(f"\n Bienvenido {usuario.primer_nombre_usuario} {usuario.primer_apellido_usuario}")
            return usuario.id_usuario
        else:
            print("Usuario o contraseña incorrectos. Intente de nuevo")

def menu_principal():
    """ Ejecución del sistema de menú principal con sus opciones después de la autentificación """
    print("Iniciando sistema de gestión de la Clínica Veterinaria...")
    print("Configurando base de datos...")
    print("Sistema listo para usar.")

    print("\n--- CLÍNICA VETERINARIA ---")
    print("1. Menú Usuarios")
    print("2. Menú Propietarios")
    print("3. Menú Mascotas")
    print("4. Menú Veterinarios")
    print("5. Menú Citas")
    print("6. Menú Vacunas")
    print("7. Menú Facturas")
    print("8. Salir")

def submenu_crud(entidad: str):
    print(f"\n--- {entidad.upper()} ---")
    print("1. Crear")
    print("2. Ver todos")
    print("3. Ver por ID")
    print("4. Actualizar")
    print("5. Eliminar")
    print("6. Volver al menú principal")

def main() -> None:
    """ Sistema de login """
    create_tables()
    with SistemaVeterinaria() as sistema:
        if not sistema.usuario_crud.obtener_usuarios():
            print("No hay usuarios registrados. Creando usuario administrador por defecto...")
            sistema.usuario_crud.crear_usuario(
                primer_nombre="Admin",
                primer_apellido="Root",
                rol="Administrador",
                fecha_nacimiento=datetime(2000, 1, 1),
                nombre_usuario="admin",
                password="admin123"
            )

        usuario_id_creacion = login(sistema.usuario_crud)
        while True:
            menu_principal()
            opcion = input("Selecciona una opción: ")

            if opcion == "1":
                while True:
                    submenu_crud("Usuarios")
                    op = input("Seleccione: ")

                    if op == "1":
                        print("\n--- Crear Usuario ---")
                        primer_nombre = input("Primer nombre: ")
                        segundo_nombre = input("Segundo nombre (opcional, enter para omitir): ")
                        primer_apellido = input("Primer apellido: ")
                        segundo_apellido = input("Segundo apellido (opcional, enter para omitir): ")
                        rol = input("Rol: ")
                        fecha_nac = input("Fecha nacimiento (YYYY-MM-DD): ")
                        nombre_usuario = input("Nombre de usuario: ")
                        password = input("Contraseña: ")

                        usuario = sistema.usuario_crud.crear_usuario(
                            primer_nombre=primer_nombre,
                            segundo_nombre=segundo_nombre if segundo_nombre else None,
                            primer_apellido=primer_apellido,
                            segundo_apellido=segundo_apellido if segundo_apellido else None,
                            rol=rol,
                            fecha_nacimiento=datetime.strptime(fecha_nac, "%Y-%m-%d").date(),
                            nombre_usuario=nombre_usuario,
                            password=password
                        )
                        print("Usuario creado:", nombre_usuario)

                    elif op == "2":
                        usuarios = sistema.usuario_crud.obtener_usuarios()
                        for u in usuarios:
                            print(u.id_usuario, u.nombre_usuario, u.rol_usuario)    

                    elif op == "3":
                        uid = input("ID usuario: ")
                        usuario = sistema.usuario_crud.obtener_usuario(UUID(uid))
                        if usuario:
                            print("Usuario encontrado:", usuario.nombre_usuario)
                        else:
                            print("Usuario no encontrado")    
                        

                    elif op == "4":
                        uid = UUID(input("ID usuario a actualizar: "))
                        nuevo_nombre = input("Nuevo nombre de usuario (enter para omitir): ")
                        nueva_password = input("Nueva contraseña (enter para omitir): ")
                        cambios = {}
                        if nuevo_nombre:
                            cambios["nombre_usuario"] = nuevo_nombre
                        if nueva_password:
                            cambios["password"] = nueva_password
                        usuario = sistema.usuario_crud.actualizar_usuario(uid, **cambios)
                        print("Usuario actualizado:", nuevo_nombre)

                    elif op == "5":
                        uid = input("ID usuario a eliminar: ")
                        ok = sistema.usuario_crud.eliminar_usuario(UUID(uid))
                        print("Eliminado" if ok else "No encontrado")

                    elif op == "6":
                        break

                    else:
                        print("Opción inválida")
        
            elif opcion == "2":
                while True:
                    submenu_crud("Propietarios")
                    op = input("Seleccione: ")
                    if op == "1":
                        print("\n--- Crear Propietario ---")
                        primer_nombre = input("Primer nombre: ")
                        segundo_nombre = input("Segundo nombre (opcional, enter para omitir): ")
                        primer_apellido = input("Primer apellido: ")
                        segundo_apellido = input("Segundo apellido: ")
                        telefono = input("Teléfono: ")
                        direccion = input("Dirección: ")

                        propietario = sistema.propietario_crud.crear_propietario(
                            primer_nombre=primer_nombre,
                            primer_apellido=primer_apellido,
                            segundo_nombre=segundo_nombre if segundo_nombre else None,
                            segundo_apellido=segundo_apellido if segundo_apellido else None,
                            telefono=telefono,
                            direccion=direccion,
                            usuario_id_creacion=usuario_id_creacion
                        )
                        print("Propietario creado: ", {primer_nombre}, {primer_apellido})    

                    elif op == "2":
                        propietarios = sistema.propietario_crud.obtener_propietarios()
                        for p in propietarios:
                            print(p.id_propietario, p.primer_nombre_propietario, p.primer_apellido_propietario, p.segundo_apellido_propietario, p.telefono)

                    elif op == "3":
                        pid = input("ID propietario: ")
                        propietario = sistema.propietario_crud.obtener_propietario(UUID(pid))
                        if propietario:
                            print("Propietario encontrado:", propietario.mostrar_info())
                        else:
                            print("Propietario no encontrado")

                    elif op == "4":
                        pid = input("ID propietario: ")
                        nuevo_telefono = input("Nuevo teléfono: ")
                        nueva_direccion = input("Nueva dirección: ")
                        cambios = {}
                        if nuevo_telefono: 
                            cambios["telefono"] = nuevo_telefono
                        if nueva_direccion: 
                            cambios["direccion"] = nueva_direccion
                        propietario = sistema.propietario_crud.actualizar_propietario(UUID(pid), usuario_id_creacion, **cambios)
                        print("Propietario actualizado:", pid)

                    elif op == "5":
                        pid = input("ID propietario: ")
                        ok = sistema.propietario_crud.eliminar_propietario(UUID(pid))
                        print("Eliminado" if ok else "No encontrado")

                    elif op == "6":
                        break
                    else:
                        print("Opción inválida")

            elif opcion == "3":
                while True:
                    submenu_crud("Animales")
                    op = input("Seleccione: ")

                    if op == "1":
                        print("\n--- Crear Animal ---")
                        nombre = input("Nombre del animal: ")
                        especie = input("Especie: ")
                        fecha_nac = input("Fecha de nacimiento (YYYY-MM-DD): ")
                        propietario_id = input("ID propietario: ")

                        print("\n¿Ya tienes una categoría registrada?")
                        print("1. Usar ID de categoría existente")
                        print("2. Crear nueva categoría")
                        opcion_categoria = input("Seleccione: ")

                        if opcion_categoria == "1":
                            categoria_id = UUID(input("ID categoría: "))
                        elif opcion_categoria == "2":
                            from Entidades.CategoriaAnimalORM import CategoriaAnimal
                            nombre_cat = input("Nombre de la categoría: ")
                            descripcion = input("Descripción (opcional): ")

                            nueva_categoria = CategoriaAnimal(
                                nombre_categoria=nombre_cat.strip(),
                                descripcion=descripcion.strip() if descripcion else None
                            )
                            sistema.db.add(nueva_categoria)
                            sistema.db.commit()
                            sistema.db.refresh(nueva_categoria)
                            categoria_id = nueva_categoria.id_categoria_animal
                            print("Categoría creada:", nueva_categoria.nombre_categoria)
                        else:
                            print("Opción inválida, cancelando creación de animal.")
                            continue

                        animal = sistema.animal_crud.crear_animal(
                            nombre_animal=nombre,
                            especie_animal=especie,
                            fecha_nacimiento_animal=datetime.strptime(fecha_nac, "%Y-%m-%d").date(),
                            propietario_id=UUID(propietario_id),
                            categoria_id=categoria_id,
                            usuario_id_creacion=usuario_id_creacion
                        )
                        print("Animal creado:", nombre)


                    elif op == "2":
                        animales = sistema.animal_crud.obtener_animales()
                        for a in animales:
                            print(a.id_animal, a.nombre_animal, a.especie_animal)

                    elif op == "3":
                        aid = input("ID animal: ")
                        animal = sistema.animal_crud.obtener_animal(UUID(aid))
                        if animal:
                            print("Animal encontrado:", animal.mostrar_info())
                        else:
                            print("Animal no encontrado")

                    elif op == "4":
                        aid = input("ID animal a actualizar: ")
                        nombre = input("Nuevo nombre (enter para omitir): ")
                        especie = input("Nueva especie (enter para omitir): ")
                        cambios = {}
                        if nombre: cambios["nombre_animal"] = nombre
                        if especie: cambios["especie_animal"] = especie

                        animal = sistema.animal_crud.actualizar_animal(UUID(aid), usuario_id_creacion, **cambios)
                        print("Animal actualizado:", aid)

                    elif op == "5":
                        aid = input("ID animal a eliminar: ")
                        ok = sistema.animal_crud.eliminar_animal(UUID(aid))
                        print("Eliminado" if ok else "No encontrado")

                    elif op == "6":
                        break

                    else:
                        print("Opción inválida")

            elif opcion == "4":
                while True:
                    submenu_crud("Veterinarios")
                    op = input("Seleccione: ")

                    if op == "1":
                        print("\n--- Crear Veterinario ---")
                        primer_nombre = input("Primer nombre: ")
                        segundo_nombre = input("Segundo nombre (opcional): ")
                        primer_apellido = input("Primer apellido: ")
                        segundo_apellido = input("Segundo apellido (opcional): ")
                        telefono = input("Teléfono: ")
                        email = input("Email: ")
                        especialidad = input("Especialidad: ")

                        veterinario = sistema.veterinario_crud.crear_veterinario(
                            primer_nombre=primer_nombre,
                            segundo_nombre=segundo_nombre if segundo_nombre else None,
                            primer_apellido=primer_apellido,
                            segundo_apellido=segundo_apellido if segundo_apellido else None,
                            telefono=telefono,
                            email=email,
                            especialidad=especialidad,
                            usuario_id_creacion=usuario_id_creacion
                        )
                        print("Veterinario creado:", {primer_nombre}, {primer_apellido})

                    elif op == "2":
                        veterinarios = sistema.veterinario_crud.obtener_veterinarios()
                        for v in veterinarios:
                            print(v.id_veterinario, v.primer_nombre_veterinario, v.primer_apellido_veterinario, v.email)

                    elif op == "3":
                        vid = input("ID del veterinario: ")
                        veterinario = sistema.veterinario_crud.obtener_veterinario(UUID(vid))
                        if veterinario:
                            print("Veterinario encontrado:", veterinario)
                        else:
                            print("Veterinario no encontrado")

                    elif op == "4":
                        vid = input("ID del veterinario a actualizar: ")
                        telefono = input("Nuevo teléfono (enter para omitir): ")
                        email = input("Nuevo email (enter para omitir): ")
                        especialidad = input("Nueva especialidad (enter para omitir): ")
                        cambios = {}
                        if telefono: cambios["telefono"] = telefono
                        if email: cambios["email"] = email
                        if especialidad: cambios["especialidad"] = especialidad

                        veterinario = sistema.veterinario_crud.actualizar_veterinario(UUID(vid), usuario_id_creacion, **cambios)
                        print("Veterinario actualizado:", vid)

                    elif op == "5":
                        vid = input("ID del veterinario a eliminar: ")
                        ok = sistema.veterinario_crud.eliminar_veterinario(UUID(vid))
                        print("Eliminado" if ok else "No encontrado")

                    elif op == "6":
                        break

                    else:
                        print("Opción inválida")

            elif opcion == "5":
                while True:
                    submenu_crud("Citas")
                    op = input("Seleccione: ")

                    if op == "1":
                        print("\n--- Crear Cita ---")
                        fecha_input = input("Fecha (YYYY-MM-DD): ")
                        fecha_inicio_cita = datetime.strptime(fecha_input, "%Y-%m-%d")
                        motivo = input("Motivo de la cita: ")
                        animal_id = UUID(input("ID Animal: "))
                        vacuna_id = (input("ID Vacuna: "))
                        veterinario_id = UUID(input("ID Veterinario: "))

                        cita = sistema.cita_crud.crear_cita(
                            fecha_inicio_cita=fecha_inicio_cita,
                            motivo_cita=motivo,
                            animal_id=animal_id,
                            vacuna_id=UUID(vacuna_id),
                            veterinario_id=veterinario_id,
                            usuario_id_creacion=usuario_id_creacion
                        )
                        print("Cita creada:")

                    elif op == "2":
                        citas = sistema.cita_crud.obtener_citas()
                        for c in citas:
                            print(c.id_cita, c.fecha_inicio_cita, c.motivo_cita)

                    elif op == "3":
                        cid = input("ID de la cita: ")
                        cita = sistema.cita_crud.obtener_cita(UUID(cid))
                        if cita:
                            print("Cita encontrada:", cita.agendar_cita())
                        else:
                            print("Cita no encontrada")

                    elif op == "4":
                        cid = input("ID de la cita a actualizar: ")
                        fecha = input("Nueva fecha (YYYY-MM-DD, enter para omitir): ")
                        motivo = input("Nuevo motivo (enter para omitir): ")
                        cambios = {}
                        if fecha: cambios["fecha_inicio_cita"] = fecha
                        if motivo: cambios["motivo_cita"] = motivo

                        cita = sistema.cita_crud.actualizar_cita(UUID(cid), usuario_id_creacion, **cambios)
                        print("Cita actualizada:", cid)

                    elif op == "5":
                        cid = input("ID de la cita a eliminar: ")
                        ok = sistema.cita_crud.eliminar_cita(UUID(cid))
                        print("Eliminada" if ok else "No encontrada")

                    elif op == "6":
                        break
                    else:
                        print("Opción inválida")

            elif opcion == "6":
                while True:
                    submenu_crud("Vacunas")
                    op = input("Seleccione: ")

                    if op == "1":
                        print("\n--- Crear Vacuna ---")
                        nombre = input("Nombre vacuna: ")
                        fecha_aplicacion = input("Fecha de aplicación (YYYY-MM-DD): ")

                        proxima_dosis_input = input("Próxima dosis (YYYY-MM-DD) [opcional]: ")
                        proxima_dosis = None
                        if proxima_dosis_input.strip():
                            proxima_dosis = datetime.strptime(proxima_dosis_input, "%Y-%m-%d").date()

                        vacuna = sistema.vacuna_crud.crear_vacuna(
                            nombre_vacuna=nombre,
                            fecha_aplicacion_vacuna=datetime.strptime(fecha_aplicacion, "%Y-%m-%d").date(),
                            proxima_dosis_vacuna=proxima_dosis,
                            usuario_id_creacion=usuario_id_creacion
                        )
                        print("Vacuna creada:", vacuna.mostrar_info())

                    elif op == "2":
                        vacunas = sistema.vacuna_crud.obtener_vacunas()
                        for v in vacunas:
                            print(v.id_vacuna, v.nombre_vacuna, v.fecha_aplicacion_vacuna)

                    elif op == "3":
                        vid = input("ID de la vacuna: ")
                        vacuna = sistema.vacuna_crud.obtener_vacuna(UUID(vid))
                        if vacuna:
                            print("Vacuna encontrada:", vacuna.mostrar_info())
                        else:
                            print("Vacuna no encontrada")

                    elif op == "4":
                        vid = input("ID de la vacuna a actualizar: ")
                        nombre = input("Nuevo nombre (enter para omitir): ")
                        fecha_aplicacion = input("Nueva fecha de aplicación (enter para omitir): ")
                        cambios = {}
                        if nombre: cambios["nombre_vacuna"] = nombre
                        if fecha_aplicacion: cambios["fecha_aplicacion_vacuna"] = descripcion

                        vacuna = sistema.vacuna_crud.actualizar_vacuna(UUID(vid), usuario_id_creacion, **cambios)
                        print("Vacuna actualizada:", vid)

                    elif op == "5":
                        vid = input("ID de la vacuna a eliminar: ")
                        ok = sistema.vacuna_crud.eliminar_vacuna(UUID(vid))
                        print("Eliminada" if ok else "No encontrada")

                    elif op == "6":
                        break
                    else:
                        print("Opción inválida")    

            elif opcion == "7":
                while True:
                    submenu_crud("Facturas")
                    op = input("Seleccione: ")

                    if op == "1":
                        print("\n--- Crear Factura ---")
                        monto = float(input("Monto de la factura: "))
                        descripcion = input("Descripción de la factura: ")
                        cita_id = UUID(input("ID de la cita asociada: "))

                        factura = sistema.factura_crud.crear_factura(
                            monto_factura=monto,
                            descripcion_factura=descripcion,
                            cita_id=cita_id,
                            usuario_id_creacion=usuario_id_creacion
                        )
                        print("Factura creada:\n", factura)

                    elif op == "2":
                        facturas = sistema.factura_crud.obtener_facturas()
                        for f in facturas:
                            print(f.id_factura, f.monto_factura, f.fecha_emision, f.descripcion_factura)

                    elif op == "3":
                        fid = input("ID de la factura: ")
                        factura = sistema.factura_crud.obtener_factura(UUID(fid))
                        print(factura if factura else "No encontrada")

                    elif op == "4":
                        fid = input("ID de la factura a actualizar: ")
                        nuevo_monto = input("Nuevo monto (enter para omitir): ")
                        nueva_desc = input("Nueva descripción (enter para omitir): ")
                        cambios = {}
                        if nuevo_monto:
                            cambios["monto_factura"] = float(nuevo_monto)
                        if nueva_desc:
                            cambios["descripcion_factura"] = nueva_desc

                        factura = sistema.factura_crud.actualizar_factura(
                            UUID(fid), usuario_id_creacion, **cambios
                        )
                        print("Factura actualizada:", factura if factura else "No encontrada")

                    elif op == "5":
                        fid = input("ID de la factura a eliminar: ")
                        ok = sistema.factura_crud.eliminar_factura(UUID(fid))
                        print("Eliminada" if ok else "No encontrada")

                    elif op == "6":
                        break

                    else:
                        print("Opción inválida")                    

            elif opcion == "8":
                print("Saliendo del sistema...")
                break

            else:
                print("Opción inválida")       

if __name__ == "__main__":
    main()     