from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.producto import Producto, BAJO_STOCK_UMBRAL
from app.schemas.producto import ProductoCreate, ProductoUpdate


def get_by_id(db: Session, producto_id: int) -> Producto | None:
    return db.get(Producto, producto_id)


def list_all(db: Session, categoria: str | None = None) -> list[Producto]:
    q = db.query(Producto)
    if categoria:
        q = q.filter(Producto.categoria == categoria)
    return q.all()


def list_bajo_stock(db: Session) -> list[Producto]:
    """Productos con stock por debajo del umbral (la BD no tiene stock mínimo)."""
    return (
        db.query(Producto)
        .filter(
            Producto.stock_actual.isnot(None),
            Producto.stock_actual < BAJO_STOCK_UMBRAL,
            or_(
                func.lower(func.trim(Producto.estado)) == "activo",
                Producto.estado.is_(None),
            ),
        )
        .all()
    )


def create(db: Session, data: ProductoCreate) -> Producto:
    producto = Producto(
        nombre=data.nombre,
        categoria=data.categoria,
        precio_compra=data.precio_compra,
        precio_venta=data.precio_venta,
        stock_actual=data.stock_actual,
        fecha_vencimiento=data.fecha_vencimiento,
        estado=data.estado,
    )
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto


def update(db: Session, producto: Producto, data: ProductoUpdate) -> Producto:
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(producto, field, value)
    db.commit()
    db.refresh(producto)
    return producto


def adjust_stock(db: Session, producto: Producto, delta: int) -> Producto:
    """Aplica *delta* al stock actual."""
    base = producto.stock_actual or 0
    producto.stock_actual = base + delta
    db.commit()
    db.refresh(producto)
    return producto
