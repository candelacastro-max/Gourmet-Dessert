from fastapi import APIRouter, Depends, HTTPException, status
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.usuario import Usuario
from app.models.pedido import Pedido
from app.schemas.pedido import PedidoCreate, PedidoOut
from app.services.pedido_service import crear_pedido

router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@router.get("/mios", response_model=List[PedidoOut])
def get_mis_pedidos(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    pedidos = db.query(Pedido).filter(Pedido.usuario_id == current_user.id).order_by(Pedido.creado_en.desc()).all()
    return pedidos

@router.get("/{pedido_id}", response_model=PedidoOut)
def get_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
        
    # Asumimos que el usuario actual no es admin (o podríamos agregar lógica de rol)
    if pedido.usuario_id != current_user.id:
        # Se pide devolver 404 en el contrato si no es tuyo (o 403, pero el contrato sugiere 404 para ocultar info)
        # "404 = no existe o no es tuyo"
        raise HTTPException(status_code=404, detail="Pedido no encontrado o no es tuyo")
        
    return pedido

@router.post("/", response_model=PedidoOut, status_code=status.HTTP_201_CREATED)
def create_pedido_endpoint(
    datos: PedidoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return crear_pedido(db=db, usuario=current_user, datos=datos)
