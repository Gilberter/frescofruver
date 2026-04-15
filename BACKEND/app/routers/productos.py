from fastapi import APIRouter, HTTPException, status, Query

from app.core.deps import DBSession, CurrentUser, AnyRole, AdminOrOwner
from app.crud import producto as crud_producto
from app.crud import inventario as crud_inventario
from app.models.producto import CategoriaProducto
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoOut, AjusteInventarioIn
from app.schemas.inventario import MovimientoOut
from app.services import producto_service

router = APIRouter(prefix="/productos", tags=["Productos e Inventario"])


@router.get("/", response_model=list[ProductoOut], dependencies=[AnyRole])
def listar_productos(
    db: DBSession,
    categoria: CategoriaProducto | None = Query(default=None),
):
    """Inventario en tiempo real filtrable por categoría (RF-03.2)."""
    return crud_producto.list_all(db, categoria)


@router.get("/bajo-stock", response_model=list[ProductoOut], dependencies=[AnyRole])
def productos_bajo_stock(db: DBSession):
    """Productos cuyo stock_actual <= stock_minimo (RF-07)."""
    return crud_producto.list_bajo_stock(db)


@router.post("/", response_model=ProductoOut, status_code=status.HTTP_201_CREATED, dependencies=[AdminOrOwner])
def crear_producto(data: ProductoCreate, db: DBSession, current_user: CurrentUser):
    """Registrar nuevo producto (RF-03.1)."""
    return producto_service.crear_producto(db, data, current_user.id)


@router.get("/{producto_id}", response_model=ProductoOut, dependencies=[AnyRole])
def obtener_producto(producto_id: int, db: DBSession):
    producto = crud_producto.get_by_id(db, producto_id)
    if not producto:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return producto


@router.patch("/{producto_id}", response_model=ProductoOut, dependencies=[AdminOrOwner])
def actualizar_producto(producto_id: int, data: ProductoUpdate, db: DBSession, current_user: CurrentUser):
    """Actualizar producto (RF-03.1). Audita cambio de precio (RF-08)."""
    return producto_service.actualizar_producto(db, producto_id, data, current_user.id)


@router.post("/{producto_id}/ajuste", response_model=ProductoOut, dependencies=[AdminOrOwner])
def ajuste_manual(producto_id: int, data: AjusteInventarioIn, db: DBSession, current_user: CurrentUser):
    """Ajuste manual de inventario con motivo obligatorio (RF-03.4)."""
    return producto_service.ajuste_manual(db, producto_id, data, current_user.id)


@router.get("/{producto_id}/movimientos", response_model=list[MovimientoOut], dependencies=[AnyRole])
def movimientos_producto(producto_id: int, db: DBSession):
    """Historial de movimientos de inventario del producto (RF-03.5)."""
    return crud_inventario.list_by_producto(db, producto_id)
