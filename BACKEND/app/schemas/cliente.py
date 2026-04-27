from pydantic import BaseModel, Field


class ClienteCreate(BaseModel):
    nombre_completo: str = Field(..., max_length=100)
    no_documento: str = Field(..., max_length=50)
    telefono: str | None = Field(default=None, max_length=20)
    correo: str | None = Field(default=None, max_length=100)
    direccion: str | None = Field(default=None, max_length=150)


class ClienteUpdate(BaseModel):
    nombre_completo: str | None = Field(default=None, max_length=100)
    telefono: str | None = Field(default=None, max_length=20)
    correo: str | None = Field(default=None, max_length=100)
    direccion: str | None = Field(default=None, max_length=150)
    estado: str | None = Field(default=None, max_length=20)


class ClienteOut(BaseModel):
    id: int
    nombre_completo: str | None
    no_documento: str | None
    telefono: str | None
    correo: str | None
    direccion: str | None
    estado: str | None

    model_config = {"from_attributes": True}
