import enum
from datetime import datetime
from sqlalchemy import String, Numeric, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.models import *

from app.core.database import Base



class EstadoVenta(str, enum.Enum):
    confirmada = "confirmada"
    cancelada = "cancelada"


class Venta(Base):
    __tablename__ = "ventas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    numero_factura: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"))
    fecha_venta: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    total: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    estado: Mapped[EstadoVenta] = mapped_column(Enum(EstadoVenta), default=EstadoVenta.confirmada)

    # Relationships
    cliente: Mapped["Cliente"] = relationship(back_populates="ventas")
    detalles: Mapped[list["DetalleVenta"]] = relationship(back_populates="venta", cascade="all, delete-orphan")


class DetalleVenta(Base):
    __tablename__ = "detalles_venta"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    venta_id: Mapped[int] = mapped_column(ForeignKey("ventas.id"))
    producto_id: Mapped[int] = mapped_column(ForeignKey("productos.id"))
    cantidad: Mapped[int] = mapped_column(Integer)
    precio_unitario: Mapped[float] = mapped_column(Numeric(12, 2))
    subtotal: Mapped[float] = mapped_column(Numeric(14, 2))

    # Relationships
    venta: Mapped["Venta"] = relationship(back_populates="detalles")
    producto: Mapped["Producto"] = relationship(back_populates="detalles_venta")
