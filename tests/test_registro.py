def test_registro_sin_consentimiento_se_rechaza(client):
    r = client.post(
        "/auth/register",
        json={
            "nombre": "Sin Consentimiento",
            "email": "sin_consentimiento@prueba.com",
            "password": "clave-larga-123",
            "acepto_tratamiento": False,
        },
    )
    assert r.status_code == 422

def test_registro_con_consentimiento_y_login(client):
    email = "nuevo@prueba.com"
    password = "clave-super-segura"
    r = client.post(
        "/auth/register",
        json={
            "nombre": "Usuario Nuevo",
            "email": email,
            "password": password,
            "acepto_tratamiento": True,
        },
    )
    assert r.status_code == 201
    datos = r.json()
    assert "password" not in datos
    assert "hashed_password" not in datos

    # Verificamos que ahora pueda iniciar sesión
    r_login = client.post("/auth/login", data={"username": email, "password": password})
    assert r_login.status_code == 200
    assert "access_token" in r_login.json()

def test_login_con_clave_incorrecta(client):
    email = "usuario_existente@prueba.com"
    r = client.post(
        "/auth/register",
        json={
            "nombre": "Usuario",
            "email": email,
            "password": "clave-correcta-123",
            "acepto_tratamiento": True,
        },
    )
    assert r.status_code == 201

    r_login = client.post("/auth/login", data={"username": email, "password": "clave-INCORRECTA"})
    assert r_login.status_code == 401
