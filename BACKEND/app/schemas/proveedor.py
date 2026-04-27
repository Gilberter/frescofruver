from datetime import date
from pydantic import BaseModel, Field
from app.models.proveedor import EstadoOrden


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


class DetalleCompraIn(BaseModel):
    producto_id: int
    cantidad: int = Field(..., gt=0)
    precio_costo: float = Field(..., gt=0)


class OrdenCompraCreate(BaseModel):
    proveedor_id: int
    cliente_id: int | None = Field(
        default=None,
        description="Opcional; si se omite se usa el mismo id que el proveedor (compatibilidad con datos de ejemplo).",
    )
    detalles: list[DetalleCompraIn] = Field(..., min_length=1)


class DetalleCompraOut(BaseModel):
    id: int
    producto_id: int | None
    cantidad: int | None
    precio_costo: float | None
    subtotal: float | None

    model_config = {"from_attributes": True}


class OrdenCompraOut(BaseModel):
    id: int
    proveedor_id: int | None
    cliente_id: int | None
    fecha_orden: date | None
    estado_orden: EstadoOrden | None
    total_orden: float | None
    detalles: list[DetalleCompraOut] = []

    model_config = {"from_attributes": True}


class OrdenCompraResumen(BaseModel):
    id: int
    proveedor_id: int | None
    cliente_id: int | None
    fecha_orden: date | None
    estado_orden: EstadoOrden | None
    total_orden: float | None

    model_config = {"from_attributes": True}
