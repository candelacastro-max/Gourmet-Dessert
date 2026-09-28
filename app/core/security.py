# pyrefly: ignore [missing-import]
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verificar_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def crear_token(data: dict, tipo: str = "access") -> str:
    """Crea un JWT. tipo puede ser 'access' o 'refresh'."""
    minutos = settings.ACCESS_MIN if tipo == "access" else settings.REFRESH_MIN
    payload = data.copy()
    payload.update({
        "tipo": tipo,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=minutos)
    })
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
