from fastapi import APIRouter, Depends, Query, HTTPException, status
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal

from app.core.database import get_db
from app.models.producto import Producto
from app.dependencies import require_admin
from fastapi import UploadFile, File
import os
import secrets
from app.utils.archivos import parece_imagen

router = APIRouter(prefix="/productos", tags=["productos"], redirect_slashes=False)

@router.get("")
def listar_productos(
    page: int = Query(0, ge=0, description="Número de página (empieza en 0)"),
    limit: int = Query(10, ge=1, le=100, description="Cantidad de productos por página"),
    nombre: str = Query("", description="Filtrar por nombre"),
    db: Session = Depends(get_db)
):
    offset = page * limit
    query = db.query(Producto)
    if nombre:
        query = query.filter(Producto.nombre.ilike(f"%{nombre}%"))
    productos = query.offset(offset).limit(limit).all()
    
    # Devolvemos lista directa — el frontend hace setProductos(data) y luego data.map(...)
    return [
        {
            "id": p.id,
            "nombre": p.nombre,
            "precio": float(p.precio),
            "precio_final": float(p.precio_final) if p.precio_final is not None else float(p.precio),
            "stock": p.stock,
            "cuotas_cantidad": p.cuotas_cantidad or 1,
            "cuotas_valor": float(p.cuotas_valor) if p.cuotas_valor is not None else float(p.precio),
            "garantia_meses": p.garantia_meses or 0,
            "imagen_url": p.imagen_url,
        }
        for p in productos
    ]

@router.get("/{producto_id}")
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {
        "id": producto.id,
        "nombre": producto.nombre,
        "precio": float(producto.precio),
        "precio_final": float(producto.precio_final) if producto.precio_final is not None else float(producto.precio),
        "stock": producto.stock,
        "cuotas_cantidad": producto.cuotas_cantidad or 1,
        "cuotas_valor": float(producto.cuotas_valor) if producto.cuotas_valor is not None else float(producto.precio),
        "garantia_meses": producto.garantia_meses or 0,
        "imagen_url": producto.imagen_url,
    }


# ── POST /productos — solo admin ─────────────────────────────────────────────
@router.post("", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def crear_producto(body: dict, db: Session = Depends(get_db)):
    p = Producto(
        nombre=body["nombre"],
        precio=Decimal(str(body["precio"])),
        precio_final=Decimal(str(body.get("precio_final", body["precio"]))),
        stock=body.get("stock", 0),
        cuotas_cantidad=body.get("cuotas_cantidad", 1),
        cuotas_valor=Decimal(str(body.get("cuotas_valor", body["precio"]))),
        garantia_meses=body.get("garantia_meses", 0),
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return {"id": p.id, "nombre": p.nombre, "precio": float(p.precio), "stock": p.stock}


# ── PUT /productos/{id} — solo admin ─────────────────────────────────────────
@router.put("/{producto_id}", dependencies=[Depends(require_admin)])
def actualizar_producto(producto_id: int, body: dict, db: Session = Depends(get_db)):
    p = db.query(Producto).filter(Producto.id == producto_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for key, value in body.items():
        if hasattr(p, key):
            setattr(p, key, value)
    db.commit()
    db.refresh(p)
    return {"id": p.id, "nombre": p.nombre, "precio": float(p.precio), "stock": p.stock}


# ── DELETE /productos/{id} — solo admin ──────────────────────────────────────
@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(require_admin)])
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    p = db.query(Producto).filter(Producto.id == producto_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(p)
    db.commit()

# ── POST /productos/{id}/imagen — solo admin ─────────────────────────────────
@router.post("/{producto_id}/imagen", dependencies=[Depends(require_admin)])
async def subir_imagen_producto(producto_id: int, archivo: UploadFile = File(...), db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
        
    ext = os.path.splitext(archivo.filename)[1].lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        raise HTTPException(status_code=415, detail="Formato no permitido")
        
    contenido = await archivo.read()
    if len(contenido) > 5 * 1024 * 1024: # 5MB limit
        raise HTTPException(status_code=413, detail="Archivo demasiado grande")
        
    if not parece_imagen(contenido):
        raise HTTPException(status_code=415, detail="El archivo no parece ser una imagen válida")
        
    nombre_archivo = f"{producto_id}-{secrets.token_hex(8)}{ext}"
    ruta_guardado = os.path.join("uploads", "productos", nombre_archivo)
    
    with open(ruta_guardado, "wb") as f:
        f.write(contenido)
        
    producto.imagen_url = f"/static/productos/{nombre_archivo}"
    db.commit()
    db.refresh(producto)
    
    return {
        "id": producto.id,
        "nombre": producto.nombre,
        "precio": float(producto.precio),
        "imagen_url": producto.imagen_url
    }
