from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional
from datetime import datetime

class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str = Field(min_length=8)
    acepto_tratamiento: bool

    @model_validator(mode="after")
    def tratamiento_requerido(self):
        if not self.acepto_tratamiento:
            raise ValueError("Debés aceptar el tratamiento de datos personales para registrarte (Ley 25.326).")
        return self

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    rol: str
    acepto_tratamiento: bool

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
