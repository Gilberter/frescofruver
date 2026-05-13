from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud import producto as crud_producto
from app.crud import inventario as crud_inventario
from app.crud import auditoria as crud_auditoria
from app.models.producto import Producto
from app.models.inventario import TipoMovimiento, MovimientoIn, MovimientoOut
from app.schemas.producto import ProductoCreate, ProductoUpdate



def crear_producto(db: Session, data: ProductoCreate, actor_id: int) -> Producto:
    producto = crud_producto.create(db, data)
    crud_auditoria.registrar(
        db,
        accion="crear_producto",
        descripcion=f"Producto '{data.nombre}' creado",
        usuario_id=actor_id,
    )
    return producto


def actualizar_producto(db: Session, producto_id: int, data: ProductoUpdate, actor_id: int) -> Producto:
    producto = crud_producto.get_by_id(db, producto_id)
    if not producto:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

    # Audit price changes
    if data.precio_venta is not None and float(data.precio_venta) != float(producto.precio_venta or 0):
        crud_auditoria.registrar(
            db,
            accion="cambio_precio",
            descripcion=(
                f"Producto id={producto_id}: precio venta "
                f"{producto.precio_venta} → {data.precio_venta}"
            ),
            usuario_id=actor_id,
        )

    return crud_producto.update(db, producto, data)


def ajuste_inventario(
    db: Session,
    producto_id: int,
    data: MovimientoIn,
    actor_id: int,
) -> Producto:

    producto = crud_producto.get_by_id(
        db,
        producto_id
    )

    if not producto:

        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado",
        )

    stock_actual = producto.stock_actual or 0


    print(f"Producto data.tipo {data.tipo}")
    if data.tipo == TipoMovimiento.entrada:
        
        nuevo_stock = stock_actual + data.cantidad
        print(f"Producto nuevo_stock {nuevo_stock}")

    elif data.tipo == TipoMovimiento.salida:

        if data.cantidad > stock_actual:

            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    f"Stock insuficiente. "
                    f"Stock actual: {stock_actual}"
                ),
            )

        nuevo_stock = stock_actual - data.cantidad

    elif data.tipo == TipoMovimiento.ajuste:

        nuevo_stock = data.cantidad

    else:

        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Tipo de movimiento inválido",
        )


    producto.stock_actual = nuevo_stock

    db.commit()

    db.refresh(producto)

    print(f"Producto actualizado {producto.stock_actual}")

    crud_inventario.registrar_movimiento(
        db,
        producto_id=producto_id,
        usuario_id=actor_id,
        tipo=data.tipo,
        cantidad=data.cantidad,
        stock_resultante=nuevo_stock,
        motivo=data.motivo,
    )

    # =========================
    # AUDITORÍA
    # =========================

    crud_auditoria.registrar(
        db,
        accion="movimiento_inventario",
        descripcion=(
            f"Producto id={producto_id} | "
            f"tipo={data.tipo.value} | "
            f"cantidad={data.cantidad} | "
            f"stock_final={nuevo_stock} | "
            f"motivo={data.motivo}"
        ),
        usuario_id=actor_id,
    )

    return producto