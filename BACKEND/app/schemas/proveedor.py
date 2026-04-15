from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from app.models.proveedor import EstadoOrden


class ProveedorCreate(BaseModel):
    nombre: str = Field(..., max_length=150)
    contacto: str | None = None
    telefono: str | None = None
    correo: str | None = None
    direccion: str | None = None


class ProveedorUpdate(BaseModel):
    nombre: str | None = None
    contacto: str | None = None
    telefono: str | None = None
    correo: str | None = None
    direccion: str | None = None
    estado: str | None = None


class ProveedorOut(BaseModel):
    id: int
    nombre: str
    contacto: str | None
    telefono: str | None
    correo: str | None
    direccion: str | None
    estado: str

    model_config = {"from_attributes": True}


class ProveedorPerfil(ProveedorOut):
    total_ordenes: int = 0
    monto_total_invertido: float = 0.0


# ── Orden de Compra ───────────────────────────────────────────────────────────

class DetalleCompraIn(BaseModel):
    producto_id: int
    cantidad: int = Field(..., gt=0)
    precio_costo: float = Field(..., gt=0)


class OrdenCompraCreate(BaseModel):
    proveedor_id: int
    detalles: list[DetalleCompraIn] = Field(..., min_length=1)


class DetalleCompraOut(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_costo: float
    subtotal: float

    model_config = {"from_attributes": True}


class OrdenCompraOut(BaseModel):
    id: int
    proveedor_id: int
    fecha_orden: datetime
    estado_orden: EstadoOrden
    total_orden: float
    detalles: list[DetalleCompraOut] = []

    model_config = {"from_attributes": True}


class OrdenCompraResumen(BaseModel):
    id: int
    proveedor_id: int
    fecha_orden: datetime
    estado_orden: EstadoOrden
    total_orden: float

    model_config = {"from_attributes": True}
