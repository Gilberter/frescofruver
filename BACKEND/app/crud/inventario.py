from datetime import date

from sqlalchemy.orm import Session

from app.models.inventario import MovimientoInventario, TipoMovimiento


def registrar_movimiento(
    db: Session,
    producto_id: int,
    usuario_id: int,
    tipo: TipoMovimiento,
    cantidad: int,
    stock_resultante: int,
    motivo: str | None = None,
) -> MovimientoInventario:
    mov = MovimientoInventario(
        fecha_movimiento=date.today(),
        producto_id=producto_id,
        usuario_id=usuario_id,
        tipo_movimiento=tipo,
        cantidad=cantidad,
        stock_resultante=stock_resultante,
        motivo=motivo,
    )
    db.add(mov)
    db.commit()
    db.refresh(mov)
    return mov


def list_by_producto(db: Session, producto_id: int) -> list[MovimientoInventario]:
    return (
        db.query(MovimientoInventario)
        .filter(MovimientoInventario.producto_id == producto_id)
        .order_by(MovimientoInventario.fecha_movimiento.desc())
        .all()
    )


def list_all(db: Session) -> list[MovimientoInventario]:
    return db.query(MovimientoInventario).order_by(MovimientoInventario.fecha_movimiento.desc()).all()
