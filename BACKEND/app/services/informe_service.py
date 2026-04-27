from datetime import datetime, timezone, date, time
from sqlalchemy.orm import Session

from app.models.venta import Venta, DetalleVenta, EstadoVenta
from app.models.proveedor import OrdenCompra, DetalleCompra, EstadoOrden
from app.models.producto import Producto
from app.schemas.informe import (
    FilaVentaTabular,
    InformeVentasTabular,
    FilaCompraTabular,
    InformeComprasTabular,
    ResumenPeriodo,
    DetalleProductoConsolidado,
    InformeConsolidado,
)


def _format_fecha(fecha: datetime | date | None) -> str:
    if fecha is None:
        return ""
    if isinstance(fecha, datetime):
        return fecha.strftime("%Y-%m-%d %H:%M:%S")
    return fecha.strftime("%Y-%m-%d")


def _as_datetime(fecha: date | datetime | None) -> datetime | None:
    if fecha is None:
        return None
    if isinstance(fecha, datetime):
        return fecha
    return datetime.combine(fecha, time.min)


def _estado_venta_str(estado: EstadoVenta | str | None) -> str:
    if estado is None:
        return ""
    return estado.value if isinstance(estado, EstadoVenta) else str(estado)


def _estado_orden_str(estado: EstadoOrden | str | None) -> str:
    if estado is None:
        return ""
    return estado.value if isinstance(estado, EstadoOrden) else str(estado)


def obtener_informe_ventas(
    db: Session,
    fecha_inicio: datetime,
    fecha_fin: datetime,
    cliente_id: int | None = None,
    estado: str | None = None,
) -> InformeVentasTabular:
    d0 = fecha_inicio.date()
    d1 = fecha_fin.date()

    query = db.query(Venta).filter(
        Venta.fecha_venta.isnot(None),
        Venta.fecha_venta >= d0,
        Venta.fecha_venta <= d1,
    )

    if cliente_id:
        query = query.filter(Venta.cliente_id == cliente_id)
    if estado:
        match = next(
            (e for e in EstadoVenta if e.value.lower() == estado.strip().lower()),
            None,
        )
        if match is not None:
            query = query.filter(Venta.estado == match)

    ventas = query.all()

    filas: list[FilaVentaTabular] = []
    totales: list[float] = []

    for venta in ventas:
        cantidad_items = len(venta.detalles)
        subtotal = sum(float(d.subtotal or 0) for d in venta.detalles)
        fv = venta.fecha_venta
        fecha_dt = _as_datetime(fv) or datetime.now(timezone.utc)

        filas.append(
            FilaVentaTabular(
                numero_factura=venta.numero_factura or "",
                cliente=venta.cliente.nombre_completo if venta.cliente else "N/A",
                fecha_venta=fecha_dt,
                cantidad_items=cantidad_items,
                subtotal=subtotal,
                total=float(venta.total or 0),
                estado=_estado_venta_str(venta.estado),
                usuario=venta.usuario.nombre_completo if venta.usuario else "N/A",
            )
        )
        totales.append(float(venta.total or 0))

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
    query = db.query(OrdenCompra).filter(
        OrdenCompra.fecha_orden.isnot(None),
        OrdenCompra.fecha_orden >= fecha_inicio.date(),
        OrdenCompra.fecha_orden <= fecha_fin.date(),
    )

    if proveedor_id:
        query = query.filter(OrdenCompra.proveedor_id == proveedor_id)
    if estado:
        match = next(
            (e for e in EstadoOrden if e.value.lower() == estado.strip().lower()),
            None,
        )
        if match is not None:
            query = query.filter(OrdenCompra.estado_orden == match)

    ordenes = query.all()

    filas: list[FilaCompraTabular] = []
    totales: list[float] = []

    for orden in ordenes:
        cantidad_items = len(orden.detalles) if orden.detalles else 0
        fo = orden.fecha_orden
        fecha_dt = _as_datetime(fo) or datetime.now(timezone.utc)

        filas.append(
            FilaCompraTabular(
                numero_orden=str(orden.id),
                proveedor=orden.proveedor.nombre if orden.proveedor else "N/A",
                fecha_orden=fecha_dt,
                cantidad_items=cantidad_items,
                subtotal=float(orden.total_orden or 0),
                total_orden=float(orden.total_orden or 0),
                estado=_estado_orden_str(orden.estado_orden),
                usuario="N/A",
            )
        )
        totales.append(float(orden.total_orden or 0))

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
    informe_ventas = obtener_informe_ventas(db, fecha_inicio, fecha_fin)
    informe_compras = obtener_informe_compras(db, fecha_inicio, fecha_fin)

    ganancia_bruta = informe_ventas.total_ingresos - informe_compras.total_invertido
    margen_porcentaje = (
        (ganancia_bruta / informe_ventas.total_ingresos * 100)
        if informe_ventas.total_ingresos > 0
        else 0.0
    )

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

    productos_consolidados = _obtener_detalles_productos(db, fecha_inicio, fecha_fin)

    top_5 = sorted(productos_consolidados, key=lambda x: x.ganancia, reverse=True)[:5]

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
    productos = db.query(Producto).all()
    detalles: list[DetalleProductoConsolidado] = []
    d0 = fecha_inicio.date()
    d1 = fecha_fin.date()

    for producto in productos:
        ventas = (
            db.query(DetalleVenta)
            .join(Venta)
            .filter(
                DetalleVenta.producto_id == producto.id,
                Venta.fecha_venta.isnot(None),
                Venta.fecha_venta >= d0,
                Venta.fecha_venta <= d1,
                Venta.estado == EstadoVenta.completada,
            )
            .all()
        )

        cantidad_vendida = sum(int(v.cantidad or 0) for v in ventas)
        ingresos_venta = sum(float(v.subtotal or 0) for v in ventas)

        compras = (
            db.query(DetalleCompra)
            .join(OrdenCompra)
            .filter(
                DetalleCompra.producto_id == producto.id,
                OrdenCompra.fecha_orden.isnot(None),
                OrdenCompra.fecha_orden >= d0,
                OrdenCompra.fecha_orden <= d1,
                OrdenCompra.estado_orden == EstadoOrden.completada,
            )
            .all()
        )

        cantidad_comprada = sum(int(c.cantidad or 0) for c in compras)
        costo_compra = sum(float(c.subtotal or 0) for c in compras)

        if cantidad_vendida > 0 or cantidad_comprada > 0:
            ganancia = ingresos_venta - costo_compra

            detalles.append(
                DetalleProductoConsolidado(
                    nombre_producto=producto.nombre or "",
                    cantidad_vendida=cantidad_vendida,
                    cantidad_comprada=cantidad_comprada,
                    ingresos_venta=round(ingresos_venta, 2),
                    costo_compra=round(costo_compra, 2),
                    ganancia=round(ganancia, 2),
                    stock_actual=int(producto.stock_actual or 0),
                )
            )

    return detalles
