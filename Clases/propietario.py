# Se crea la clase propietario del animal
class Propietario:
    def __init__(self, nombre, telefono, direccion):
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion

    def mostrar_info(self):
        return f"Nombre: {self.nombre}, TelÃ©fono: {self.telefono}, Dirección: {self.direccion}"