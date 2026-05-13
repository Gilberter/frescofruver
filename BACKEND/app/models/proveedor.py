from __future__ import annotations

import enum
from datetime import date

from sqlalchemy import String, Float, Integer, ForeignKey, Date, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models import *
from app.core.database import Base





class Proveedor(Base):
    """Mapea la tabla `proveedores` del dump SQL."""

    __tablename__ = "proveedores"

    id: Mapped[int] = mapped_column("IdProv", primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column("NomProv", String(100), nullable=True)
    telefono: Mapped[str] = mapped_column("TelProv", String(20), nullable=True)
    direccion: Mapped[str] = mapped_column("DirProv", String(150), nullable=True)
    correo: Mapped[str] = mapped_column("CorreoProv", String(100), nullable=True)
    estado: Mapped[str] = mapped_column("EstadoProv", String(20), nullable=True, default="Activo")

    ordenes: Mapped[list["OrdenCompra"]] = relationship("OrdenCompra", back_populates="proveedor")

