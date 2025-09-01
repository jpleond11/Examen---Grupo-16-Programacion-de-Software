# Se crea la clase propietario del animal
class Propietario:
    def __init__(self, nombre: str, telefono: str, direccion: str) -> None:
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion

    def mostrar_info(self) -> str:
        return f"Nombre: {self.nombre}, Telefono: {self.telefono}, Dirección: {self.direccion}"