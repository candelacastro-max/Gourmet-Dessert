from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class ItemIn(BaseModel):
    producto_id: int
    cantidad: int = Field(gt=0, description="La cantidad debe ser mayor a cero")

class PedidoCreate(BaseModel):
    items: List[ItemIn] = Field(min_length=1, description="Debe incluir al menos un ítem")

class ItemOut(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_unitario: float
    
    model_config = {"from_attributes": True}

class PedidoOut(BaseModel):
    id: int
    estado: str
    total: float
    creado_en: datetime
    items: List[ItemOut]
    
    model_config = {"from_attributes": True}
