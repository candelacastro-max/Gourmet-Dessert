# pyrefly: ignore [missing-import]
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers.pedidos import router as pedidos_router
from app.routers.productos import router as productos_router
from app.routers.auth import router as auth_router

app = FastAPI(title="E-commerce IRESM", description="API para el e-commerce del Instituto Remedios Escalada de San Martín")

# CORS: permite que el frontend (Vite en :5173) consuma la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(pedidos_router)
app.include_router(productos_router)

# Montamos la carpeta estática para servir el frontend
app.mount("/tienda", StaticFiles(directory="static", html=True), name="tienda")

@app.get("/")
def read_root():
    return {
        "mensaje": "Bienvenido a la API del e-commerce estudiantil IRESM.",
        "legal": "Esta es la API de un e-commerce argentino sujeta a la Ley 24.240 de Defensa del Consumidor."
    }
