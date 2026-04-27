from pydantic import BaseModel, Field
from app.models.usuario import RolUsuario


class UsuarioCreate(BaseModel):
    nombre_completo: str = Field(..., max_length=150)
    no_documento: str = Field(..., max_length=50)
    username: str = Field(..., max_length=60)
    password: str = Field(..., min_length=6)
    telefono: str = Field(..., max_length=20)
    correo: str = Field(..., max_length=100)
    rol: RolUsuario = RolUsuario.vendedor
    estado: str = "Activo"


class UsuarioUpdate(BaseModel):
    nombre_completo: str | None = None
    rol: RolUsuario | None = None
    estado: str | None = None


class UsuarioOut(BaseModel):
    id: int
    nombre_completo: str
    no_documento: str
    username: str
    telefono: str | None = None
    correo: str | None = None
    rol: RolUsuario
    estado: str

    model_config = {"from_attributes": True}


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    rol: RolUsuario
    username: str
