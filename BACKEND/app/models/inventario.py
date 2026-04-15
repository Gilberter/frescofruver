import enum
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models import *


class TipoMovimiento(str, enum.Enum):
    pedido = "pedido"       # salida por venta
    compra = "compra"       # entrada por orden de compra
    ajuste = "ajuste"       # ajuste manual


class MovimientoInventario(Base):
    __tablename__ = "movimientos_inventario"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    producto_id: Mapped[int] = mapped_column(ForeignKey("productos.id"))
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    fecha_movimiento: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    tipo_movimiento: Mapped[TipoMovimiento] = mapped_column(Enum(TipoMovimiento))
    cantidad: Mapped[int] = mapped_column(Integer)   # positive = entrada, negative = salida
    motivo: Mapped[str | None] = mapped_column(String(255))
    stock_resultante: Mapped[int] = mapped_column(Integer)

    # Relationships
    producto: Mapped["Producto"] = relationship(back_populates="movimientos")
    usuario: Mapped["Usuario"] = relationship(back_populates="movimientos")
