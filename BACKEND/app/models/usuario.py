import enum
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models import *


class RolUsuario(str, enum.Enum):
    vendedor = "Vendedor"
    administrador = "Administrador"
    dueno = "Dueño"


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre_completo: Mapped[str] = mapped_column(String(150))
    no_documento: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(60), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))
    rol: Mapped[RolUsuario] = mapped_column(Enum(RolUsuario), default=RolUsuario.vendedor)
    estado: Mapped[str] = mapped_column(String(10), default="activo")  # activo | inactivo

    # Relationships
    auditorias: Mapped[list["Auditoria"]] = relationship(back_populates="usuario")
    movimientos: Mapped[list["MovimientoInventario"]] = relationship(back_populates="usuario")
