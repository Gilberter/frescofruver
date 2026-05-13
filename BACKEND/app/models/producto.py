from __future__ import annotations

from datetime import date


from sqlalchemy import String, Integer, Float, Date, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models import *
from app.schemas import *
from app.core.database import Base




class Producto(Base):
    """Mapea la tabla `productos` de `DATA/Database_FrescoFruver.sql`."""

    __tablename__ = "productos"

    id: Mapped[int] = mapped_column("IdProducto", primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column("NomProd", String(100), nullable=True, index=True)
    precio_compra: Mapped[float] = mapped_column("PrecioCompraProd", Float, nullable=True)
    precio_venta: Mapped[float] = mapped_column("PrecioVentaProd", Float, nullable=True)
    stock_actual: Mapped[int] = mapped_column("StockActualProd", Integer, nullable=True, default=0)
    fecha_vencimiento: Mapped[date] = mapped_column("FechaVencimientoProd", Date, nullable=True)
    categoria: Mapped[str] = mapped_column("CategoriaProd", String(50), nullable=True, index=True)
    estado: Mapped[EstadoProducto] = mapped_column(
        "EstadoProd",
        Enum(EstadoProducto, values_callable=lambda x: [e.value for e in x], native_enum=False),
        nullable=True,
        default=EstadoProducto.Activo,
    )

    detalles_venta: Mapped[list["DetalleVenta"]] = relationship("DetalleVenta", back_populates="producto")
    detalles_compra: Mapped[list["DetalleOrdenCompra"]] = relationship("DetalleOrdenCompra", back_populates="producto")
    movimientos: Mapped[list["MovimientoInventario"]] = relationship(
        "MovimientoInventario",
        back_populates="producto",
    )
