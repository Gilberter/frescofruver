from __future__ import annotations

import enum
from datetime import date

from sqlalchemy import String, Integer, ForeignKey, Date, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class TipoMovimiento(str, enum.Enum):
    entrada = "Entrada"
    salida = "Salida"
    ajuste = "Ajuste"


class MovimientoInventario(Base):
    __tablename__ = "movimientoinventario"

    id: Mapped[int] = mapped_column("IdMovimiento", primary_key=True, autoincrement=True)
    fecha_movimiento: Mapped[date | None] = mapped_column("FechaMovimiento", Date, nullable=True)
    tipo_movimiento: Mapped[TipoMovimiento | None] = mapped_column(
        "TipoMovimiento",
        Enum(TipoMovimiento, values_callable=lambda x: [e.value for e in x], native_enum=False),
        nullable=True,
    )
    cantidad: Mapped[int | None] = mapped_column("Cantidad", Integer, nullable=True)
    motivo: Mapped[str | None] = mapped_column("Motivo", String(100), nullable=True)
    stock_resultante: Mapped[int | None] = mapped_column("StockResultante", Integer, nullable=True)
    producto_id: Mapped[int | None] = mapped_column("IdProducto", ForeignKey("productos.IdProducto"), nullable=True)
    usuario_id: Mapped[int | None] = mapped_column("IdUsuario", ForeignKey("usuario.IdUsuario"), nullable=True)

    producto: Mapped["Producto | None"] = relationship("Producto", back_populates="movimientos")
    usuario: Mapped["Usuario | None"] = relationship("Usuario", back_populates="movimientos")
