import os
import sys

# Permitir ejecutar con python -m app.seed o python app/seed.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.usuario import Usuario
from app.models.producto import Producto
from app.core.security import hash_password

def seed_database():
    db = SessionLocal()
    try:
        # 1. Crear el admin si no existe
        admin_email = os.getenv("SEED_ADMIN_EMAIL", "admin@equipo.com")
        admin_password = os.getenv("SEED_ADMIN_PASSWORD", "admin123456")

        admin_existente = db.query(Usuario).filter(Usuario.email == admin_email).first()
        if not admin_existente:
            nuevo_admin = Usuario(
                nombre="Administrador",
                email=admin_email,
                hashed_password=hash_password(admin_password),
                rol="admin",
                acepto_tratamiento=True
            )
            db.add(nuevo_admin)
            print(f"Admin creado: {admin_email}")
        else:
            print(f"Admin ya existe: {admin_email}")

        # 2. Crear los productos si no existen (con imagen_url apuntando a /demo/<archivo>)
        productos_demo = [
            {
                "nombre": "Burger Dulce (Banana y avena)",
                "precio": 9500.0,
                "precio_final": 9500.0,
                "stock": 25,
                "cuotas_cantidad": 3,
                "cuotas_valor": 3166.67,
                "garantia_meses": 0,
                "imagen_url": "/demo/dessert_burger_1786462447266.png"
            },
            {
                "nombre": "Pancho Mágico (Postre de frutas)",
                "precio": 8200.0,
                "precio_final": 8200.0,
                "stock": 20,
                "cuotas_cantidad": 3,
                "cuotas_valor": 2733.33,
                "garantia_meses": 0,
                "imagen_url": "/demo/dessert_hotdog_1786462456214.png"
            },
            {
                "nombre": "Pizza Pastel (Frutilla y crema)",
                "precio": 12000.0,
                "precio_final": 12000.0,
                "stock": 15,
                "cuotas_cantidad": 3,
                "cuotas_valor": 4000.0,
                "garantia_meses": 0,
                "imagen_url": "/demo/dessert_pizza_1786462490716.png"
            },
            {
                "nombre": "Alfajor Artesanal Gourmet",
                "precio": 3500.0,
                "precio_final": 3500.0,
                "stock": 50,
                "cuotas_cantidad": 1,
                "cuotas_valor": 3500.0,
                "garantia_meses": 0,
                "imagen_url": None
            }
        ]

        for p_data in productos_demo:
            existente = db.query(Producto).filter(Producto.nombre == p_data["nombre"]).first()
            if not existente:
                producto = Producto(**p_data)
                db.add(producto)
                print(f"Producto creado: {p_data['nombre']}")
            else:
                print(f"Producto ya existe: {p_data['nombre']}")

        db.commit()
        print("Seed listo.")
    except Exception as e:
        db.rollback()
        print("Error durante el seed:", e)
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
