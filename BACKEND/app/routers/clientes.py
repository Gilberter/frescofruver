from fastapi import APIRouter, HTTPException, status

from app.core.deps import DBSession, CurrentUser, AnyRole
from app.crud import cliente as crud_cliente
from app.crud import venta as crud_venta
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteOut
from app.schemas.venta import VentaResumen

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get("/", response_model=list[ClienteOut], dependencies=[AnyRole])
def listar_clientes(db: DBSession):
    return crud_cliente.list_all(db)


@router.post("/", response_model=ClienteOut, status_code=status.HTTP_201_CREATED, dependencies=[AnyRole])
def crear_cliente(data: ClienteCreate, db: DBSession):
    """Registrar cliente (RF-02.1). Falla si la cédula ya existe (RF-RNF)."""
    if crud_cliente.get_by_documento(db, data.no_documento):
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Ya existe un cliente con esa cédula")
    return crud_cliente.create(db, data)


@router.get("/buscar", response_model=ClienteOut, dependencies=[AnyRole])
def buscar_por_cedula(cedula: str, db: DBSession):
    """Buscar cliente por número de cédula (RF-02.2)."""
    cliente = crud_cliente.get_by_documento(db, cedula)
    if not cliente:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return cliente


@router.get("/{cliente_id}", response_model=ClienteOut, dependencies=[AnyRole])
def obtener_cliente(cliente_id: int, db: DBSession):
    cliente = crud_cliente.get_by_id(db, cliente_id)
    if not cliente:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return cliente


@router.patch("/{cliente_id}", response_model=ClienteOut, dependencies=[AnyRole])
def actualizar_cliente(cliente_id: int, data: ClienteUpdate, db: DBSession):
    cliente = crud_cliente.get_by_id(db, cliente_id)
    if not cliente:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return crud_cliente.update(db, cliente, data)


@router.get("/{cliente_id}/pedidos", response_model=list[VentaResumen], dependencies=[AnyRole])
def historial_pedidos(cliente_id: int, db: DBSession):
    """Historial de pedidos del cliente (RF-02.4)."""
    return crud_venta.list_by_cliente(db, cliente_id)
