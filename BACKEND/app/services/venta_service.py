from datetime import date, datetime, time, timezone, timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud import venta as crud_venta
from app.crud import producto as crud_producto
from app.crud import inventario as crud_inventario
from app.crud import cliente as crud_cliente
from app.crud import auditoria as crud_auditoria
from app.models.venta import Venta, DetalleVenta, EstadoVenta
from app.models.inventario import TipoMovimiento
from app.schemas.venta import VentaCreate

CANCEL_WINDOW_MINUTES = 10


def _fecha_venta_a_utc(fecha: date | datetime | None) -> datetime | None:
    if fecha is None:
        return None
    if isinstance(fecha, datetime):
        fv = fecha
        if fv.tzinfo is None:
            return fv.replace(tzinfo=timezone.utc)
        return fv.astimezone(timezone.utc)
    return datetime.combine(fecha, time.min, tzinfo=timezone.utc)


def crear_venta(db: Session, data: VentaCreate, actor_id: int) -> Venta:
    cliente = crud_cliente.get_by_id(db, data.cliente_id)
    if not cliente:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")

    detalles_orm: list[DetalleVenta] = []
    total = 0.0

    for item in data.detalles:
        producto = crud_producto.get_by_id(db, item.producto_id)
        if not producto:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail=f"Producto id={item.producto_id} no encontrado",
            )
        stock = producto.stock_actual or 0
        if stock < item.cantidad:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    f"Stock insuficiente para '{producto.nombre or 'producto'}'. "
                    f"Disponible: {stock}, solicitado: {item.cantidad}"
                ),
            )
        pventa = float(producto.precio_venta or 0)
        subtotal = pventa * item.cantidad
        total += subtotal
        detalles_orm.append(
            DetalleVenta(
                producto_id=item.producto_id,
                cantidad=item.cantidad,
                precio_unitario=pventa,
                subtotal=subtotal,
            )
        )

    try:
        numero_factura = crud_venta.next_factura_number(db)
        venta = Venta(
            numero_factura=numero_factura,
            cliente_id=data.cliente_id,
            usuario_id=actor_id,
            total=total,
            estado=EstadoVenta.completada,
            fecha_venta=date.today(),
            canal_venta="Tienda",
        )
        venta = crud_venta.create_with_detalles(db, venta, detalles_orm)

        for item in data.detalles:
            producto = crud_producto.get_by_id(db, item.producto_id)
            if producto is None:
                continue
            nuevo_stock = (producto.stock_actual or 0) - item.cantidad
            crud_producto.adjust_stock(db, producto, -item.cantidad)
            crud_inventario.registrar_movimiento(
                db,
                producto_id=item.producto_id,
                usuario_id=actor_id,
                tipo=TipoMovimiento.salida,
                cantidad=-item.cantidad,
                stock_resultante=nuevo_stock,
                motivo=f"Venta {numero_factura}",
            )

        crud_auditoria.registrar(
            db,
            accion="confirmar_venta",
            descripcion=f"Venta {numero_factura} confirmada. Total: {total}",
            usuario_id=actor_id,
        )
    except Exception:
        db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al procesar la venta. Se realizó rollback completo.",
        )

    return venta


def cancelar_venta(db: Session, venta_id: int, actor_id: int) -> Venta:
    venta = crud_venta.get_by_id(db, venta_id)
    if not venta:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Venta no encontrada")

    if venta.estado == EstadoVenta.cancelada:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="La venta ya fue cancelada")

    ahora = datetime.now(timezone.utc)
    fecha_venta = _fecha_venta_a_utc(venta.fecha_venta)
    if fecha_venta is None:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La venta no tiene fecha válida para evaluar la ventana de cancelación",
        )

    if ahora - fecha_venta > timedelta(minutes=CANCEL_WINDOW_MINUTES):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Solo se puede cancelar dentro de los primeros {CANCEL_WINDOW_MINUTES} minutos",
        )

    for detalle in venta.detalles:
        producto = crud_producto.get_by_id(db, detalle.producto_id or 0)
        if producto is None:
            continue
        crud_producto.adjust_stock(db, producto, detalle.cantidad or 0)
        crud_inventario.registrar_movimiento(
            db,
            producto_id=detalle.producto_id or 0,
            usuario_id=actor_id,
            tipo=TipoMovimiento.ajuste,
            cantidad=detalle.cantidad or 0,
            stock_resultante=producto.stock_actual or 0,
            motivo=f"Cancelación venta {venta.numero_factura}",
        )

    venta = crud_venta.cancel(db, venta)
    crud_auditoria.registrar(
        db,
        accion="cancelar_venta",
        descripcion=f"Venta {venta.numero_factura} cancelada",
        usuario_id=actor_id,
    )
    return venta
