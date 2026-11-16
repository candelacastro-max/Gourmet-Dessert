from tests.ayudantes import cuerpo_pedido

def test_arrepentimiento_sin_sesion(client, cliente, producto):
    # 1. Compramos 1 unidad
    r_compra = client.post("/pedidos/", headers=cliente, json=cuerpo_pedido(producto["id"], 1))
    assert r_compra.status_code == 201
    pedido_id = r_compra.json()["id"]

    # Stock bajó a 1
    assert client.get(f"/productos/{producto['id']}").json()["stock"] == 1

    # 2. Arrepentimiento sin sesión (sin Authorization headers)
    r_arr = client.post(
        "/arrepentimiento",
        json={"pedido_id": pedido_id, "email": "cliente@prueba.com"},
    )
    assert r_arr.status_code == 201
    assert "codigo" in r_arr.json()
    assert r_arr.json()["codigo"].startswith("ARR-")

    # El stock vuelve a 2
    assert client.get(f"/productos/{producto['id']}").json()["stock"] == 2

def test_arrepentimiento_no_revela(client):
    # Pedido que no existe: respuesta uniforme con 201 y código
    r = client.post(
        "/arrepentimiento",
        json={"pedido_id": 99999, "email": "inexistente@prueba.com"},
    )
    assert r.status_code == 201
    assert "codigo" in r.json()
    assert r.json()["codigo"].startswith("ARR-")

def test_arrepentimiento_correo_distinto_no_devuelve_stock(client, cliente, producto):
    # BT9: Arrepentimiento con correo que no coincide responde 201 igual pero NO cancela ni devuelve stock
    r_compra = client.post("/pedidos/", headers=cliente, json=cuerpo_pedido(producto["id"], 1))
    assert r_compra.status_code == 201
    pedido_id = r_compra.json()["id"]

    # Stock bajó a 1
    assert client.get(f"/productos/{producto['id']}").json()["stock"] == 1

    r_arr = client.post(
        "/arrepentimiento",
        json={"pedido_id": pedido_id, "email": "intruso@prueba.com"},
    )
    assert r_arr.status_code == 201
    assert "codigo" in r_arr.json()

    # El stock sigue en 1 (NO volvió porque el email no coincide)
    assert client.get(f"/productos/{producto['id']}").json()["stock"] == 1
