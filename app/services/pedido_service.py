# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
# pyrefly: ignore [missing-import]
from fastapi import HTTPException
from app.models.pedido import Pedido, ItemPedido, SolicitudRevocacion
from app.models.producto import Producto
from app.schemas.pedido import PedidoCreate
from app.models.usuario import Usuario
from datetime import datetime, timezone
import secrets

def crear_pedido(db: Session, usuario: Usuario, datos: PedidoCreate) -> Pedido:
    try:
        nuevo_pedido = Pedido(usuario_id=usuario.id, estado="comprado", total=0.0)
        db.add(nuevo_pedido)
        db.flush() # Para obtener el ID del pedido sin hacer commit
        
        total = 0.0
        
        for item in datos.items:
            producto = db.query(Producto).filter(Producto.id == item.producto_id).first()
            if not producto:
                raise HTTPException(status_code=404, detail=f"Producto {item.producto_id} no encontrado")
            
            if producto.stock < item.cantidad:
                raise HTTPException(
                    status_code=409, 
                    detail=f"Sin stock suficiente de {producto.nombre}. Quedan {producto.stock} unidades."
                )
            
            # Descontar stock
            producto.stock -= item.cantidad
            
            # Crear ítem con el precio actual
            nuevo_item = ItemPedido(
                pedido_id=nuevo_pedido.id,
                producto_id=producto.id,
                cantidad=item.cantidad,
                precio_unitario=producto.precio
            )
            db.add(nuevo_item)
            
            total += float(producto.precio) * item.cantidad
            
        nuevo_pedido.total = total
        db.commit()
        db.refresh(nuevo_pedido)
        return nuevo_pedido
        
    except Exception as e:
        db.rollback()
        raise e

def generar_codigo() -> str:
    fecha = datetime.now(timezone.utc).strftime("%Y%m%d")
    return f"ARR-{fecha}-{secrets.token_hex(3).upper()}"

def revocar(db: Session, usuario: Usuario, pedido_id: int):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    
    if not pedido or pedido.usuario_id != usuario.id:
        raise HTTPException(status_code=404, detail="Pedido no encontrado o no es tuyo")
        
    if pedido.estado == "cancelado":
        raise HTTPException(status_code=409, detail="El pedido ya está cancelado")
        
    if pedido.creado_en:
        # Check if created_en is naive or aware
        if pedido.creado_en.tzinfo is None:
            creado_en_aware = pedido.creado_en.replace(tzinfo=timezone.utc)
        else:
            creado_en_aware = pedido.creado_en
            
        dias_pasados = (datetime.now(timezone.utc) - creado_en_aware).days
        if dias_pasados > 10:
            raise HTTPException(status_code=409, detail="El plazo de 10 días para revocar ha expirado")
            
    try:
        # Devolver stock
        for item in pedido.items:
            producto = db.query(Producto).filter(Producto.id == item.producto_id).first()
            if producto:
                producto.stock += item.cantidad
                
        # Cambiar estado
        pedido.estado = "cancelado"
        
        # Crear solicitud
        codigo = generar_codigo()
        solicitud = SolicitudRevocacion(
            codigo=codigo,
            pedido_id=pedido.id,
            usuario_id=usuario.id
        )
        db.add(solicitud)
        
        db.commit()
        db.refresh(solicitud)
        return solicitud
        
    except Exception as e:
        db.rollback()
        raise e
