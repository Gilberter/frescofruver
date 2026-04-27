from fastapi import APIRouter

from app.core.deps import DBSession, AdminOrOwner
from app.crud import inventario as crud_inventario
from app.schemas.inventario import MovimientoOut

router = APIRouter(prefix="/inventario", tags=["Inventario"])


@router.get("/movimientos", response_model=list[MovimientoOut], dependencies=[AdminOrOwner])
def todos_los_movimientos(db: DBSession):
    """Historial completo de movimientos de inventario (RF-03.5)."""
    return crud_inventario.list_all(db)
