# Se crea la clase vacuna
class Vacuna:
    def __init__(self, nombre, fecha_aplicacion, proxima_dosis) -> None:
        self.nombre = nombre
        self.fecha_aplicacion = fecha_aplicacion
        self.proxima_dosis = proxima_dosis

    def mostrar_info(self):
        return f"Vacuna: {self.nombre}, Fecha de aplicación: {self.fecha_aplicacion}, Proxima dosis: {self.proxima_dosis}"