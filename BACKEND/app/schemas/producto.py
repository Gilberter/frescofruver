from datetime import date

from pydantic import BaseModel, Field, model_validator

from app.models.producto import BAJO_STOCK_UMBRAL


class ProductoCreate(BaseModel):
    nombre: str = Field(..., max_length=100)
    categoria: str = Field(..., max_length=50)
    precio_compra: float = Field(..., gt=0)
    precio_venta: float = Field(..., gt=0)
    stock_actual: int = Field(default=0, ge=0)
    fecha_vencimiento: date | None = None
    estado: str = Field(default="Activo", max_length=20)

    @model_validator(mode="after")
    def precio_venta_mayor(self):
        if self.precio_venta <= self.precio_compra:
            raise ValueError("El precio de venta debe ser mayor al precio de compra")
        return self


class ProductoUpdate(BaseModel):
    nombre: str | None = Field(default=None, max_length=100)
    categoria: str | None = Field(default=None, max_length=50)
    precio_compra: float | None = Field(default=None, gt=0)
    precio_venta: float | None = Field(default=None, gt=0)
    fecha_vencimiento: date | None = None
    estado: str | None = Field(default=None, max_length=20)


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

    model_config = {"from_attributes": True}

    @model_validator(mode="after")
    def set_bajo_stock(self):
        sa = self.stock_actual if self.stock_actual is not None else 0
        self.bajo_stock = sa < BAJO_STOCK_UMBRAL
        return self


class AjusteInventarioIn(BaseModel):
    cantidad: int = Field(..., description="Positivo = entrada, negativo = salida")
    motivo: str = Field(..., min_length=3, max_length=255)
