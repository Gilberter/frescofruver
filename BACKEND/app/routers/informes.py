from fastapi import APIRouter, Query, status
from datetime import datetime, timedelta
from app.core.deps import DBSession, AnyRole
from app.services import informe_service
from app.schemas.informe import (
    InformeVentasTabular,
    InformeComprasTabular,
    InformeConsolidado,
)

router = APIRouter(prefix="/informes", tags=["Informes Tabulares"])


@router.get("/ventas", response_model=InformeVentasTabular, dependencies=[AnyRole])
def obtener_informe_ventas(
    db: DBSession,
    fecha_inicio: datetime = Query(
        ...,
        description="Fecha inicio (ISO format: 2026-04-01T00:00:00)",
    ),
    fecha_fin: datetime = Query(
        ...,
        description="Fecha fin (ISO format: 2026-04-30T23:59:59)",
    ),
    cliente_id: int | None = Query(None, description="Filtrar por cliente ID"),
    estado: str | None = Query(None, description="Filtrar por estado (confirmada/cancelada)"),
):
    """
    Obtiene informe tabular de ventas en el período especificado.
    
    **Parámetros:**
    - `fecha_inicio`: Fecha inicial (ISO format)
    - `fecha_fin`: Fecha final (ISO format)
    - `cliente_id`: (Opcional) Filtrar por cliente
    - `estado`: (Opcional) Filtrar por estado
    
    **Retorna:** Tabla de ventas con métricas agregadas
    """
    return informe_service.obtener_informe_ventas(
        db, fecha_inicio, fecha_fin, cliente_id, estado
    )


@router.get("/compras", response_model=InformeComprasTabular, dependencies=[AnyRole])
def obtener_informe_compras(
    db: DBSession,
    fecha_inicio: datetime = Query(...),
    fecha_fin: datetime = Query(...),
    proveedor_id: int | None = Query(None, description="Filtrar por proveedor ID"),
    estado: str | None = Query(None, description="Filtrar por estado"),
):
    """
    Obtiene informe tabular de compras en el período especificado.
    
    **Parámetros:**
    - `fecha_inicio`: Fecha inicial (ISO format)
    - `fecha_fin`: Fecha final (ISO format)
    - `proveedor_id`: (Opcional) Filtrar por proveedor
    - `estado`: (Opcional) Filtrar por estado
    
    **Retorna:** Tabla de compras con métricas agregadas
    """
    return informe_service.obtener_informe_compras(
        db, fecha_inicio, fecha_fin, proveedor_id, estado
    )


@router.get("/consolidado", response_model=InformeConsolidado, dependencies=[AnyRole])
def obtener_informe_consolidado(
    db: DBSession,
    fecha_inicio: datetime = Query(
        ...,
        description="Fecha inicio del período",
    ),
    fecha_fin: datetime = Query(
        ...,
        description="Fecha fin del período",
    ),
):
    """
    Obtiene informe consolidado (ventas + compras + análisis por producto).
    
    **Incluye:**
    - Resumen de ventas y compras
    - Ganancia bruta y margen porcentual
    - Detalles por producto (ventas vs compras)
    - Top 5 productos por ganancia
    
    **Parámetros:**
    - `fecha_inicio`: Fecha inicial (ISO format)
    - `fecha_fin`: Fecha final (ISO format)
    
    **Retorna:** Informe consolidado completo
    """
    return informe_service.obtener_informe_consolidado(
        db, fecha_inicio, fecha_fin
    )


# Endpoint auxiliar: obtener período predeterminado (último mes)
@router.get("/ultimo-mes", response_model=InformeConsolidado, dependencies=[AnyRole])
def obtener_informe_ultimo_mes(db: DBSession):
    """
    Obtiene informe consolidado del último mes completo.
    Útil para consultas rápidas sin especificar fechas.
    """
    ahora = datetime.now()
    fecha_fin = ahora.replace(day=1) - timedelta(days=1)
    fecha_inicio = fecha_fin.replace(day=1)
    
    return informe_service.obtener_informe_consolidado(
        db, fecha_inicio, fecha_fin
    )