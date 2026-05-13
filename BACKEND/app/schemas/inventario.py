from datetime import date
from pydantic import BaseModel, Field, model_validator
import enum

class TipoMovimiento(str, enum.Enum):
    entrada = "Entrada"
    salida = "Salida"
    ajuste = "Ajuste"

class MovimientoOut(BaseModel):
    id: int
    producto_id: int
    usuario_id: int
    fecha_movimiento: date
    tipo_movimiento: TipoMovimiento
    cantidad: int
    motivo: str
    observacion: str | None = None
    stock_resultante: int | None

    model_config = {"from_attributes": True}


# =========================
# INVENTARIO
# =========================

class MovimientoIn(BaseModel):

    tipo: TipoMovimiento

    cantidad: int = Field(..., gt=0)

    motivo: str = Field(
        ...,
        min_length=3,
        max_length=255
    )

    observacion: str | None = Field(
        default=None,
        max_length=255
    )