from datetime import datetime
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
    producto_id: int
    cantidad: int
    precio_unitario: float
    subtotal: float

    model_config = {"from_attributes": True}


class VentaOut(BaseModel):
    id: int
    numero_factura: str
    cliente_id: int
    fecha_venta: datetime
    total: float
    estado: EstadoVenta
    detalles: list[DetalleVentaOut] = []

    model_config = {"from_attributes": True}


class VentaResumen(BaseModel):
    id: int
    numero_factura: str
    cliente_id: int
    fecha_venta: datetime
    total: float
    estado: EstadoVenta

    model_config = {"from_attributes": True}
