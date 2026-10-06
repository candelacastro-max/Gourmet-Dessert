# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field


app = FastAPI(
    title="API de Catálogo - Trampaantojo",
    version="1.0.0"
)

class Producto(BaseModel):
    id: int
    nombre: str
    precio_final: float = Field(gt=0, description="El precio final debe ser mayor a 0")
    cuotas_cantidad: int = Field(ge=1, description="Mínimo 1 cuota")
    cuotas_valor: float = Field(gt=0, description="Valor de cada cuota")
    garantia_meses: int = Field(ge=0, description="Meses de garantía (0 si no aplica)")
    stock: int = Field(ge=0, description="Stock disponible")

productos_db: list[Producto] = [
    Producto(
        id=1,
        nombre="Esponja (Bizcochuelo)",
        precio_final=11500.0,
        cuotas_cantidad=3,
        cuotas_valor=3833.33,
        garantia_meses=0,
        stock=50
    ),
    Producto(
        id=2,
        nombre="Vela (Chocolate Blanco)",
        precio_final=9000.0,
        cuotas_cantidad=3,
        cuotas_valor=3000.0,
        garantia_meses=0,
        stock=20
    ),
    Producto(
        id=3,
        nombre="Huevo Frito (Postre de Gelatina)",
        precio_final=6000.0,
        cuotas_cantidad=3,
        cuotas_valor=2000.0,
        garantia_meses=0,
        stock=15
    ),
    Producto(
        id=4,
        nombre="Hamburguesa (Postre de Banana)",
        precio_final=9500.0,
        cuotas_cantidad=3,
        cuotas_valor=3166.66,
        garantia_meses=0,
        stock=8
    ),
    Producto(
        id=5,
        nombre="Tomate (Alfajor Rojo)",
        precio_final=11000.0,
        cuotas_cantidad=3,
        cuotas_valor=3666.66,
        garantia_meses=0,
        stock=25
    ),


]

@app.get("/productos", response_model=list[Producto], summary="Obtener todos los productos")
def obtener_productos():
    return productos_db

@app.post("/productos", response_model=Producto, status_code=201, summary="Agregar un nuevo producto")
def crear_producto(producto: Producto):
    productos_db.append(producto)
    return producto