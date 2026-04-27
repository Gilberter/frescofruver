from __future__ import annotations

from datetime import date
from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Auditoria(Base):
    """Mapea la tabla `auditoria` del dump `DATA/Database_FrescoFruver.sql`."""

    __tablename__ = "auditoria"

    id: Mapped[int] = mapped_column("IdAuditoria", primary_key=True, autoincrement=True)
    usuario_id: Mapped[int | None] = mapped_column(
        "IdUsuario",
        ForeignKey("usuario.IdUsuario"),
        nullable=True,
    )
    fecha_auditoria: Mapped[date | None] = mapped_column(
        "FechaAuditoria",
        Date,
        server_default=func.current_date(),
        nullable=True,
    )
    accion: Mapped[str] = mapped_column("Accion", String(100))
    descripcion: Mapped[str | None] = mapped_column("Descripcion", String(255))

    usuario: Mapped["Usuario | None"] = relationship("Usuario", back_populates="auditorias")
