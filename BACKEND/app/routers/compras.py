from fastapi import APIRouter, Query, status

from app.core.deps import DBSession, CurrentUser, AdminOrOwner
from app.crud import proveedor as crud_proveedor
from app.models.proveedor import EstadoOrden
from app.schemas.proveedor import OrdenCompraCreate, OrdenCompraOut, OrdenCompraResumen
from app.services import proveedor_service

router = APIRouter(prefix="/ordenes-compra", tags=["Órdenes de Compra"])


@router.get("/", response_model=list[OrdenCompraResumen], dependencies=[AdminOrOwner])
def listar_ordenes(
    db: DBSession,
    proveedor_id: int | None = Query(default=None),
    estado: EstadoOrden | None = Query(default=None),
):
    """Historial filtrable por proveedor y estado (RF-05.8)."""
    return crud_proveedor.list_ordenes(db, proveedor_id, estado)


@router.post("/", response_model=OrdenCompraOut, status_code=status.HTTP_201_CREATED, dependencies=[AdminOrOwner])
def crear_orden(data: OrdenCompraCreate, db: DBSession, current_user: CurrentUser):
    """
    Crear orden de compra vinculada a proveedor activo (RF-05.1, RF-05.2).
    Solo Admin/Dueño pueden acceder.
    """
    return proveedor_service.crear_orden_compra(db, data, current_user.id)


@router.get("/{orden_id}", response_model=OrdenCompraOut, dependencies=[AdminOrOwner])
def obtener_orden(orden_id: int, db: DBSession):
    from fastapi import HTTPException
    orden = crud_proveedor.get_orden_by_id(db, orden_id)
    if not orden:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
    return orden


@router.post("/{orden_id}/recibir", response_model=OrdenCompraOut, dependencies=[AdminOrOwner])
def recibir_orden(orden_id: int, db: DBSession, current_user: CurrentUser):
    """
    Marcar orden como Completada → aumenta el inventario (RF-05.5).
    Solo funciona si la orden está en estado Pendiente.
    """
    return proveedor_service.recibir_orden(db, orden_id, current_user.id)


@router.post("/{orden_id}/cancelar", response_model=OrdenCompraOut, dependencies=[AdminOrOwner])
def cancelar_orden(orden_id: int, db: DBSession, current_user: CurrentUser):
    """Cancelar orden en estado Pendiente (RF-05.7)."""
    return proveedor_service.cancelar_orden(db, orden_id, current_user.id)
