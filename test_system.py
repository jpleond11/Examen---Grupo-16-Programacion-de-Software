"""
Script de prueba para verificar que el sistema funciona correctamente con Neon
"""

from database.config import SessionLocal, create_tables
from Entidades.UsuarioORM import Usuario
from Entidades.CategoriaAnimalORM import CategoriaAnimal
from Entidades.PropietarioORM import Propietario
from Entidades.AnimalORM import Animal
from Entidades.VeterinarioORM import Veterinario
from Entidades.VacunaORM import Vacuna
from Entidades.CitaORM import Cita
from Entidades.FacturaORM import Factura
from datetime import datetime, date
from uuid import uuid4

def test_system():
    """Probar el sistema completo"""
    print("=== PRUEBA DEL SISTEMA COMPLETO ===\n")
    
    # Crear tablas si no existen
    print("1. Creando tablas...")
    create_tables()
    print("   ✓ Tablas creadas/verificadas")
    
    # Crear sesión de base de datos
    db = SessionLocal()
    
    try:
        # 1. Crear un usuario
        print("\n2. Creando usuario...")
        usuario = Usuario(
            primer_nombre_usuario="Admin",
            segundo_nombre_usuario="Sistema",
            primer_apellido_usuario="Principal",
            segundo_apellido_usuario="Test",
            rol_usuario="Administrador",
            fecha_nacimiento_usuario=date(1990, 1, 1),
            nombre_usuario="admin",
            password="admin123"
        )
        db.add(usuario)
        db.commit()
        print(f"   ✓ Usuario creado: {usuario.primer_nombre_usuario} {usuario.primer_apellido_usuario}")
        
        # 2. Crear categoría de animal
        print("\n3. Creando categoría de animal...")
        categoria = CategoriaAnimal(
            nombre_categoria="Mascotas Domésticas",
            descripcion="Animales domésticos comunes"
        )
        db.add(categoria)
        db.commit()
        print(f"   ✓ Categoría creada: {categoria.nombre_categoria}")
        
        # 3. Crear propietario
        print("\n4. Creando propietario...")
        propietario = Propietario(
            primer_nombre_propietario="Juan",
            segundo_nombre_propietario="Carlos",
            primer_apellido_propietario="Pérez",
            segundo_apellido_propietario="García",
            telefono="555-1234",
            direccion="Calle Principal 123",
            usuario_id_creacion=usuario.id_usuario
        )
        db.add(propietario)
        db.commit()
        print(f"   ✓ Propietario creado: {propietario.primer_nombre_propietario} {propietario.primer_apellido_propietario}")
        
        # 4. Crear animal
        print("\n5. Creando animal...")
        animal = Animal(
            nombre_animal="Max",
            especie_animal="Perro",
            fecha_nacimiento_animal=date(2020, 5, 15),
            propietario_id=propietario.id_propietario,
            categoria_id=categoria.id_categoria_animal,
            usuario_id_creacion=usuario.id_usuario
        )
        db.add(animal)
        db.commit()
        print(f"   ✓ Animal creado: {animal.nombre_animal} ({animal.especie_animal})")
        
        # 5. Crear veterinario
        print("\n6. Creando veterinario...")
        veterinario = Veterinario(
            primer_nombre_veterinario="Dr. María",
            segundo_nombre_veterinario="Elena",
            primer_apellido_veterinario="Rodríguez",
            segundo_apellido_veterinario="López",
            telefono="555-5678",
            email="maria.rodriguez@clinica.com",
            especialidad="Medicina General",
            usuario_id_creacion=usuario.id_usuario
        )
        db.add(veterinario)
        db.commit()
        print(f"   ✓ Veterinario creado: {veterinario.primer_nombre_veterinario} {veterinario.primer_apellido_veterinario}")
        
        # 6. Crear vacuna
        print("\n7. Creando vacuna...")
        vacuna = Vacuna(
            nombre_vacuna="Vacuna Antirrábica",
            fecha_aplicacion_vacuna=date(2024, 1, 15),
            proxima_dosis_vacuna=date(2025, 1, 15),
            usuario_id_creacion=usuario.id_usuario
        )
        db.add(vacuna)
        db.commit()
        print(f"   ✓ Vacuna creada: {vacuna.nombre_vacuna}")
        
        # 7. Crear cita
        print("\n8. Creando cita...")
        cita = Cita(
            fecha_inicio_cita=datetime(2024, 12, 20, 10, 0),
            fecha_final_cita=datetime(2024, 12, 20, 11, 0),
            motivo_cita="Consulta de rutina y vacunación",
            animal_id=animal.id_animal,
            vacuna_id=vacuna.id_vacuna,
            veterinario_id=veterinario.id_veterinario,
            usuario_id_creacion=usuario.id_usuario
        )
        db.add(cita)
        db.commit()
        print(f"   ✓ Cita creada: {cita.motivo_cita}")
        
        # 8. Crear factura
        print("\n9. Creando factura...")
        factura = Factura(
            monto_factura=150.00,
            fecha_emision=datetime.now(),
            descripcion_factura="Consulta veterinaria y vacunación",
            cita_id=cita.id_cita,
            usuario_id_creacion=usuario.id_usuario
        )
        db.add(factura)
        db.commit()
        print(f"   ✓ Factura creada: ${factura.monto_factura}")
        
        # 9. Verificar datos
        print("\n10. Verificando datos en la base de datos...")
        
        # Contar registros
        usuarios_count = db.query(Usuario).count()
        propietarios_count = db.query(Propietario).count()
        animales_count = db.query(Animal).count()
        veterinarios_count = db.query(Veterinario).count()
        vacunas_count = db.query(Vacuna).count()
        citas_count = db.query(Cita).count()
        facturas_count = db.query(Factura).count()
        categorias_count = db.query(CategoriaAnimal).count()
        
        print(f"   ✓ Usuarios: {usuarios_count}")
        print(f"   ✓ Propietarios: {propietarios_count}")
        print(f"   ✓ Animales: {animales_count}")
        print(f"   ✓ Veterinarios: {veterinarios_count}")
        print(f"   ✓ Vacunas: {vacunas_count}")
        print(f"   ✓ Citas: {citas_count}")
        print(f"   ✓ Facturas: {facturas_count}")
        print(f"   ✓ Categorías: {categorias_count}")
        
        print("\n" + "="*50)
        print("🎉 ¡SISTEMA FUNCIONANDO CORRECTAMENTE!")
        print("✅ Conexión a Neon establecida")
        print("✅ Tablas creadas correctamente")
        print("✅ Datos insertados exitosamente")
        print("✅ Relaciones funcionando")
        print("="*50)
        
    except Exception as e:
        print(f"\n❌ Error durante la prueba: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    test_system()
