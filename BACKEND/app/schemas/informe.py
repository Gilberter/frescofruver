from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

# ── Informe de Ventas ─────────────────────────────────────────────────────

class FilaVentaTabular(BaseModel):
    """Fila individual del informe tabular de ventas"""
    numero_factura: str
    cliente: str
    fecha_venta: datetime
    cantidad_items: int
    subtotal: float
    total: float
    estado: str
    usuario: Optional[str] = None

class InformeVentasTabular(BaseModel):
    """Informe tabular completo de ventas"""
    periodo: str  # ej: "2026-04-01 a 2026-04-20"
    fecha_generacion: datetime
    cantidad_registros: int
    total_ingresos: float
    promedio_venta: float
    venta_maxima: float
    venta_minima: float
    ventas: list[FilaVentaTabular]

# ── Informe de Compras ─────────────────────────────────────────────────────

class FilaCompraTabular(BaseModel):
    """Fila individual del informe tabular de compras"""
    numero_orden: str
    proveedor: str
    fecha_orden: datetime
    cantidad_items: int
    subtotal: float
    total_orden: float
    estado: str
    usuario: Optional[str] = None

class InformeComprasTabular(BaseModel):
    """Informe tabular completo de compras"""
    periodo: str
    fecha_generacion: datetime
    cantidad_registros: int
    total_invertido: float
    promedio_orden: float
    orden_maxima: float
    orden_minima: float
    compras: list[FilaCompraTabular]

# ── Informe Consolidado ─────────────────────────────────────────────────────

class ResumenPeriodo(BaseModel):
    """Resumen de ventas y compras en el período"""
    periodo: str
    fecha_generacion: datetime
    
    # Ventas
    total_ventas: int
    total_ingresos: float
    promedio_venta: float
    
    # Compras
    total_compras: int
    total_invertido: float
    promedio_compra: float
    
    # Consolidado
    ganancia_bruta: float
    margen_porcentaje: float

class DetalleProductoConsolidado(BaseModel):
    """Detalles de producto en el informe consolidado"""
    nombre_producto: str
    cantidad_vendida: int
    cantidad_comprada: int
    ingresos_venta: float
    costo_compra: float
    ganancia: float
    stock_actual: int

class InformeConsolidado(BaseModel):
    """Informe consolidado: ventas + compras + análisis de productos"""
    resumen: ResumenPeriodo
    productos: list[DetalleProductoConsolidado]
    detalles_productos_top_5: list[DetalleProductoConsolidado]  # Top 5 por ganancia

# ── Opciones de Filtro ─────────────────────────────────────────────────────

class FiltrosInforme(BaseModel):
    """Filtros para los informes"""
    fecha_inicio: datetime = Field(..., description="Fecha inicial del período")
    fecha_fin: datetime = Field(..., description="Fecha final del período")
    cliente_id: Optional[int] = None
    proveedor_id: Optional[int] = None
    estado: Optional[str] = None