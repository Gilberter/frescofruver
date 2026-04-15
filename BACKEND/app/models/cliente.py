from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

from app.models import *

class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre_completo: Mapped[str] = mapped_column(String(150))
    no_documento: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    telefono: Mapped[str | None] = mapped_column(String(20))
    direccion: Mapped[str | None] = mapped_column(String(255))
    estado: Mapped[str] = mapped_column(String(10), default="activo")

    # Relationships
    ventas: Mapped[list["Venta"]] = relationship(back_populates="cliente")
