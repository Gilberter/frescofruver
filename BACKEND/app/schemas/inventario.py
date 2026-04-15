from datetime import datetime
from pydantic import BaseModel
from app.models.inventario import TipoMovimiento


class MovimientoOut(BaseModel):
    id: int
    producto_id: int
    usuario_id: int
    fecha_movimiento: datetime
    tipo_movimiento: TipoMovimiento
    cantidad: int
    motivo: str | None
    stock_resultante: int

    model_config = {"from_attributes": True}
