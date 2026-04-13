from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Auditoria(Base):
    __tablename__ = "auditorias"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    usuario_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"), nullable=True)
    fecha_auditoria: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    accion: Mapped[str] = mapped_column(String(100))
    descripcion: Mapped[str | None] = mapped_column(Text)

    # Relationships
    usuario: Mapped["Usuario | None"] = relationship(back_populates="auditorias")
