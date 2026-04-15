from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud import proveedor as crud_proveedor
from app.crud import producto as crud_producto
from app.crud import inventario as crud_inventario
from app.crud import auditoria as crud_auditoria
from app.models.proveedor import Proveedor, OrdenCompra, DetalleCompra, EstadoOrden
from app.models.inventario import TipoMovimiento
from app.schemas.proveedor import ProveedorCreate, ProveedorUpdate, OrdenCompraCreate, ProveedorPerfil


def crear_proveedor(db: Session, data: ProveedorCreate, actor_id: int) -> Proveedor:
    proveedor = crud_proveedor.create(db, data)
    crud_auditoria.registrar(db, "crear_proveedor", f"Proveedor '{data.nombre}' creado", actor_id)
    return proveedor


def actualizar_proveedor(db: Session, proveedor_id: int, data: ProveedorUpdate, actor_id: int) -> Proveedor:
    prov = crud_proveedor.get_by_id(db, proveedor_id)
    if not prov:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado")
    updated = crud_proveedor.update(db, prov, data)
    crud_auditoria.registrar(db, "actualizar_proveedor", f"Proveedor id={proveedor_id} actualizado", actor_id)
    return updated


def perfil_proveedor(db: Session, proveedor_id: int) -> ProveedorPerfil:
    prov = crud_proveedor.get_by_id(db, proveedor_id)
    if not prov:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado")
    stats = crud_proveedor.get_perfil_stats(db, proveedor_id)
    return ProveedorPerfil.model_validate({**prov.__dict__, **stats})


def crear_orden_compra(db: Session, data: OrdenCompraCreate, actor_id: int) -> OrdenCompra:
    prov = crud_proveedor.get_by_id(db, data.proveedor_id)
    if not prov or prov.estado != "activo":
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No se puede crear una orden sin un proveedor activo seleccionado",
        )

    total = 0.0
    detalles_orm: list[DetalleCompra] = []

    for item in data.detalles:
        producto = crud_producto.get_by_id(db, item.producto_id)
        if not producto:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Producto id={item.producto_id} no encontrado")
        subtotal = item.precio_costo * item.cantidad
        total += subtotal
        detalles_orm.append(
            DetalleCompra(
                producto_id=item.producto_id,
                cantidad=item.cantidad,
                precio_costo=item.precio_costo,
                subtotal=subtotal,
            )
        )

    orden = OrdenCompra(proveedor_id=data.proveedor_id, total_orden=total)
    orden = crud_proveedor.create_orden_with_detalles(db, orden, detalles_orm)
    crud_auditoria.registrar(db, "crear_orden_compra", f"Orden id={orden.id} creada", actor_id)
    return orden


def recibir_orden(db: Session, orden_id: int, actor_id: int) -> OrdenCompra:
    orden = crud_proveedor.get_orden_by_id(db, orden_id)
    if not orden:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
    if orden.estado_orden != EstadoOrden.pendiente:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Solo se pueden recibir órdenes en estado Pendiente")

    # Increase stock for each detail
    for detalle in orden.detalles:

        producto = crud_producto.get_by_id(db, detalle.producto_id) 
        if producto is None:
            print(f"Producto no encontrado")
            continue
        crud_producto.adjust_stock(db, producto, detalle.cantidad)
        crud_inventario.registrar_movimiento(
            db,
            producto_id=detalle.producto_id,
            usuario_id=actor_id,
            tipo=TipoMovimiento.compra,
            cantidad=detalle.cantidad,
            stock_resultante=producto.stock_actual,
            motivo=f"Recepción orden id={orden_id}",
        )

    orden = crud_proveedor.update_estado_orden(db, orden, EstadoOrden.recibida)
    crud_auditoria.registrar(db, "recibir_orden", f"Orden id={orden_id} marcada como Recibida", actor_id)
    return orden


def cancelar_orden(db: Session, orden_id: int, actor_id: int) -> OrdenCompra:
    orden = crud_proveedor.get_orden_by_id(db, orden_id)
    if not orden:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
    if orden.estado_orden != EstadoOrden.pendiente:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Solo se pueden cancelar órdenes en estado Pendiente",
        )
    orden = crud_proveedor.update_estado_orden(db, orden, EstadoOrden.cancelada)
    crud_auditoria.registrar(db, "cancelar_orden", f"Orden id={orden_id} cancelada", actor_id)
    return orden
