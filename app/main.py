from pathlib import Path
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.core.config import settings
from app.routers.pedidos import router as pedidos_router
from app.routers.productos import router as productos_router
from app.routers.auth import router as auth_router
from app.routers.usuarios import router as usuarios_router

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

Path("uploads/productos").mkdir(parents=True, exist_ok=True)

limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

app = FastAPI(title="E-commerce IRESM", description="API para el e-commerce del Instituto Remedios Escalada de San Martín")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# CORS: permite los orígenes configurados
cors_origins_list = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(pedidos_router)
app.include_router(productos_router)
app.include_router(usuarios_router)

# Montamos las carpetas estáticas
app.mount("/tienda", StaticFiles(directory="static", html=True), name="tienda")
app.mount("/static", StaticFiles(directory="uploads"), name="static")
app.mount("/demo", StaticFiles(directory="app/static/demo"), name="demo")

@app.get("/salud", tags=["Salud"])
def salud(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"estado": "ok", "base": "ok"}

@app.get("/")
def read_root():
    return {
        "mensaje": "Bienvenido a la API del e-commerce estudiantil IRESM.",
        "legal": "Esta es la API de un e-commerce argentino sujeta a la Ley 24.240 de Defensa del Consumidor."
    }

