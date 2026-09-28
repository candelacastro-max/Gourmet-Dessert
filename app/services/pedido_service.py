# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
# pyrefly: ignore [missing-import]
from fastapi import HTTPException
from app.models.pedido import Pedido, ItemPedido
from app.models.producto import Producto
from app.schemas.pedido import PedidoCreate
from app.models.usuario import Usuario

def crear_pedido(db: Session, usuario: Usuario, datos: PedidoCreate) -> Pedido:
    try:
        nuevo_pedido = Pedido(usuario_id=usuario.id, estado="pendiente", total=0.0)
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
