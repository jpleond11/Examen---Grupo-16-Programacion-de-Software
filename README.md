# Examen-1---Grupo-16-Programacion-de-Software
# Clínica Veterinaria - Sistema de Gestión

Este proyecto es un programa de consola en **Python** que permite gestionar una clínica veterinaria de forma sencilla.  
Los usuarios pueden registrar mascotas, agendar citas, aplicar vacunas y generar facturas de manera interactiva.

---

## 🚀 Funcionalidades principales

1. **Registrar una mascota**  
   - Perro, gato o ave.  
   - Datos básicos (nombre, edad, raza/color/tipo según especie).  
   - Información del propietario (nombre, teléfono, dirección).  

2. **Agendar una cita**  
   - Selección de una mascota registrada.  
   - Fecha, hora y motivo de la cita.  

3. **Aplicar una vacuna**  
   - Registro de nombre de la vacuna, fecha de aplicación y próxima dosis.  

4. **Generar una factura**  
   - Selección de una cita ya creada.  
   - Registro de monto y fecha de emisión.  

---

## 📂 Estructura del proyecto
📦 ClinicaVeterinaria
┣ 📂 Clases
┃ ┣ animal.py
┃ ┣ cita.py
┃ ┣ factura.py
┃ ┣ propietario.py
┃ ┗ vacuna.py
┣ main.py
┗ README.md

---

## 🛠️ Requisitos

- Python 3.8 o superior  
- No requiere librerías externas (solo `datetime`, que ya viene con Python).

---

## ▶️ Cómo ejecutar el programa

1. Clona este repositorio o descarga el código:
   ```bash
   git clone https://github.com/usuario/clinica-veterinaria.git
   cd clinica-veterinaria
2. Ejecuta el archivo principal:
    python main.py
3. El menú aparecerá en pantalla:
    --- CLINICA VETERINARIA ---
    1. Registrar una mascota
    2. Agendar una cita
    3. Aplicar una vacuna
    4. Generar una factura
    5. Salir

📝 Ejemplo de uso:
**Registrar una mascota**
--- Registrar Mascota ---
Especie (perro/gato/ave): perro
Nombre de la mascota: Max
Edad: 3

--- Datos del propietario ---
Nombre del propietario: Laura
Teléfono: 3001234567
Dirección: Calle 123
Raza: Labrador

Mascota registrada exitosamente:
Nombre: Max | Especie: Perro | Edad: 3 | Propietario: Laura   

**Agendar una cita**
--- Agendar Cita ---
Selecciona el número de la mascota: 1
Fecha y hora de la cita (formato: DD/MM/YYYY HH:MM): 02/09/2025 15:00
Motivo de la cita: Vacunación
Cita agendada exitosamente.

Autor
Proyecto desarrollado como ejemplo de sistema de gestión para una clínica veterinaria en Python.
Desarrollado por Juan Pablo León Duque y Andrés David Villa Marín