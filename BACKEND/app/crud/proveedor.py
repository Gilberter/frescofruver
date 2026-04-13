from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.proveedor import Proveedor, OrdenCompra, DetalleCompra, EstadoOrden
from app.schemas.proveedor import ProveedorCreate, ProveedorUpdate


# ── Proveedor ─────────────────────────────────────────────────────────────────

def get_by_id(db: Session, proveedor_id: int) -> Proveedor | None:
    return db.get(Proveedor, proveedor_id)


def list_all(db: Session) -> list[Proveedor]:
    return db.query(Proveedor).all()


def create(db: Session, data: ProveedorCreate) -> Proveedor:
    proveedor = Proveedor(**data.model_dump())
    db.add(proveedor)
    db.commit()
    db.refresh(proveedor)
    return proveedor


def update(db: Session, proveedor: Proveedor, data: ProveedorUpdate) -> Proveedor:
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(proveedor, field, value)
    db.commit()
    db.refresh(proveedor)
    return proveedor


def get_perfil_stats(db: Session, proveedor_id: int) -> dict:
    total_ordenes = (
        db.query(func.count(OrdenCompra.id))
        .filter(OrdenCompra.proveedor_id == proveedor_id)
        .scalar()
        or 0
    )
    monto_total = (
        db.query(func.sum(OrdenCompra.total_orden))
        .filter(
            OrdenCompra.proveedor_id == proveedor_id,
            OrdenCompra.estado_orden == EstadoOrden.recibida,
        )
        .scalar()
        or 0.0
    )
    return {"total_ordenes": total_ordenes, "monto_total_invertido": float(monto_total)}


# ── Orden de Compra ───────────────────────────────────────────────────────────

def get_orden_by_id(db: Session, orden_id: int) -> OrdenCompra | None:
    return db.get(OrdenCompra, orden_id)


def list_ordenes(
    db: Session,
    proveedor_id: int | None = None,
    estado: EstadoOrden | None = None,
) -> list[OrdenCompra]:
    q = db.query(OrdenCompra)
    if proveedor_id:
        q = q.filter(OrdenCompra.proveedor_id == proveedor_id)
    if estado:
        q = q.filter(OrdenCompra.estado_orden == estado)
    return q.order_by(OrdenCompra.fecha_orden.desc()).all()


def create_orden_with_detalles(
    db: Session,
    orden: OrdenCompra,
    detalles: list[DetalleCompra],
) -> OrdenCompra:
    db.add(orden)
    db.flush()
    for d in detalles:
        d.orden_id = orden.id
        db.add(d)
    db.commit()
    db.refresh(orden)
    return orden


def update_estado_orden(db: Session, orden: OrdenCompra, estado: EstadoOrden) -> OrdenCompra:
    orden.estado_orden = estado
    db.commit()
    db.refresh(orden)
    return orden
