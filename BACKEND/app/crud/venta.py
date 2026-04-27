import re
from sqlalchemy.orm import Session

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
    """Genera el siguiente número FAC-NNN alineado con el dump (FAC-001, …)."""
    rows = db.query(Venta.numero_factura).all()
    nums: list[int] = []
    for (nf,) in rows:
        if not nf:
            continue
        m = re.match(r"^FAC-(\d+)$", nf.strip(), re.I)
        if m:
            nums.append(int(m.group(1)))
    n = max(nums) + 1 if nums else 1
    return f"FAC-{n:03d}"


def create_with_detalles(
    db: Session,
    venta: Venta,
    detalles: list[DetalleVenta],
) -> Venta:
    db.add(venta)
    db.flush()
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
