from __future__ import annotations

import enum
from datetime import date

from sqlalchemy import String, Float, Integer, ForeignKey, Date, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class EstadoVenta(str, enum.Enum):
    completada = "Completada"
    pendiente = "Pendiente"
    cancelada = "Cancelada"


class Venta(Base):
    """Mapea la tabla `ventas` del dump SQL."""

    __tablename__ = "ventas"

    id: Mapped[int] = mapped_column("IdVenta", primary_key=True, autoincrement=True)
    numero_factura: Mapped[str | None] = mapped_column("NumeroFactura", String(50), nullable=True, unique=True, index=True)
    fecha_venta: Mapped[date | None] = mapped_column("FechaVenta", Date, nullable=True)
    total: Mapped[float | None] = mapped_column("TotalVenta", Float, nullable=True)
    estado: Mapped[EstadoVenta | None] = mapped_column(
        "EstadoVenta",
        Enum(EstadoVenta, values_callable=lambda x: [e.value for e in x], native_enum=False),
        nullable=True,
        default=EstadoVenta.completada,
    )
    canal_venta: Mapped[str | None] = mapped_column("CanalVenta", String(50), nullable=True, default="Tienda")
    cliente_id: Mapped[int | None] = mapped_column("IdCliente", ForeignKey("cliente.IdCliente"), nullable=True)
    usuario_id: Mapped[int | None] = mapped_column("IdUsuario", ForeignKey("usuario.IdUsuario"), nullable=True)

    cliente: Mapped["Cliente | None"] = relationship("Cliente", back_populates="ventas")
    usuario: Mapped["Usuario | None"] = relationship("Usuario", back_populates="ventas")
    detalles: Mapped[list["DetalleVenta"]] = relationship(
        back_populates="venta",
        cascade="all, delete-orphan",
    )


class DetalleVenta(Base):
    __tablename__ = "detalleventa"

    id: Mapped[int] = mapped_column("IdDetalleVenta", primary_key=True, autoincrement=True)
    venta_id: Mapped[int | None] = mapped_column("IdVenta", ForeignKey("ventas.IdVenta"), nullable=True)
    producto_id: Mapped[int | None] = mapped_column("IdProducto", ForeignKey("productos.IdProducto"), nullable=True)
    cantidad: Mapped[int | None] = mapped_column("Cantidad", Integer, nullable=True)
    precio_unitario: Mapped[float | None] = mapped_column("PrecioUnitario", Float, nullable=True)
    subtotal: Mapped[float | None] = mapped_column("Subtotal", Float, nullable=True)

    venta: Mapped["Venta"] = relationship(back_populates="detalles")
    producto: Mapped["Producto | None"] = relationship("Producto", back_populates="detalles_venta")
