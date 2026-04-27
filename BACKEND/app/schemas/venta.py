from datetime import date
from pydantic import BaseModel, Field
from app.models.venta import EstadoVenta


class DetalleVentaIn(BaseModel):
    producto_id: int
    cantidad: int = Field(..., gt=0)


class VentaCreate(BaseModel):
    cliente_id: int
    detalles: list[DetalleVentaIn] = Field(..., min_length=1)


class DetalleVentaOut(BaseModel):
    id: int
    producto_id: int | None
    cantidad: int | None
    precio_unitario: float | None
    subtotal: float | None

    model_config = {"from_attributes": True}


class VentaOut(BaseModel):
    id: int
    numero_factura: str | None
    cliente_id: int | None
    usuario_id: int | None
    canal_venta: str | None
    fecha_venta: date | None
    total: float | None
    estado: EstadoVenta | None
    detalles: list[DetalleVentaOut] = []

    model_config = {"from_attributes": True}


class VentaResumen(BaseModel):
    id: int
    numero_factura: str | None
    cliente_id: int | None
    usuario_id: int | None
    canal_venta: str | None
    fecha_venta: date | None
    total: float | None
    estado: EstadoVenta | None

    model_config = {"from_attributes": True}
