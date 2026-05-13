from datetime import date
from pydantic import BaseModel, Field


class ProveedorCreate(BaseModel):
    nombre: str = Field(..., max_length=100)
    telefono: str | None = Field(default=None, max_length=20)
    correo: str | None = Field(default=None, max_length=100)
    direccion: str | None = Field(default=None, max_length=150)


class ProveedorUpdate(BaseModel):
    nombre: str | None = Field(default=None, max_length=100)
    telefono: str | None = Field(default=None, max_length=20)
    correo: str | None = Field(default=None, max_length=100)
    direccion: str | None = Field(default=None, max_length=150)
    estado: str | None = Field(default=None, max_length=20)


class ProveedorOut(BaseModel):
    id: int
    nombre: str | None
    telefono: str | None
    correo: str | None
    direccion: str | None
    estado: str | None

    model_config = {"from_attributes": True}


class ProveedorPerfil(ProveedorOut):
    total_ordenes: int = 0
    monto_total_invertido: float = 0.0
