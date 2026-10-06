# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.core.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    rol = Column(String, default="customer")           # "customer" | "admin"
    acepto_tratamiento = Column(Boolean, default=False)
    fecha_consentimiento = Column(DateTime, nullable=True)
    activo = Column(Boolean, default=True)
    fecha_baja = Column(DateTime, nullable=True)
