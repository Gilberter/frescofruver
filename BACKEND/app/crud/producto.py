from sqlalchemy.orm import Session

from app.models.producto import Producto, CategoriaProducto
from app.schemas.producto import ProductoCreate, ProductoUpdate


def get_by_id(db: Session, producto_id: int) -> Producto | None:
    return db.get(Producto, producto_id)


def list_all(db: Session, categoria: CategoriaProducto | None = None) -> list[Producto]:
    q = db.query(Producto)
    if categoria:
        q = q.filter(Producto.categoria == categoria)
    return q.all()


def list_bajo_stock(db: Session) -> list[Producto]:
    return (
        db.query(Producto)
        .filter(Producto.stock_actual <= Producto.stock_minimo, Producto.estado == "activo")
        .all()
    )


def create(db: Session, data: ProductoCreate) -> Producto:
    producto = Producto(**data.model_dump())
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
    """Apply *delta* (positive or negative) to stock_actual.
    Caller is responsible for validating no negative stock.
    """
    producto.stock_actual += delta
    db.commit()
    db.refresh(producto)
    return producto
