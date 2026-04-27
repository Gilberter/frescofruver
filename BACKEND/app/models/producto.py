from __future__ import annotations

from datetime import date

from sqlalchemy import String, Integer, Float, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

# La BD del dump no incluye stock mínimo; umbral fijo para alertas (RF-07).
BAJO_STOCK_UMBRAL = 70


class Producto(Base):
    """Mapea la tabla `productos` de `DATA/Database_FrescoFruver.sql`."""

    __tablename__ = "productos"

    id: Mapped[int] = mapped_column("IdProducto", primary_key=True, autoincrement=True)
    nombre: Mapped[str | None] = mapped_column("NomProd", String(100), nullable=True, index=True)
    precio_compra: Mapped[float | None] = mapped_column("PrecioCompraProd", Float, nullable=True)
    precio_venta: Mapped[float | None] = mapped_column("PrecioVentaProd", Float, nullable=True)
    stock_actual: Mapped[int | None] = mapped_column("StockActualProd", Integer, nullable=True, default=0)
    fecha_vencimiento: Mapped[date | None] = mapped_column("FechaVencimientoProd", Date, nullable=True)
    categoria: Mapped[str | None] = mapped_column("CategoriaProd", String(50), nullable=True, index=True)
    estado: Mapped[str | None] = mapped_column("EstadoProd", String(20), nullable=True, default="Activo")

    detalles_venta: Mapped[list["DetalleVenta"]] = relationship("DetalleVenta", back_populates="producto")
    detalles_compra: Mapped[list["DetalleCompra"]] = relationship("DetalleCompra", back_populates="producto")
    movimientos: Mapped[list["MovimientoInventario"]] = relationship(
        "MovimientoInventario",
        back_populates="producto",
    )
