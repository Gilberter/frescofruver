from __future__ import annotations

import enum
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class RolUsuario(str, enum.Enum):
    vendedor = "Vendedor"
    administrador = "Administrador"
    dueno = "Dueño"


class Usuario(Base):
    """Mapea la tabla `usuario` del dump `DATA/Database_FrescoFruver.sql`."""

    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column("IdUsuario", primary_key=True, autoincrement=True)
    nombre_completo: Mapped[str | None] = mapped_column("NomUsuario", String(100), nullable=True)
    no_documento: Mapped[str | None] = mapped_column(
        "NoDocumentoUsuario", String(50), nullable=True, index=True
    )
    username: Mapped[str | None] = mapped_column("Username", String(50), nullable=True, unique=True, index=True)
    password: Mapped[str] = mapped_column("Password", String(255))
    telefono: Mapped[str | None] = mapped_column("TelUsuario", String(20), nullable=True)
    correo: Mapped[str | None] = mapped_column("CorreoUsuario", String(100), nullable=True)
    rol: Mapped[RolUsuario] = mapped_column(
        "RolUsuario",
        Enum(
            RolUsuario,
            native_enum=False,
            values_callable=lambda enum_cls: [item.value for item in enum_cls],
        ),
        default=RolUsuario.vendedor,
    )
    estado: Mapped[str | None] = mapped_column("Estado", String(20), nullable=True)

    auditorias: Mapped[list["Auditoria"]] = relationship("Auditoria", back_populates="usuario")
    movimientos: Mapped[list["MovimientoInventario"]] = relationship(
        "MovimientoInventario",
        back_populates="usuario",
    )
    ventas: Mapped[list["Venta"]] = relationship("Venta", back_populates="usuario")