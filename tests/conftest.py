import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.core.database import Base, get_db
from app.models.usuario import Usuario
from app.models.producto import Producto
from app.models.pedido import Pedido, ItemPedido, SolicitudRevocacion
from tests.ayudantes import registrar, token_de

# Una base en memoria, nueva para cada test. StaticPool hace que todas
# las sesiones usen la misma conexión: si no, cada una vería una base vacía.
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SesionPrueba = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db_prueba():
    with SesionPrueba() as db:
        yield db

@pytest.fixture
def client():
    Base.metadata.create_all(engine)
    app.dependency_overrides[get_db] = get_db_prueba
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)

@pytest.fixture
def cliente(client):
    """Headers de un cliente común, ya logueado."""
    return token_de(client, *registrar(client))

@pytest.fixture
def admin(client):
    """Headers de un admin. No hay endpoint para dar el rol: se toca la base."""
    email, password = registrar(client, email="admin@prueba.com")
    with SesionPrueba() as db:
        usuario = db.query(Usuario).filter_by(email=email).one()
        usuario.rol = "admin"
        db.commit()
    return token_de(client, email, password)

@pytest.fixture
def producto(client, admin):
    """Un producto con 2 unidades. Ajustá los campos a tu Producto."""
    r = client.post(
        "/productos",
        headers=admin,
        json={
            "nombre": "Mate de prueba",
            "precio": 1000,
            "stock": 2,
        },
    )
    assert r.status_code == 201, r.text
    return r.json()
