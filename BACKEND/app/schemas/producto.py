from datetime import date
import enum

from pydantic import BaseModel, Field, model_validator


BAJO_STOCK_UMBRAL = 70


class EstadoProducto(str, enum.Enum):
    Activo = "Activo"
    Desactivo = "Desactivo"

# =========================
# PRODUCTO
# =========================

class ProductoCreate(BaseModel):

    nombre: str = Field(..., max_length=100)

    categoria: str = Field(..., max_length=50)

    precio_compra: float = Field(..., gt=0)

    precio_venta: float = Field(..., gt=0)

    fecha_vencimiento: date | None = None

    estado: EstadoProducto = EstadoProducto.Activo

    @model_validator(mode="after")
    def validar_precios(self):

        if self.precio_venta <= self.precio_compra:

            raise ValueError(
                "El precio de venta debe ser mayor al precio de compra"
            )

        return self


class ProductoUpdate(BaseModel):

    nombre: str | None = Field(default=None, max_length=100)

    categoria: str | None = Field(default=None, max_length=50)

    precio_compra: float | None = Field(default=None, gt=0)

    precio_venta: float | None = Field(default=None, gt=0)

    fecha_vencimiento: date | None = None

    estado: EstadoProducto | None = None


class ProductoOut(BaseModel):

    id: int

    nombre: str | None

    categoria: str | None

    precio_compra: float | None

    precio_venta: float | None

    stock_actual: int | None

    fecha_vencimiento: date | None

    estado: str | None

    bajo_stock: bool = False

    model_config = {
        "from_attributes": True
    }

    @model_validator(mode="after")
    def calcular_bajo_stock(self):

        stock = self.stock_actual or 0

        self.bajo_stock = stock < BAJO_STOCK_UMBRAL

        return self

