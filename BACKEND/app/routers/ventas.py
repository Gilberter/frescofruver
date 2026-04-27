from fastapi import APIRouter, status

from app.core.deps import DBSession, CurrentUser, AnyRole
from app.crud import venta as crud_venta
from app.schemas.venta import VentaCreate, VentaOut, VentaResumen
from app.services import venta_service

router = APIRouter(prefix="/ventas", tags=["Ventas / Pedidos"])


@router.get("/", response_model=list[VentaResumen], dependencies=[AnyRole])
def listar_ventas(db: DBSession):
    """Listar todas las ventas (RF-07)."""
    return crud_venta.list_all(db)


@router.post("/", response_model=VentaOut, status_code=status.HTTP_201_CREATED, dependencies=[AnyRole])
def crear_venta(data: VentaCreate, db: DBSession, current_user: CurrentUser):
    """
    Crear venta con transacción atómica (RF-04.7):
    - Valida stock de cada producto
    - Crea venta + detalles + descuenta inventario
    - Rollback completo si algo falla
    """
    return venta_service.crear_venta(db, data, current_user.id)


@router.get("/{venta_id}", response_model=VentaOut, dependencies=[AnyRole])
def obtener_venta(venta_id: int, db: DBSession):
    from fastapi import HTTPException
    venta = crud_venta.get_by_id(db, venta_id)
    if not venta:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Venta no encontrada")
    return venta


@router.post("/{venta_id}/cancelar", response_model=VentaOut, dependencies=[AnyRole])
def cancelar_venta(venta_id: int, db: DBSession, current_user: CurrentUser):
    """
    Cancelar venta dentro de los primeros 10 minutos (RF-04.6).
    Revierte el stock descontado.
    """
    return venta_service.cancelar_venta(db, venta_id, current_user.id)
