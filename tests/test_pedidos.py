from tests.ayudantes import cuerpo_pedido

def test_compra_descuenta_stock(client, cliente, producto):
    r = client.post("/pedidos/", headers=cliente, json=cuerpo_pedido(producto["id"], 1))
    assert r.status_code == 201
    # Stock baja de 2 a 1
    prod = client.get(f"/productos/{producto['id']}").json()
    assert prod["stock"] == 1

def test_sin_stock_da_409_y_no_toca_nada(client, cliente, producto):
    r = client.post(
        "/pedidos/", headers=cliente, json=cuerpo_pedido(producto["id"], 3)
    )
    assert r.status_code == 409
    # El rollback: el stock sigue igual y no quedó un pedido a medias
    assert client.get(f"/productos/{producto['id']}").json()["stock"] == 2
    assert client.get("/pedidos/mios", headers=cliente).json() == []

def test_precio_congelado(client, cliente, admin, producto):
    # Compra a precio 1000
    r = client.post("/pedidos/", headers=cliente, json=cuerpo_pedido(producto["id"], 1))
    assert r.status_code == 201
    pedido_id = r.json()["id"]

    # El admin sube el precio a 5000
    r_put = client.put(f"/productos/{producto['id']}", headers=admin, json={"precio": 5000})
    assert r_put.status_code == 200

    # El pedido histórico sigue teniendo el precio viejo (1000)
    pedidos = client.get("/pedidos/mios", headers=cliente).json()
    pedido = next(p for p in pedidos if p["id"] == pedido_id)
    assert float(pedido["total"]) == 1000.0
    assert float(pedido["items"][0]["precio_unitario"]) == 1000.0

def test_comprar_sin_sesion_da_401(client, producto):
    r = client.post("/pedidos/", json=cuerpo_pedido(producto["id"], 1))
    assert r.status_code == 401
