from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.core.database import get_db
from app.core.security import hash_password, verificar_password, crear_token
from app.core.config import settings
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioOut, Token
from app.dependencies import get_current_user
from jose import jwt, JWTError

router = APIRouter(prefix="/auth", tags=["auth"])


# ── POST /auth/register ──────────────────────────────────────────────────────
@router.post("/register", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def registrar(datos: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == datos.email).first():
        raise HTTPException(status_code=409, detail="El email ya está registrado.")
    nuevo = Usuario(
        nombre=datos.nombre,
        email=datos.email,
        hashed_password=hash_password(datos.password),
        rol="customer",
        acepto_tratamiento=datos.acepto_tratamiento,
        fecha_consentimiento=datetime.now(timezone.utc) if datos.acepto_tratamiento else None,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


# ── POST /auth/login ─────────────────────────────────────────────────────────
@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # form.username lleva el email (convención OAuth2PasswordRequestForm)
    usuario = db.query(Usuario).filter(Usuario.email == form.username).first()
    if not usuario or not verificar_password(form.password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = {"sub": str(usuario.id), "rol": usuario.rol}
    return Token(
        access_token=crear_token(payload, tipo="access"),
        refresh_token=crear_token(payload, tipo="refresh"),
    )


# ── POST /auth/refresh ───────────────────────────────────────────────────────
@router.post("/refresh", response_model=Token)
def refresh(body: dict, db: Session = Depends(get_db)):
    rt = body.get("refresh_token")
    err401 = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(rt, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("tipo") != "refresh":
            raise HTTPException(
                status_code=401,
                detail="Se requiere un refresh_token, no un access_token."
            )
        uid = payload.get("sub")
        if not uid:
            raise err401
    except JWTError:
        raise err401

    usuario = db.query(Usuario).filter(Usuario.id == int(uid)).first()
    if not usuario:
        raise err401
    p = {"sub": str(usuario.id), "rol": usuario.rol}
    return Token(
        access_token=crear_token(p, tipo="access"),
        refresh_token=crear_token(p, tipo="refresh"),
    )


# ── GET /auth/me ─────────────────────────────────────────────────────────────
@router.get("/me", response_model=UsuarioOut)
def me(current_user: Usuario = Depends(get_current_user)):
    return current_user
