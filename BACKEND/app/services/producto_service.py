from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud import producto as crud_producto
from app.crud import inventario as crud_inventario
from app.crud import auditoria as crud_auditoria
from app.models.producto import Producto
from app.models.inventario import TipoMovimiento
from app.schemas.producto import ProductoCreate, ProductoUpdate, AjusteInventarioIn


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
    if data.precio_venta and data.precio_venta != producto.precio_venta:
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


def ajuste_manual(db: Session, producto_id: int, data: AjusteInventarioIn, actor_id: int) -> Producto:
    producto = crud_producto.get_by_id(db, producto_id)
    if not producto:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

    nuevo_stock = producto.stock_actual + data.cantidad
    if nuevo_stock < 0:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Stock insuficiente. Stock actual: {producto.stock_actual}",
        )

    crud_producto.adjust_stock(db, producto, data.cantidad)
    crud_inventario.registrar_movimiento(
        db,
        producto_id=producto_id,
        usuario_id=actor_id,
        tipo=TipoMovimiento.ajuste,
        cantidad=data.cantidad,
        stock_resultante=nuevo_stock,
        motivo=data.motivo,
    )
    crud_auditoria.registrar(
        db,
        accion="ajuste_inventario",
        descripcion=f"Producto id={producto_id}: ajuste {data.cantidad} | motivo: {data.motivo}",
        usuario_id=actor_id,
    )
    return producto
