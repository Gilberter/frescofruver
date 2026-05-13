
from datetime import date
from pydantic import BaseModel, Field
import enum

class EstadoOrden(str, enum.Enum):
    pendiente = "Pendiente"
    completada = "Completada"
    cancelada = "Cancelada"

class DetalleOrdenCompraIn(BaseModel):
    producto_id: int
    cantidad: int = Field(..., gt=0)
    precio_unitario: float = Field(..., gt=0)


class OrdenCompraCreate(BaseModel):

    proveedor_id: int

    detalles: list[DetalleOrdenCompraIn] = Field(
        ...,
        min_length=1
    )

class ProductoMiniOut(BaseModel):
    id: int
    nombre: str

    model_config = {"from_attributes": True}

class DetalleOrdenCompraOut(BaseModel):

    id: int

    cantidad: int

    precio_unitario: float

    subtotal: float

    producto: ProductoMiniOut

    model_config = {
        "from_attributes": True
    }


class OrdenCompraBase(BaseModel):

    id: int

    proveedor_id: int
    usuario_id: int # el usuario de dueño/admin que hizo la compra

    fecha_orden: date

    estado_orden: EstadoOrden

    total_orden: float

    model_config = {
        "from_attributes": True
    }



class OrdenCompraResumen(
    OrdenCompraBase
):
    pass

class OrdenCompraOut(
    OrdenCompraBase
):

    detalles: list[
        DetalleOrdenCompraOut
    ]