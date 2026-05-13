from __future__ import annotations

import enum
from datetime import date

from sqlalchemy import String, Float, Integer, ForeignKey, Date, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.schemas import *
from app.core.database import Base
from app.models import *



class OrdenCompra(Base):
    __tablename__ = "ordencompra"

    id: Mapped[int] = mapped_column("IdOrdenCompra", primary_key=True, autoincrement=True)
    fecha_orden: Mapped[date] = mapped_column("FechaOrden", Date, nullable=True)
    estado_orden: Mapped[EstadoOrden | None] = mapped_column(
        "EstadoOrden",
        Enum(EstadoOrden, values_callable=lambda x: [e.value for e in x], native_enum=False),
        nullable=True,
        default=EstadoOrden.pendiente,
    )
    total_orden: Mapped[float] = mapped_column("TotalOrden", Float, nullable=True)
    proveedor_id: Mapped[int] = mapped_column("IdProv", ForeignKey("proveedores.IdProv"), nullable=True)

    usuario_id: Mapped[int] = mapped_column(
        "IdUsuario",
        ForeignKey("usuario.IdUsuario"),
        nullable=False
    )   
    
    usuario: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="ordenes_compra"
    )
    proveedor: Mapped["Proveedor"] = relationship("Proveedor", back_populates="ordenes")
    detalles: Mapped[list["DetalleOrdenCompra"]] = relationship(
        "DetalleOrdenCompra",
        back_populates="orden",
        cascade="all, delete-orphan",
    )


class DetalleOrdenCompra(Base):
    __tablename__ = "detallecompra"

    id: Mapped[int] = mapped_column("IdDetalleCompra", primary_key=True, autoincrement=True)
    orden_id: Mapped[int] = mapped_column("IdOrdenCompra", ForeignKey("ordencompra.IdOrdenCompra"))

    producto_id: Mapped[int] = mapped_column("IdProducto", ForeignKey("productos.IdProducto"))
    cantidad: Mapped[int] = mapped_column("Cantidad", Integer)
    precio_unitario: Mapped[float] = mapped_column("PrecioCosto", Float)
    subtotal: Mapped[float] = mapped_column("Subtotal", Float)

    orden: Mapped["OrdenCompra"] = relationship("OrdenCompra", back_populates="detalles")
    producto: Mapped["Producto"] = relationship("Producto", back_populates="detalles_compra")
