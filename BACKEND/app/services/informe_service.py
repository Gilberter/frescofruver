from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.crud import venta as crud_venta
from app.crud import proveedor as crud_proveedor
from app.crud import producto as crud_producto
from app.models.venta import Venta, DetalleVenta, EstadoVenta
from app.models.proveedor import OrdenCompra, DetalleCompra, EstadoOrden
from app.models.producto import Producto
from app.models.proveedor import OrdenCompra, DetalleCompra, EstadoOrden
from app.schemas.informe import (
    FilaVentaTabular,
    InformeVentasTabular,
    FilaCompraTabular,
    InformeComprasTabular,
    ResumenPeriodo,
    DetalleProductoConsolidado,
    InformeConsolidado,
)


def _format_fecha(fecha: datetime) -> str:
    """Formatea fecha a string"""
    return fecha.strftime("%Y-%m-%d %H:%M:%S") if fecha else ""


def obtener_informe_ventas(
    db: Session,
    fecha_inicio: datetime,
    fecha_fin: datetime,
    cliente_id: int | None = None,
    estado: str | None = None,
) -> InformeVentasTabular:
    """
    Genera informe tabular de ventas en el período especificado
    """
    # Query base
    query = db.query(Venta).filter(
        Venta.fecha_venta >= fecha_inicio,
        Venta.fecha_venta <= fecha_fin,
    )
    
    # Filtros opcionales
    if cliente_id:
        query = query.filter(Venta.cliente_id == cliente_id)
    if estado:
        query = query.filter(Venta.estado == estado)
    
    ventas = query.all()
    
    # Construir filas del informe
    filas: list[FilaVentaTabular] = []
    totales = []
    
    for venta in ventas:
        cantidad_items = len(venta.detalles)
        subtotal = sum(d.subtotal for d in venta.detalles)
        
        filas.append(
            FilaVentaTabular(
                numero_factura=venta.numero_factura,
                cliente=venta.cliente.nombre_completo if venta.cliente else "N/A",
                fecha_venta=venta.fecha_venta,
                cantidad_items=cantidad_items,
                subtotal=subtotal,
                total=venta.total,
                estado=venta.estado.value,
                usuario=venta.cliente.nombre_completo,  # Puedes cambiar a usuario real si existe
            )
        )
        totales.append(venta.total)
    
    # Calcular métricas
    cantidad_registros = len(ventas)
    total_ingresos = sum(totales) if totales else 0.0
    promedio_venta = total_ingresos / cantidad_registros if cantidad_registros > 0 else 0.0
    venta_maxima = max(totales) if totales else 0.0
    venta_minima = min(totales) if totales else 0.0
    
    periodo = f"{_format_fecha(fecha_inicio)} a {_format_fecha(fecha_fin)}"
    
    return InformeVentasTabular(
        periodo=periodo,
        fecha_generacion=datetime.now(timezone.utc),
        cantidad_registros=cantidad_registros,
        total_ingresos=round(total_ingresos, 2),
        promedio_venta=round(promedio_venta, 2),
        venta_maxima=round(venta_maxima, 2),
        venta_minima=round(venta_minima, 2),
        ventas=filas,
    )


def obtener_informe_compras(
    db: Session,
    fecha_inicio: datetime,
    fecha_fin: datetime,
    proveedor_id: int | None = None,
    estado: str | None = None,
) -> InformeComprasTabular:
    """
    Genera informe tabular de compras en el período especificado
    """
    # Query base
    query = db.query(OrdenCompra).filter(
        OrdenCompra.fecha_orden >= fecha_inicio,
        OrdenCompra.fecha_orden <= fecha_fin,
    )
    
    # Filtros opcionales
    if proveedor_id:
        query = query.filter(OrdenCompra.proveedor_id == proveedor_id)
    if estado:
        query = query.filter(OrdenCompra.estado_orden == estado)
    
    ordenes = query.all()
    
    # Construir filas del informe
    filas: list[FilaCompraTabular] = []
    totales = []
    
    for orden in ordenes:
        cantidad_items = len(orden.detalles) if hasattr(orden, 'detalles') else 0
        
        filas.append(
            FilaCompraTabular(
                numero_orden=str(orden.id),  # Ajusta si tienes un número de orden
                proveedor=orden.proveedor.nombre if orden.proveedor else "N/A",
                fecha_orden=orden.fecha_orden,
                cantidad_items=cantidad_items,
                subtotal=orden.total_orden,
                total_orden=orden.total_orden,
                estado=orden.estado_orden.value,
                usuario="N/A",  # Ajusta según tus datos
            )
        )
        totales.append(orden.total_orden)
    
    # Calcular métricas
    cantidad_registros = len(ordenes)
    total_invertido = sum(totales) if totales else 0.0
    promedio_orden = total_invertido / cantidad_registros if cantidad_registros > 0 else 0.0
    orden_maxima = max(totales) if totales else 0.0
    orden_minima = min(totales) if totales else 0.0
    
    periodo = f"{_format_fecha(fecha_inicio)} a {_format_fecha(fecha_fin)}"
    
    return InformeComprasTabular(
        periodo=periodo,
        fecha_generacion=datetime.now(timezone.utc),
        cantidad_registros=cantidad_registros,
        total_invertido=round(total_invertido, 2),
        promedio_orden=round(promedio_orden, 2),
        orden_maxima=round(orden_maxima, 2),
        orden_minima=round(orden_minima, 2),
        compras=filas,
    )


