from pydantic import BaseModel, Field


class ClienteCreate(BaseModel):
    nombre_completo: str = Field(..., max_length=150)
    no_documento: str = Field(..., max_length=20)
    telefono: str | None = None
    direccion: str | None = None


class ClienteUpdate(BaseModel):
    nombre_completo: str | None = None
    telefono: str | None = None
    direccion: str | None = None
    estado: str | None = None


class ClienteOut(BaseModel):
    id: int
    nombre_completo: str
    no_documento: str
    telefono: str | None
    direccion: str | None
    estado: str

    model_config = {"from_attributes": True}
