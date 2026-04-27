from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Cliente(Base):
    """Mapea la tabla `cliente` de `DATA/Database_FrescoFruver.sql`."""

    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column("IdCliente", primary_key=True, autoincrement=True)
    nombre_completo: Mapped[str | None] = mapped_column("NomCliente", String(100), nullable=True)
    no_documento: Mapped[str | None] = mapped_column(
        "NoDocumentoCliente", String(50), nullable=True, index=True
    )
    telefono: Mapped[str | None] = mapped_column("TelCliente", String(20), nullable=True)
    correo: Mapped[str | None] = mapped_column("CorreoCliente", String(100), nullable=True)
    direccion: Mapped[str | None] = mapped_column("DireccionCliente", String(150), nullable=True)
    estado: Mapped[str | None] = mapped_column("EstadoCliente", String(20), nullable=True)

    ventas: Mapped[list["Venta"]] = relationship("Venta", back_populates="cliente")
    ordenes_compra: Mapped[list["OrdenCompra"]] = relationship("OrdenCompra", back_populates="cliente")
