from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.usuario import Usuario
from app.models.pedido import Pedido, SolicitudRevocacion
import json
from datetime import datetime, date
from decimal import Decimal

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError ("Type %s not serializable" % type(obj))

@router.get("/me/datos")
def get_mis_datos(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    pedidos = db.query(Pedido).filter(Pedido.usuario_id == current_user.id).all()
    solicitudes = db.query(SolicitudRevocacion).filter(SolicitudRevocacion.usuario_id == current_user.id).all()
    
    # Extraer items y datos útiles
    pedidos_data = []
    for p in pedidos:
        pedidos_data.append({
            "id": p.id,
            "estado": p.estado,
            "total": p.total,
            "creado_en": p.creado_en,
            "items": [{"producto_id": i.producto_id, "cantidad": i.cantidad, "precio_unitario": i.precio_unitario} for i in p.items]
        })
        
    solicitudes_data = [{"id": s.id, "codigo": s.codigo, "pedido_id": s.pedido_id, "creada_en": s.creada_en} for s in solicitudes]

    return {
        "usuario": {
            "id": current_user.id,
            "nombre": current_user.nombre,
            "email": current_user.email,
            "rol": current_user.rol,
            "acepto_tratamiento": current_user.acepto_tratamiento,
            "fecha_consentimiento": current_user.fecha_consentimiento,
            "activo": current_user.activo,
            "fecha_baja": current_user.fecha_baja
        },
        "pedidos": pedidos_data,
        "solicitudes_revocacion": solicitudes_data
    }

@router.get("/me/exportar")
def exportar_mis_datos(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    datos = get_mis_datos(db, current_user)
    
    json_data = json.dumps(datos, default=json_serial, indent=4)
    
    return Response(
        content=json_data,
        media_type="application/json",
        headers={
            "Content-Disposition": "attachment; filename=mis_datos.json"
        }
    )

@router.delete("/me")
def dar_de_baja(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    current_user.nombre = "Usuario Anónimo"
    current_user.email = f"anon-{current_user.id}@baja.local"
    current_user.hashed_password = "---"
    current_user.activo = False
    current_user.fecha_baja = datetime.utcnow()
    
    db.commit()
    
    return {"mensaje": "Cuenta dada de baja exitosamente"}
