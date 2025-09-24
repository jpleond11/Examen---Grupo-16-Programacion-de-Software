from datetime import datetime
from Clases.animal import Perro, Gato, Ave
from Clases.cita import Cita
from Clases.factura import Factura
from Clases.propietario import Propietario
from Clases.vacuna import Vacuna

def menu():
    print("\n--- CLINICA VETERINARIA ---")
    print("1. Registrar una mascota")
    print("2. Agendar una cita")
    print("3. Aplicar una vacuna")
    print("4. Generar una factura")
    print("5. Salir")

#Generación de listas para almacenar registros:
def main() -> None:
    mascotas = []
    citas = []
    facturas = []

    while True:
        menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("\n--- Registrar Mascota ---")
            especie = input("Especie (perro/gato/ave): ").lower()
            nombre = input("Nombre de la mascota: ")
            edad = int(input("Edad: "))
            print ("\n--- Datos del propietario ---")
            nombre_propt = input("Nombre del propietario: ")
            telefono = input("Teléfono: ")
            direccion = input("Dirección: ")
            propietario = Propietario(nombre_propt, telefono, direccion)
            if especie == "perro":
                raza = input("Raza: ")
                animal = Perro(nombre, edad, propietario, raza)
            elif especie == "gato":
                color = input("Color: ")
                animal = Gato(nombre, edad, propietario, color)
            elif especie == "ave":
                tipo = input("Tipo de ave: ")
                animal = Ave(nombre, edad, propietario, tipo)
            else:
                print("Especie no reconocida.")
                return
            mascotas.append(animal)
            print("Mascota registrada exitosamente: ")
            print(animal.mostrar_info())

            def seleccionar_mascota():
                print("\n--- Mascotas registradas ---")
                for i, animal in enumerate(mascotas):
                    print(f"{i+1}. {animal.nombre} ({animal.especie}) - Propietario: {animal.propietario.nombre}")

                try:
                    index = int(input("Selecciona el número de la mascota: ")) - 1
                    return mascotas[index]
                except (IndexError, ValueError):
                    print("Selección inválida.")
                    return None    


        elif opcion == "2":
            print("\n--- Agendar Cita ---")
            animal = seleccionar_mascota()
            fecha_cita = input("Fecha y hora de la cita (formato: DD/MM/YYYY HH:MM): ")
            try:
                fecha = datetime.strptime(fecha_cita, "%d/%m/%Y %H:%M")
            except ValueError:
                print("Formato de fecha incorrecto.")
                return

            motivo = input("Motivo de la cita: ")
            cita = Cita(animal, fecha, motivo)
            citas.append(cita)
            print("Cita agendada exitosamente.")
            print(cita.agendar_cita())    


        elif opcion == "3":
            print("\n--- Aplicar Vacuna ---")
            animal = seleccionar_mascota()
            nombre_vacuna = input("Nombre de la vacuna: ")
            fecha_aplicacion = input("Fecha de la aplicación: ")
            proxima_dosis = input("Fecha de la próxima dosis: ")
            vacuna = Vacuna(nombre_vacuna, fecha_aplicacion, proxima_dosis)
            print("Vacuna aplicada exitosamente")
            print(vacuna.mostrar_info())

        elif opcion == "4":
            print("\n--- Generar Factura ---")
            print("\n--- Citas disponibles ---")
            for i, cita in enumerate(citas):
                print(f"{i+1}. {cita.animal.nombre} - {cita.fecha.strftime('%d/%m/%Y %H:%M')} - Motivo: {cita.motivo}")
            index = int(input("Selecciona el número de la cita: ")) - 1
            cita_seleccionada = citas[index]
            monto = float(input("Monto de la factura: "))
            fecha_emision = datetime.now()
            factura = Factura(cita_seleccionada, monto, fecha_emision)
            facturas.append(factura)
            print("\n--- FACTURA GENERADA ---")
            print(factura)

        elif opcion == "5":
            print("Saliendo...")
            break

        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()