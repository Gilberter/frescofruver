import enum
from sqlalchemy import String, Numeric, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class CategoriaProducto(str, enum.Enum):
    fruta = "fruta"
    verdura = "verdura"


class UnidadMedida(str, enum.Enum):
    kg = "kg"
    libra = "libra"
    unidad = "unidad"


class Producto(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), index=True)
    categoria: Mapped[CategoriaProducto] = mapped_column(Enum(CategoriaProducto))
    unidad_medida: Mapped[UnidadMedida] = mapped_column(Enum(UnidadMedida))
    precio_compra: Mapped[float] = mapped_column(Numeric(12, 2))
    precio_venta: Mapped[float] = mapped_column(Numeric(12, 2))
    stock_actual: Mapped[int] = mapped_column(Integer, default=0)
    stock_minimo: Mapped[int] = mapped_column(Integer, default=0)
    estado: Mapped[str] = mapped_column(String(10), default="activo")

    # Relationships
    detalles_venta: Mapped[list["DetalleVenta"]] = relationship(back_populates="producto")
    detalles_compra: Mapped[list["DetalleCompra"]] = relationship(back_populates="producto")
    movimientos: Mapped[list["MovimientoInventario"]] = relationship(back_populates="producto")
