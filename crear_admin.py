import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.usuario import Usuario
from app.core.security import hash_password

def listar_o_crear_admin():
    db = SessionLocal()
    try:
        usuarios = db.query(Usuario).all()
        print("\n--- USUARIOS EN BASE DE DATOS ---")
        if not usuarios:
            print("No hay usuarios registrados actualmente.")
        else:
            for u in usuarios:
                print(f"ID: {u.id} | Email: {u.email} | Nombre: {u.nombre} | Rol: {u.rol}")
        print("---------------------------------\n")

        # Crear o actualizar un admin con credenciales claras y conocidas
        email_admin = "admin@ecommerce.com"
        pass_admin = "admin123"

        admin = db.query(Usuario).filter(Usuario.email == email_admin).first()
        if not admin:
            admin = Usuario(
                nombre="Administrador",
                email=email_admin,
                hashed_password=hash_password(pass_admin),
                rol="admin",
                acepto_tratamiento=True
            )
            db.add(admin)
            print(f"-> Creado usuario ADMIN por defecto:")
        else:
            admin.rol = "admin"
            admin.hashed_password = hash_password(pass_admin)
            print(f"-> Actualizado usuario ADMIN existente:")

        db.commit()
        print(f"   Email: {email_admin}")
        print(f"   Contraseña: {pass_admin}\n")
    finally:
        db.close()

if __name__ == "__main__":
    listar_o_crear_admin()
