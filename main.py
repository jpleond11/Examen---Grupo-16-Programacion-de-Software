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

