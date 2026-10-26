from app.models.pedido import SolicitudRevocacion
from fastapi import APIRouter, Depends, HTTPException, status
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.dependencies import get_current_user, require_admin
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

@router.get("/admin/notificaciones-cancelaciones")
def get_notificaciones_cancelaciones(
    db: Session = Depends(get_db),
    admin: Usuario = Depends(require_admin)
):
    solicitudes = db.query(SolicitudRevocacion).order_by(SolicitudRevocacion.creada_en.desc()).all()
    resultado = []
    for s in solicitudes:
        items_data = []
        if s.pedido and s.pedido.items:
            for it in s.pedido.items:
                items_data.append({
                    "producto_id": it.producto_id,
                    "nombre": it.producto.nombre if it.producto else f"Producto #{it.producto_id}",
                    "cantidad": it.cantidad,
                    "precio_unitario": float(it.precio_unitario) if it.precio_unitario else 0.0
                })
        resultado.append({
            "id": s.id,
            "codigo": s.codigo,
            "pedido_id": s.pedido_id,
            "total_pedido": float(s.pedido.total) if s.pedido and s.pedido.total else 0.0,
            "cliente_nombre": s.usuario.nombre if s.usuario else "Usuario Desconocido",
            "cliente_email": s.usuario.email if s.usuario else "Sin email",
            "motivo": s.motivo or "Sin motivo especificado",
            "creada_en": s.creada_en.isoformat() if s.creada_en else None,
            "items": items_data
        })
    return resultado

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

from app.services.pedido_service import revocar
from app.dependencies import require_admin
from pydantic import BaseModel
from typing import Optional

class RevocacionRequest(BaseModel):
    motivo: Optional[str] = None

@router.post("/{pedido_id}/revocacion", status_code=status.HTTP_201_CREATED)
def revocar_pedido_endpoint(
    pedido_id: int,
    req: Optional[RevocacionRequest] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    motivo = req.motivo if req else None
    solicitud = revocar(db, current_user, pedido_id, motivo=motivo)
    return {
        "codigo": solicitud.codigo,
        "pedido_id": solicitud.pedido_id,
        "motivo": solicitud.motivo,
        "creada_en": solicitud.creada_en
    }

class ArrepentimientoRequest(BaseModel):
    pedido_id: int
    email: str
    motivo: Optional[str] = None

@router.post("/arrepentimiento", status_code=status.HTTP_201_CREATED)
def arrepentimiento_publico(req: ArrepentimientoRequest, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == req.pedido_id).first()
    if not pedido or pedido.usuario.email != req.email:
        raise HTTPException(status_code=404, detail="Pedido no encontrado o email incorrecto")
        
    solicitud = revocar(db, pedido.usuario, req.pedido_id, motivo=req.motivo)
    return {
        "codigo": solicitud.codigo,
        "pedido_id": solicitud.pedido_id,
        "motivo": solicitud.motivo,
        "creada_en": solicitud.creada_en
    }
