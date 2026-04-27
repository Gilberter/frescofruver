from datetime import datetime
from pydantic import BaseModel


class AuditoriaOut(BaseModel):
    id: int
    usuario_id: int | None
    fecha_auditoria: datetime
    accion: str
    descripcion: str | None

    model_config = {"from_attributes": True}
