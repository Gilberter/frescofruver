from datetime import datetime, timezone, timedelta
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


def crear_venta(db: Session, data: VentaCreate, actor_id: int) -> Venta:
    # 1. Validate cliente
    cliente = crud_cliente.get_by_id(db, data.cliente_id)
    if not cliente:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")

    # 2. Validate stock for every product before touching anything
    detalles_orm: list[DetalleVenta] = []
    total = 0.0

    for item in data.detalles:
        producto = crud_producto.get_by_id(db, item.producto_id)
        if not producto:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail=f"Producto id={item.producto_id} no encontrado",
            )
        if producto.stock_actual < item.cantidad:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Stock insuficiente para '{producto.nombre}'. "
                       f"Disponible: {producto.stock_actual}, solicitado: {item.cantidad}",
            )
        subtotal = float(producto.precio_venta) * item.cantidad
        total += subtotal
        detalles_orm.append(
            DetalleVenta(
                producto_id=item.producto_id,
                cantidad=item.cantidad,
                precio_unitario=float(producto.precio_venta),
                subtotal=subtotal,
            )
        )

    # 3. Atomic transaction: create venta + detalles + discount stock
    try:
        numero_factura = crud_venta.next_factura_number(db)
        venta = Venta(
            numero_factura=numero_factura,
            cliente_id=data.cliente_id,
            total=total
            )
        venta = crud_venta.create_with_detalles(db, venta, detalles_orm)

        for item in data.detalles:
            producto = crud_producto.get_by_id(db, item.producto_id)
            if producto is None:
                print("Producto no encontrado")
                continue
            nuevo_stock = producto.stock_actual - item.cantidad
            crud_producto.adjust_stock(db, producto, -item.cantidad)
            crud_inventario.registrar_movimiento(
                db,
                producto_id=item.producto_id,
                usuario_id=actor_id,
                tipo=TipoMovimiento.pedido,
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

    # Enforce 10-minute cancellation window
    ahora = datetime.now(timezone.utc)
    fecha_venta = venta.fecha_venta
    if fecha_venta.tzinfo is None:
        fecha_venta = fecha_venta.replace(tzinfo=timezone.utc)

    if ahora - fecha_venta > timedelta(minutes=CANCEL_WINDOW_MINUTES):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Solo se puede cancelar dentro de los primeros {CANCEL_WINDOW_MINUTES} minutos",
        )

    # Revert stock
    for detalle in venta.detalles:
        producto = crud_producto.get_by_id(db, detalle.producto_id)
        if producto is None:
            print("Producto no encontrado")
            continue
        crud_producto.adjust_stock(db, producto, detalle.cantidad)
        crud_inventario.registrar_movimiento(
            db,
            producto_id=detalle.producto_id,
            usuario_id=actor_id,
            tipo=TipoMovimiento.ajuste,
            cantidad=detalle.cantidad,
            stock_resultante=producto.stock_actual,
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
