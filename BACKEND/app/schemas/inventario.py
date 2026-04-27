from datetime import date
from pydantic import BaseModel
from app.models.inventario import TipoMovimiento


class MovimientoOut(BaseModel):
    id: int
    producto_id: int | None
    usuario_id: int | None
    fecha_movimiento: date | None
    tipo_movimiento: TipoMovimiento | None
    cantidad: int | None
    motivo: str | None
    stock_resultante: int | None

    model_config = {"from_attributes": True}
