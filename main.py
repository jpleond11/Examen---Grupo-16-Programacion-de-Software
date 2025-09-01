from Clases.animal import Animal
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

def main() -> None:
    mascotas = {}
    citas = {}
    vacunas = {}
    facturas = {}

    while True:
        menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre =  input("Nombre: ")
            edad = input("Edad: ")
            propietario = input("Propietario: ")
            especie = input("Especie: ")
            mascotas[nombre,edad,propietario] = Animal(nombre,edad,propietario)
            print("Mascota registrada")

        elif opcion == "2":    
            nombre = input("Ingrese nombre de la mascota: ")
            propietario = input("Ingrese propietario de la mascota: ")
            fecha_cita = input("Ingrese fecha y hora de la cita: ")
            motivo = input("Ingrese motivo de la cita: ")   
            citas[nombre, propietario, fecha_cita, motivo] = Cita(nombre, edad, propietario, fecha_cita, motivo)
            print("Cita registrada con éxito")

        elif opcion == "3":
            nombre = input("Ingrese el nombre de la mascota: ")
            fecha_aplicacion = input("Fecha de la aplicación de la vacuna: ")
            proxima_dosis = input("Fecha para agendar una próxima dosis: ")
            vacunas[nombre, fecha_aplicacion, proxima_dosis] = Vacuna(nombre, fecha_aplicacion, proxima_dosis)
            print("Vacuna registrada con éxito")

        elif opcion == "4":
            monto = input("Ingresar monto a pagar: ")
            fecha_emision = input("Fecha de emisión de la factura: ")
            nombre = input("Nombre de la mascota: ")
            propietario = input("Propietario de la mascota: ")
            motivo = input("Motivo de la consulta: ")
            facturas[monto, fecha_emision, nombre, propietario, motivo] = Factura(monto, fecha_emision, nombre, propietario, motivo)
            print("Factura generada")

        elif opcion == "5":
            print("Saliendo...")
            break

        else:
            print("Opción no válida.")    

if __name__ == "__main__":
    main()