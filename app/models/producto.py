# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String, Numeric
from app.core.database import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    precio = Column(Numeric(12, 2), nullable=False)
    stock = Column(Integer, default=0)
    # Campos adicionales para el frontend
    precio_final = Column(Numeric(12, 2), nullable=True)  # precio con descuentos
    cuotas_cantidad = Column(Integer, default=1)
    cuotas_valor = Column(Numeric(12, 2), nullable=True)
    garantia_meses = Column(Integer, default=0)
    imagen_url = Column(String, nullable=True)
