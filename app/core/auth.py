from fastapi import Depends, HTTPException
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.usuario import Usuario

# Mock de autenticación básico para que funcione el checkout
def get_current_user(db: Session = Depends(get_db)):
    # Retorna el usuario con ID 1. Si no existe, lo crea.
    user = db.query(Usuario).filter(Usuario.id == 1).first()
    if not user:
        user = Usuario(id=1, nombre="Usuario Prueba", email="prueba@iresm.edu.ar")
        db.add(user)
        db.commit()
        db.refresh(user)
    return user
