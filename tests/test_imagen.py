TRAMPA = ("foto.png", b"esto es texto plano con nombre de imagen", "image/png")
PNG_REAL_GRANDE = ("grande.png", b"\x89PNG\r\n\x1a\n" + b"0" * (2 * 1024 * 1024 + 10), "image/png")

def test_archivo_trampa_da_415(client, admin, producto):
    r = client.post(
        f"/productos/{producto['id']}/imagen",
        headers=admin,
        files={"archivo": TRAMPA},
    )
    assert r.status_code == 415

def test_cliente_no_puede_subir_imagen(client, cliente, producto):
    r = client.post(
        f"/productos/{producto['id']}/imagen",
        headers=cliente,
        files={"archivo": TRAMPA},
    )
    assert r.status_code == 403

def test_sin_sesion_no_puede_subir_imagen(client, producto):
    r = client.post(
        f"/productos/{producto['id']}/imagen",
        files={"archivo": TRAMPA},
    )
    assert r.status_code == 401

def test_imagen_grande_da_413(client, admin, producto):
    r = client.post(
        f"/productos/{producto['id']}/imagen",
        headers=admin,
        files={"archivo": PNG_REAL_GRANDE},
    )
    assert r.status_code == 413
