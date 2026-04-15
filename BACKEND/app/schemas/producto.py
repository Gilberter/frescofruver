from pydantic import BaseModel, Field, model_validator
from app.models.producto import CategoriaProducto, UnidadMedida


class ProductoCreate(BaseModel):
    nombre: str = Field(..., max_length=100)
    categoria: CategoriaProducto
    unidad_medida: UnidadMedida
    precio_compra: float = Field(..., gt=0)
    precio_venta: float = Field(..., gt=0)
    stock_actual: int = Field(default=0, ge=0)
    stock_minimo: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def precio_venta_mayor(self):
        if self.precio_venta <= self.precio_compra:
            raise ValueError("El precio de venta debe ser mayor al precio de compra")
        return self


class ProductoUpdate(BaseModel):
    nombre: str | None = None
    categoria: CategoriaProducto | None = None
    unidad_medida: UnidadMedida | None = None
    precio_compra: float | None = Field(default=None, gt=0)
    precio_venta: float | None = Field(default=None, gt=0)
    stock_minimo: int | None = Field(default=None, ge=0)
    estado: str | None = None


class ProductoOut(BaseModel):
    id: int
    nombre: str
    categoria: CategoriaProducto
    unidad_medida: UnidadMedida
    precio_compra: float
    precio_venta: float
    stock_actual: int
    stock_minimo: int
    estado: str
    bajo_stock: bool = False

    model_config = {"from_attributes": True}

    @model_validator(mode="after")
    def set_bajo_stock(self):
        self.bajo_stock = self.stock_actual <= self.stock_minimo
        return self


class AjusteInventarioIn(BaseModel):
    cantidad: int = Field(..., description="Positivo = entrada, negativo = salida")
    motivo: str = Field(..., min_length=3, max_length=255)
