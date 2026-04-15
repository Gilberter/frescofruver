from fastapi import APIRouter, status

from app.core.deps import DBSession, CurrentUser, AdminOrOwner
from app.crud import proveedor as crud_proveedor
from app.schemas.proveedor import (
    ProveedorCreate,
    ProveedorUpdate,
    ProveedorOut,
    ProveedorPerfil,
)
from app.services import proveedor_service

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])


@router.get("/", response_model=list[ProveedorOut], dependencies=[AdminOrOwner])
def listar_proveedores(db: DBSession):
    return crud_proveedor.list_all(db)


@router.post("/", response_model=ProveedorOut, status_code=status.HTTP_201_CREATED, dependencies=[AdminOrOwner])
def crear_proveedor(data: ProveedorCreate, db: DBSession, current_user: CurrentUser):
    """Registrar proveedor (RF-06.1)."""
    return proveedor_service.crear_proveedor(db, data, current_user.id)


@router.get("/{proveedor_id}", response_model=ProveedorOut, dependencies=[AdminOrOwner])
def obtener_proveedor(proveedor_id: int, db: DBSession):
    from fastapi import HTTPException
    prov = crud_proveedor.get_by_id(db, proveedor_id)
    if not prov:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado")
    return prov


@router.get("/{proveedor_id}/perfil", response_model=ProveedorPerfil, dependencies=[AdminOrOwner])
def perfil_proveedor(proveedor_id: int, db: DBSession):
    """Ver perfil con total de compras y monto invertido (RF-06.3)."""
    return proveedor_service.perfil_proveedor(db, proveedor_id)


@router.patch("/{proveedor_id}", response_model=ProveedorOut, dependencies=[AdminOrOwner])
def actualizar_proveedor(proveedor_id: int, data: ProveedorUpdate, db: DBSession, current_user: CurrentUser):
    """Editar o desactivar proveedor (RF-06.2)."""
    return proveedor_service.actualizar_proveedor(db, proveedor_id, data, current_user.id)
