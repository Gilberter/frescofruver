from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.venta import Venta, DetalleVenta


def get_by_id(db: Session, venta_id: int) -> Venta | None:
    return db.get(Venta, venta_id)


def get_by_factura(db: Session, numero_factura: str) -> Venta | None:
    return db.query(Venta).filter(Venta.numero_factura == numero_factura).first()


def list_all(db: Session) -> list[Venta]:
    return db.query(Venta).order_by(Venta.fecha_venta.desc()).all()


def list_by_cliente(db: Session, cliente_id: int) -> list[Venta]:
    return (
        db.query(Venta)
        .filter(Venta.cliente_id == cliente_id)
        .order_by(Venta.fecha_venta.desc())
        .all()
    )


def next_factura_number(db: Session) -> str:
    """Generate next sequential invoice number: F-0001, F-0002 …"""
    count = db.query(func.count(Venta.id)).scalar() or 0
    return f"F-{count + 1:04d}"


def create_with_detalles(
    db: Session,
    venta: Venta,
    detalles: list[DetalleVenta],
) -> Venta:
    db.add(venta)
    db.flush()  # get venta.id before adding details
    for d in detalles:
        d.venta_id = venta.id
        db.add(d)
    db.commit()
    db.refresh(venta)
    return venta


def cancel(db: Session, venta: Venta) -> Venta:
    from app.models.venta import EstadoVenta
    venta.estado = EstadoVenta.cancelada
    db.commit()
    db.refresh(venta)
    return venta
