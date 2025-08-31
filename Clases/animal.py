# Se crea la clase Animal y sus subclases Gato, Perro y Ave
class Animal:
    def __init__(self, nombre:str, edad:int, propietario:str) -> str:
        self.nombre = nombre
        self.edad = edad
        self.propietario = propietario
        self.especie = "Desconocida"

    def mostrar_info(self) -> str:
        return f"Nombre: {self.nombre}, Edad: {self.edad}, Especie: {self.especie}, Propietario: {self.propietario}"


# Subclase Perro
class Perro(Animal):
    def __init__(self, nombre:str, edad:int, propietario:str, raza:str) -> str:
        super().__init__(nombre, edad, propietario)
        self.raza = raza
        self.especie = "Perro"

    def mostrar_info(self):
        return super().mostrar_info() + f", Raza: {self.raza}"


# Subclase Gato
class Gato(Animal):
    def __init__(self, nombre:str, edad:int, propietario:str, color:str) -> str:
        super().__init__(nombre, edad, propietario)
        self.color = color
        self.especie = "Gato"

    def mostrar_info(self) -> str:
        return super().mostrar_info() + f", Color: {self.color}"


# Subclase Ave
class Ave(Animal):
    def __init__(self, nombre:str, edad:int, propietario:str, tipo:str) -> str:
        super().__init__(nombre, edad, propietario)
        self.tipo = tipo  # Ejemplo: "Loro", "Canario"
        self.especie = "Ave"

    def mostrar_info(self) -> str:
        return super().mostrar_info() + f", Tipo de ave: {self.tipo}"
