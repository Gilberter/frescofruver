from sqlalchemy import String, Numeric, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

from app.core.database import Base
from app.models import *


class EstadoOrden(str, enum.Enum):
    pendiente = "pendiente"
    recibida = "recibida"
    parcial = "parcial"
    cancelada = "cancelada"


class Proveedor(Base):
    __tablename__ = "proveedores"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(150))
    telefono: Mapped[str | None] = mapped_column(String(20))
    correo: Mapped[str | None] = mapped_column(String(100))
    direccion: Mapped[str | None] = mapped_column(String(255))
    estado: Mapped[str] = mapped_column(String(10), default="activo")


    # Relationships
    ordenes: Mapped[list["OrdenCompra"]] = relationship(back_populates="proveedor")


class OrdenCompra(Base):
    __tablename__ = "ordenes_compra"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    proveedor_id: Mapped[int] = mapped_column(ForeignKey("proveedores.id"))
    fecha_orden: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    estado_orden: Mapped[EstadoOrden] = mapped_column(Enum(EstadoOrden), default=EstadoOrden.pendiente)
    total_orden: Mapped[float] = mapped_column(Numeric(14, 2), default=0)

    # Relationships
    proveedor: Mapped["Proveedor"] = relationship(back_populates="ordenes")
    detalles: Mapped[list["DetalleCompra"]] = relationship(back_populates="orden", cascade="all, delete-orphan")


class DetalleCompra(Base):
    __tablename__ = "detalles_compra"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    orden_id: Mapped[int] = mapped_column(ForeignKey("ordenes_compra.id"))
    producto_id: Mapped[int] = mapped_column(ForeignKey("productos.id"))
    cantidad: Mapped[int] = mapped_column(Integer)
    precio_costo: Mapped[float] = mapped_column(Numeric(12, 2))
    subtotal: Mapped[float] = mapped_column(Numeric(14, 2))

    # Relationships
    orden: Mapped["OrdenCompra"] = relationship(back_populates="detalles")
    producto: Mapped["Producto"] = relationship(back_populates="detalles_compra")