def obtener_informe_consolidado(
    db: Session,
    fecha_inicio: datetime,
    fecha_fin: datetime,
) -> InformeConsolidado:
    """
    Genera informe consolidado: ventas + compras + análisis por producto
    """
    # Obtener informes de ventas y compras
    informe_ventas = obtener_informe_ventas(db, fecha_inicio, fecha_fin)
    informe_compras = obtener_informe_compras(db, fecha_inicio, fecha_fin)
    
    # Calcular ganancia bruta
    ganancia_bruta = informe_ventas.total_ingresos - informe_compras.total_invertido
    margen_porcentaje = (
        (ganancia_bruta / informe_ventas.total_ingresos * 100)
        if informe_ventas.total_ingresos > 0
        else 0.0
    )
    
    # Resumen consolidado
    resumen = ResumenPeriodo(
        periodo=informe_ventas.periodo,
        fecha_generacion=datetime.now(timezone.utc),
        total_ventas=informe_ventas.cantidad_registros,
        total_ingresos=informe_ventas.total_ingresos,
        promedio_venta=informe_ventas.promedio_venta,
        total_compras=informe_compras.cantidad_registros,
        total_invertido=informe_compras.total_invertido,
        promedio_compra=informe_compras.promedio_orden,
        ganancia_bruta=round(ganancia_bruta, 2),
        margen_porcentaje=round(margen_porcentaje, 2),
    )
    
    # Análisis por producto
    productos_consolidados = _obtener_detalles_productos(
        db, fecha_inicio, fecha_fin
    )
    
    # Top 5 productos por ganancia
    top_5 = sorted(
        productos_consolidados,
        key=lambda x: x.ganancia,
        reverse=True
    )[:5]
    
    return InformeConsolidado(
        resumen=resumen,
        productos=productos_consolidados,
        detalles_productos_top_5=top_5,
    )


def _obtener_detalles_productos(
    db: Session,
    fecha_inicio: datetime,
    fecha_fin: datetime,
) -> list[DetalleProductoConsolidado]:
    """
    Obtiene detalles de ventas y compras por producto
    """
    # Obtener todos los productos
    productos = db.query(Producto).all()
    detalles = []
    
    for producto in productos:
        # Ventas del producto
        ventas = db.query(DetalleVenta).join(Venta).filter(
            DetalleVenta.producto_id == producto.id,
            Venta.fecha_venta >= fecha_inicio,
            Venta.fecha_venta <= fecha_fin,
            Venta.estado == EstadoVenta.confirmada,
        ).all()
        
        cantidad_vendida = sum(v.cantidad for v in ventas)
        ingresos_venta = sum(v.subtotal for v in ventas)
        
        # Compras del producto
        compras = db.query(DetalleCompra).join(OrdenCompra).filter(
            DetalleCompra.producto_id == producto.id,
            OrdenCompra.fecha_orden >= fecha_inicio,
            OrdenCompra.fecha_orden <= fecha_fin,
            OrdenCompra.estado_orden == EstadoOrden.recibida,
        ).all()
        
        cantidad_comprada = sum(c.cantidad for c in compras)
        costo_compra = sum(c.subtotal for c in compras)
        
        # Si hay movimiento, incluir en el reporte
        if cantidad_vendida > 0 or cantidad_comprada > 0:
            ganancia = ingresos_venta - costo_compra
            
            detalles.append(
                DetalleProductoConsolidado(
                    nombre_producto=producto.nombre,
                    cantidad_vendida=cantidad_vendida,
                    cantidad_comprada=cantidad_comprada,
                    ingresos_venta=round(ingresos_venta, 2),
                    costo_compra=round(costo_compra, 2),
                    ganancia=round(ganancia, 2),
                    stock_actual=producto.stock_actual,
                )
            )
    
    return detalles


