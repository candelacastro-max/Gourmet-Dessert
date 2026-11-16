from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import Base, engine, SessionLocal, get_db
from app.core.config import settings
from app.models.usuario import Usuario
from app.models.producto import Producto
from app.models.pedido import Pedido, ItemPedido, SolicitudRevocacion
from app.core.security import hash_password

from app.routers.pedidos import router as pedidos_router
from app.routers.productos import router as productos_router
from app.routers.auth import router as auth_router
from app.routers.usuarios import router as usuarios_router

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from fastapi.middleware.gzip import GZipMiddleware

Path("uploads/productos").mkdir(parents=True, exist_ok=True)

class StaticConCache(StaticFiles):
    async def get_response(self, path, scope):
        respuesta = await super().get_response(path, scope)
        if respuesta.status_code == 200:
            respuesta.headers["Cache-Control"] = "public, max-age=2592000, immutable"
        return respuesta

limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Crear automáticamente todas las tablas si no existen
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print("Aviso al crear tablas:", e)

    # 2. Inicializar usuario admin y productos si no existen
    db = SessionLocal()
    try:
        # Admin por defecto
        admin = db.query(Usuario).filter(Usuario.email == "admin@ecommerce.com").first()
        if not admin:
            admin = Usuario(
                nombre="Administrador",
                email="admin@ecommerce.com",
                hashed_password=hash_password("admin123"),
                rol="admin",
                acepto_tratamiento=True
            )
            db.add(admin)
            db.commit()
            print("Usuario admin creado: admin@ecommerce.com / admin123")
        else:
            admin.rol = "admin"
            admin.hashed_password = hash_password("admin123")
            db.commit()

        # Productos iniciales
        if db.query(Producto).count() == 0:
            productos_iniciales = [
                Producto(
                    id=1,
                    nombre="Hamburguesa (Está hecho de banana y avena)",
                    precio=9500.00,
                    precio_final=9500.00,
                    stock=25,
                    cuotas_cantidad=3,
                    cuotas_valor=3166.67,
                    garantia_meses=0
                ),
                Producto(
                    id=2,
                    nombre="Esponja (Es un bizcochuelo)",
                    precio=12500.00,
                    precio_final=12500.00,
                    stock=20,
                    cuotas_cantidad=3,
                    cuotas_valor=4166.67,
                    garantia_meses=0
                ),
                Producto(
                    id=3,
                    nombre="Huevo (De gelatina)",
                    precio=6000.00,
                    precio_final=6000.00,
                    stock=35,
                    cuotas_cantidad=3,
                    cuotas_valor=2000.00,
                    garantia_meses=0
                ),
                Producto(
                    id=4,
                    nombre="Vela (Chocolate blanco y negro)",
                    precio=9000.00,
                    precio_final=9000.00,
                    stock=30,
                    cuotas_cantidad=3,
                    cuotas_valor=3000.00,
                    garantia_meses=0
                ),
                Producto(
                    id=5,
                    nombre="Tomate (Algo parecido al alfajor maicena)",
                    precio=11000.00,
                    precio_final=11000.00,
                    stock=40,
                    cuotas_cantidad=3,
                    cuotas_valor=3666.67,
                    garantia_meses=0
                ),
            ]
            for p in productos_iniciales:
                db.add(p)
            db.commit()
            print("Productos iniciales cargados en la base de datos.")
    except Exception as e:
        print("Aviso al inicializar datos:", e)
    finally:
        db.close()

    yield

app = FastAPI(
    title="E-commerce IRESM",
    description="API para el e-commerce del Instituto Remedios Escalada de San Martín",
    lifespan=lifespan
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# CORS: orígenes configurados y regex para permitir cualquier subdominio de Vercel
cors_origins_list = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins_list,
    allow_origin_regex=r"^https://.*\.vercel\.app$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(pedidos_router)
app.include_router(productos_router)
app.include_router(usuarios_router)

from app.routers.pedidos import arrepentimiento_publico, ArrepentimientoRequest

@app.post("/arrepentimiento", status_code=201, tags=["arrepentimiento"])
def arrepentimiento_raiz(req: ArrepentimientoRequest, db: Session = Depends(get_db)):
    return arrepentimiento_publico(req, db)

# Montamos las carpetas estáticas
app.mount("/tienda", StaticFiles(directory="static", html=True), name="tienda")
app.mount("/static", StaticConCache(directory="uploads"), name="static")
app.mount("/demo", StaticConCache(directory="app/static/demo"), name="demo")

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
