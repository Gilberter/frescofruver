from __future__ import annotations

import enum
from datetime import date

from sqlalchemy import String, Float, Integer, ForeignKey, Date, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class EstadoOrden(str, enum.Enum):
    pendiente = "Pendiente"
    completada = "Completada"
    cancelada = "Cancelada"


class Proveedor(Base):
    """Mapea la tabla `proveedores` del dump SQL."""

    __tablename__ = "proveedores"

    id: Mapped[int] = mapped_column("IdProv", primary_key=True, autoincrement=True)
    nombre: Mapped[str | None] = mapped_column("NomProv", String(100), nullable=True)
    telefono: Mapped[str | None] = mapped_column("TelProv", String(20), nullable=True)
    direccion: Mapped[str | None] = mapped_column("DirProv", String(150), nullable=True)
    correo: Mapped[str | None] = mapped_column("CorreoProv", String(100), nullable=True)
    estado: Mapped[str | None] = mapped_column("EstadoProv", String(20), nullable=True, default="Activo")

    ordenes: Mapped[list["OrdenCompra"]] = relationship("OrdenCompra", back_populates="proveedor")


class OrdenCompra(Base):
    __tablename__ = "ordencompra"

    id: Mapped[int] = mapped_column("IdOrdenCompra", primary_key=True, autoincrement=True)
    fecha_orden: Mapped[date | None] = mapped_column("FechaOrden", Date, nullable=True)
    estado_orden: Mapped[EstadoOrden | None] = mapped_column(
        "EstadoOrden",
        Enum(EstadoOrden, values_callable=lambda x: [e.value for e in x], native_enum=False),
        nullable=True,
        default=EstadoOrden.pendiente,
    )
    total_orden: Mapped[float | None] = mapped_column("TotalOrden", Float, nullable=True)
    proveedor_id: Mapped[int | None] = mapped_column("IdProv", ForeignKey("proveedores.IdProv"), nullable=True)
    cliente_id: Mapped[int | None] = mapped_column("IdCliente", ForeignKey("cliente.IdCliente"), nullable=True)

    proveedor: Mapped["Proveedor | None"] = relationship("Proveedor", back_populates="ordenes")
    cliente: Mapped["Cliente | None"] = relationship("Cliente", back_populates="ordenes_compra")
    detalles: Mapped[list["DetalleCompra"]] = relationship(
        "DetalleCompra",
        back_populates="orden",
        cascade="all, delete-orphan",
    )


class DetalleCompra(Base):
    __tablename__ = "detallecompra"

    id: Mapped[int] = mapped_column("IdDetalleCompra", primary_key=True, autoincrement=True)
    orden_id: Mapped[int | None] = mapped_column("IdOrdenCompra", ForeignKey("ordencompra.IdOrdenCompra"), nullable=True)
    producto_id: Mapped[int | None] = mapped_column("IdProducto", ForeignKey("productos.IdProducto"), nullable=True)
    cantidad: Mapped[int | None] = mapped_column("Cantidad", Integer, nullable=True)
    precio_costo: Mapped[float | None] = mapped_column("PrecioCosto", Float, nullable=True)
    subtotal: Mapped[float | None] = mapped_column("Subtotal", Float, nullable=True)

    orden: Mapped["OrdenCompra"] = relationship("OrdenCompra", back_populates="detalles")
    producto: Mapped["Producto | None"] = relationship("Producto", back_populates="detalles_compra")
