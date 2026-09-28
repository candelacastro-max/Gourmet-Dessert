import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.producto import Producto

db = SessionLocal()

def crear_productos():
    # Borramos pedidos previos asociados a productos si los hubiera para evitar violaciones de clave foránea
    from app.models.usuario import Usuario
    from app.models.pedido import ItemPedido, Pedido
    db.query(ItemPedido).delete()
    db.query(Pedido).delete()
    db.query(Producto).delete()
    db.commit()

    productos = [
        Producto(
            id=1,
            nombre="Hamburguesa (Está hecho de banana y avena)",
            precio=9500.00,
            precio_final=9500.00,
            stock=25,
            cuotas_cantidad=3,
            cuotas_valor=3166.67,
            garantia_meses=0
        ),
        Producto(
            id=2,
            nombre="Esponja (Es un bizcochuelo)",
            precio=12500.00,
            precio_final=12500.00,
            stock=20,
            cuotas_cantidad=3,
            cuotas_valor=4166.67,
            garantia_meses=0
        ),
        Producto(
            id=3,
            nombre="Huevo (De gelatina)",
            precio=6000.00,
            precio_final=6000.00,
            stock=35,
            cuotas_cantidad=3,
            cuotas_valor=2000.00,
            garantia_meses=0
        ),
        Producto(
            id=4,
            nombre="Vela (Chocolate blanco y negro)",
            precio=9000.00,
            precio_final=9000.00,
            stock=30,
            cuotas_cantidad=3,
            cuotas_valor=3000.00,
            garantia_meses=0
        ),
        Producto(
            id=5,
            nombre="Tomate (Algo parecido al alfajor maicena)",
            precio=11000.00,
            precio_final=11000.00,
            stock=40,
            cuotas_cantidad=3,
            cuotas_valor=3666.67,
            garantia_meses=0
        ),
    ]

    for p in productos:
        db.add(p)

    db.commit()
    print("Productos actualizados con éxito.")

if __name__ == "__main__":
    crear_productos()

